"""Fair-price estimation and over/under-pricing detection (CO2, CO4)."""
import numpy as np
import pandas as pd
from analytics.statistics import weighted_median, iqr_mask
from modules.data_processor import CURRENT_YEAR

OVERPRICED_PCT = 15.0
UNDERVALUED_PCT = -15.0


class PriceAnalyzer:
    def __init__(self, df: pd.DataFrame, top_n: int = 30):
        self.df = df.reset_index(drop=True)
        self.top_n = top_n
        d = self.df
        self._cat = d["category"].to_numpy()
        self._brand = d["brand"].to_numpy()
        self._model = d["model"].to_numpy()
        self._ram = d["ram_gb"].to_numpy()
        self._storage = d["storage_gb"].to_numpy()
        self._cond = d["condition"].to_numpy()
        self._age = d["age"].to_numpy()
        self._price = d["listed_price"].to_numpy(dtype=float)
        self._pid = d["product_id"].to_numpy()

    @staticmethod
    def classify(diff_pct: float) -> str:
        if diff_pct > OVERPRICED_PCT:
            return "Potentially overpriced"
        if diff_pct < UNDERVALUED_PCT:
            return "Potentially undervalued"
        return "Fairly priced"

    def _similarity(self, item: dict, age: int) -> np.ndarray:
        """Score every listing by how similar it is to `item`."""
        score = np.zeros(len(self.df))
        score += 4.0 * (self._model == item["model"])
        score += 2.0 * (self._brand == item["brand"])
        score += 1.0 * (self._ram == item["ram_gb"])
        score += 1.0 * (self._storage == item["storage_gb"])
        score += 1.5 * (self._cond == item["condition"])
        score += np.clip(1 - np.abs(self._age - age) / 3.0, 0, 1)
        return score

    def comparables(self, item: dict) -> pd.DataFrame:
        """Return the most similar listings (outliers removed) with their weights."""
        age = CURRENT_YEAR - int(item["release_year"])
        mask = self._cat == item["category"]
        if item.get("product_id") is not None:
            mask &= self._pid != item["product_id"]
        idx = np.where(mask)[0]
        if len(idx) < 3:
            raise ValueError("Not enough comparable listings in this category.")
        scores = self._similarity(item, age)[idx]
        top = np.argsort(-scores, kind="stable")[: self.top_n]
        idx, scores = idx[top], scores[top]
        keep = iqr_mask(self._price[idx])
        out = self.df.iloc[idx[keep]].copy()
        out["weight"] = scores[keep]
        return out

    def estimate(self, item: dict) -> dict:
        """item needs: category, brand, model, ram_gb, storage_gb, condition,
        release_year, listed_price (and optionally product_id)."""
        comp = self.comparables(item)
        prices, weights = comp["listed_price"].to_numpy(), comp["weight"].to_numpy()
        fair = weighted_median(prices, weights)
        listed = float(item["listed_price"])
        diff_pct = (listed - fair) / fair * 100
        return {
            "fair_price": round(fair, 0),
            "market_average": round(float(np.average(prices, weights=weights)), 0),
            "listed_price": listed,
            "diff_pct": round(diff_pct, 1),
            "comparables": int(len(prices)),
            "std_dev": round(float(prices.std(ddof=1)) if len(prices) > 1 else 0.0, 0),
            "verdict": self.classify(diff_pct),
        }

    def analyze_all(self) -> pd.DataFrame:
        """Run estimate() for every listing and attach the results."""
        rows = []
        for _, r in self.df.iterrows():
            res = self.estimate(r.to_dict())
            rows.append((res["fair_price"], res["diff_pct"], res["comparables"], res["verdict"]))
        out = self.df.copy()
        out[["fair_price", "diff_pct", "comparables", "verdict"]] = rows
        return out
