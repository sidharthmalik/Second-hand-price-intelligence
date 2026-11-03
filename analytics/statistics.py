"""Statistical helpers (CO4: median, std, IQR, weighted calculations)."""
import numpy as np


def weighted_median(values, weights) -> float:
    values = np.asarray(values, dtype=float)
    weights = np.asarray(weights, dtype=float)
    order = np.argsort(values)
    values, weights = values[order], weights[order]
    cum = np.cumsum(weights)
    return float(values[np.searchsorted(cum, cum[-1] / 2.0)])


def iqr_mask(values, k: float = 1.5):
    """Boolean mask: True for values inside the IQR fence (not outliers)."""
    values = np.asarray(values, dtype=float)
    if len(values) < 4:
        return np.ones(len(values), dtype=bool)
    q1, q3 = np.percentile(values, [25, 75])
    iqr = q3 - q1
    return (values >= q1 - k * iqr) & (values <= q3 + k * iqr)


def summary_stats(values) -> dict:
    v = np.asarray(values, dtype=float)
    return {"count": int(len(v)), "mean": float(v.mean()),
            "median": float(np.median(v)),
            "std": float(v.std(ddof=1)) if len(v) > 1 else 0.0,
            "min": float(v.min()), "max": float(v.max())}
