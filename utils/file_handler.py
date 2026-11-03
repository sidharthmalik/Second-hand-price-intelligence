"""CSV read/write helpers with error handling (CO3)."""
import os
import pandas as pd


def load_csv(path: str) -> pd.DataFrame:
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Dataset not found at '{path}'. Run: python generate_data.py")
    except pd.errors.EmptyDataError:
        raise ValueError(f"Dataset '{path}' is empty.")


def save_csv(df: pd.DataFrame, path: str) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    df.to_csv(path, index=False)
