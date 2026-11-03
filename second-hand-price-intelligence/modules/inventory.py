"""Product CRUD operations (CO2)."""
import pandas as pd
from modules.data_processor import clean_data, add_features
from utils.file_handler import load_csv, save_csv
from utils.validation import validate_product

COLUMNS = ["product_id", "brand", "model", "category", "release_year",
           "purchase_year", "condition", "processor", "ram_gb", "storage_gb",
           "original_price", "listed_price"]


class Inventory:
    def __init__(self, path: str = "data/products.csv"):
        self.path = path
        self.df = clean_data(load_csv(path))

    def _next_id(self) -> str:
        nums = self.df["product_id"].str.extract(r"(\d+)")[0].astype(float)
        n = int(nums.max()) + 1 if len(nums) else 1
        return f"P{n:04d}"

    def _save(self):
        save_csv(self.df[COLUMNS], self.path)

    def add(self, data: dict) -> str:
        data = validate_product(data)
        if data.get("purchase_year") in (None, ""):
            data["purchase_year"] = data["release_year"]
        data.setdefault("processor", "N/A")
        data["product_id"] = self._next_id()
        row = pd.DataFrame([{c: data.get(c) for c in COLUMNS}])
        self.df = add_features(pd.concat([self.df, row], ignore_index=True))
        self._save()
        return data["product_id"]

    def update(self, product_id: str, **changes) -> None:
        mask = self.df["product_id"] == product_id
        if not mask.any():
            raise KeyError(f"Product {product_id} not found")
        merged = {**self.df[mask].iloc[0][COLUMNS].to_dict(), **changes}
        merged = validate_product(merged)
        for k, v in merged.items():
            if k in COLUMNS:
                self.df.loc[mask, k] = v
        self.df = add_features(self.df)
        self._save()

    def delete(self, product_id: str) -> bool:
        before = len(self.df)
        self.df = self.df[self.df["product_id"] != product_id].reset_index(drop=True)
        removed = len(self.df) < before
        if removed:
            self._save()
        return removed

    def search(self, text: str = "", category=None, brand=None,
               min_price=None, max_price=None) -> pd.DataFrame:
        d = self.df
        if text:
            t = text.lower()
            d = d[d["brand"].str.lower().str.contains(t) | d["model"].str.lower().str.contains(t)]
        if category:
            d = d[d["category"] == category]
        if brand:
            d = d[d["brand"] == brand]
        if min_price is not None:
            d = d[d["listed_price"] >= min_price]
        if max_price is not None:
            d = d[d["listed_price"] <= max_price]
        return d
