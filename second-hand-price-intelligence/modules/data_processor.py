"""Data cleaning and feature engineering (CO4)."""
from datetime import date
import pandas as pd

CURRENT_YEAR = date.today().year
NUMERIC = ["release_year", "purchase_year", "ram_gb", "storage_gb",
           "original_price", "listed_price"]


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.drop_duplicates(subset="product_id")
    for col in NUMERIC:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["brand", "model", "category", "condition",
                           "release_year", "original_price", "listed_price"])
    df = df[(df["listed_price"] > 0) & (df["original_price"] > 0)]
    for col in ["brand", "model", "category", "condition", "processor"]:
        df[col] = df[col].astype(str).str.strip()
    df = add_features(df)
    return df.reset_index(drop=True)


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["age"] = CURRENT_YEAR - df["release_year"].astype(int)
    df["retained_pct"] = (df["listed_price"] / df["original_price"] * 100).round(1)
    return df
