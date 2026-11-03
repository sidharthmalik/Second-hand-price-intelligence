"""Depreciation analysis (CO4)."""
import numpy as np
import pandas as pd


def depreciation_by_age(df: pd.DataFrame) -> pd.DataFrame:
    """Average % of original price retained at each product age."""
    return (df.groupby("age")["retained_pct"]
              .agg(avg_retained_pct="mean", median_retained_pct="median", listings="count")
              .round(1).reset_index())


def fit_depreciation_rate(df: pd.DataFrame) -> float:
    """Fit retained = exp(slope * age). Returns yearly value loss as a fraction."""
    ratio = (df["listed_price"] / df["original_price"]).clip(lower=0.01)
    slope, _ = np.polyfit(df["age"], np.log(ratio), 1)
    return float(1 - np.exp(slope))


def predict_value(original_price: float, age: int, yearly_rate: float) -> float:
    return float(original_price * (1 - yearly_rate) ** age)


def depreciation_by_category(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for cat, g in df.groupby("category"):
        if g["age"].nunique() > 1:
            rows.append({"category": cat,
                         "yearly_depreciation_pct": round(fit_depreciation_rate(g) * 100, 1)})
    return pd.DataFrame(rows)
