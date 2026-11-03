"""Input validation helpers (CO3: custom exceptions)."""
from datetime import date

CURRENT_YEAR = date.today().year
CONDITIONS = ["Like New", "Good", "Fair", "Poor"]
REQUIRED = ["brand", "model", "category", "release_year", "condition",
            "ram_gb", "storage_gb", "original_price", "listed_price"]
INT_FIELDS = ["release_year", "purchase_year", "ram_gb", "storage_gb"]
FLOAT_FIELDS = ["original_price", "listed_price"]


class ValidationError(Exception):
    """Raised when a product listing has invalid data."""


def validate_product(data: dict) -> dict:
    """Validate and clean a product dict. Returns the cleaned dict."""
    missing = [k for k in REQUIRED if data.get(k) in (None, "")]
    if missing:
        raise ValidationError(f"Missing required fields: {', '.join(missing)}")

    clean = dict(data)
    for key in INT_FIELDS:
        if clean.get(key) not in (None, ""):
            try:
                clean[key] = int(clean[key])
            except (TypeError, ValueError):
                raise ValidationError(f"{key} must be a whole number")
    for key in FLOAT_FIELDS:
        try:
            clean[key] = float(clean[key])
        except (TypeError, ValueError):
            raise ValidationError(f"{key} must be a number")
        if clean[key] <= 0:
            raise ValidationError(f"{key} must be greater than 0")

    if not 2000 <= clean["release_year"] <= CURRENT_YEAR:
        raise ValidationError(f"release_year must be between 2000 and {CURRENT_YEAR}")
    if clean.get("purchase_year") not in (None, ""):
        if not clean["release_year"] <= clean["purchase_year"] <= CURRENT_YEAR:
            raise ValidationError("purchase_year must be between release_year and the current year")
    if clean["condition"] not in CONDITIONS:
        raise ValidationError(f"condition must be one of {CONDITIONS}")
    if clean["ram_gb"] <= 0 or clean["storage_gb"] <= 0:
        raise ValidationError("ram_gb and storage_gb must be greater than 0")
    return clean
