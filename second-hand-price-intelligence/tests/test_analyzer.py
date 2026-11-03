import pytest
import pandas as pd
from generate_data import build
from modules.data_processor import clean_data
from modules.price_analyzer import PriceAnalyzer
from modules.depreciation import fit_depreciation_rate
from analytics.statistics import weighted_median, iqr_mask
from utils.validation import validate_product, ValidationError


@pytest.fixture(scope="module")
def df():
    return clean_data(build(600))


def test_weighted_median():
    assert weighted_median([1, 2, 3], [1, 1, 1]) == 2
    assert weighted_median([1, 100], [10, 1]) == 1


def test_iqr_removes_outlier():
    mask = iqr_mask([10, 11, 12, 11, 10, 500])
    assert not mask[-1] and mask[:-1].all()


def test_overpriced_and_undervalued(df):
    a = PriceAnalyzer(df)
    row = df.iloc[0].to_dict()
    base = a.estimate({**row, "product_id": None})["fair_price"]
    assert a.estimate({**row, "product_id": None, "listed_price": base * 1.5})["verdict"] == "Potentially overpriced"
    assert a.estimate({**row, "product_id": None, "listed_price": base * 0.5})["verdict"] == "Potentially undervalued"
    assert a.estimate({**row, "product_id": None, "listed_price": base})["verdict"] == "Fairly priced"


def test_depreciation_positive(df):
    assert 0 < fit_depreciation_rate(df) < 1


def test_validation_rejects_bad_data():
    good = dict(brand="Dell", model="X", category="Laptop", release_year=2020,
                condition="Good", ram_gb=8, storage_gb=256,
                original_price=50000, listed_price=20000)
    assert validate_product(good)["listed_price"] == 20000.0
    with pytest.raises(ValidationError):
        validate_product({**good, "listed_price": -5})
    with pytest.raises(ValidationError):
        validate_product({**good, "condition": "Broken"})
    with pytest.raises(ValidationError):
        validate_product({k: v for k, v in good.items() if k != "brand"})
