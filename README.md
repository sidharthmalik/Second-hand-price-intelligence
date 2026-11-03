# Second-Hand Product Price Intelligence System


A Python application that estimates the **fair market price** of second-hand electronics and flags listings that are **potentially overpriced or undervalued**, using transparent statistics instead of a black-box model.


## The problem

Second-hand listings for the same product are often priced very differently, which makes it hard for buyers to spot a fair deal and for sellers to price sensibly. This project compares a listing against similar listings and tells you how far it sits from the estimated market price.

## Features

| Feature | What it does |
|---|---|
| Product management | Add, update, delete and search listings (CSV-backed CRUD) |
| Fair price estimation | Weighted median of the most similar listings |
| Overpricing / undervalued detection | Flags listings more than 15% above or below the estimate |
| Price comparison | Shows the asking price against the distribution of comparable listings |
| Brand analysis | Average, median and spread of prices by brand, plus value retained |
| Depreciation analysis | Value retained by product age and an estimated yearly depreciation rate |
| Analytics dashboard | Price distributions, price vs age, verdict counts, top over/under-priced listings |

## Example

Checking a Lenovo ThinkPad T480 (Intel i5, 8 GB RAM, 256 GB SSD, Good condition) listed at Rs 22,000 against the synthetic dataset:

| Metric | Result |
|---|---|
| Estimated fair price | Rs 16,500 |
| Market average (weighted) | Rs 16,607 |
| Difference | +33.3% |
| Comparable listings used | 26 |
| Verdict | Potentially overpriced |

## How the estimate works

1. **Filter** to listings in the same category, excluding the listing being checked.
2. **Score similarity** for every candidate: same model (+4), same brand (+2), same condition (+1.5), same RAM (+1), same storage (+1), plus a bonus for similar age.
3. **Take the top 30** most similar listings.
4. **Remove outliers** with the IQR rule (1.5 x IQR fences).
5. **Fair price** = weighted median of the remaining prices, using similarity scores as weights.
6. **Verdict** = difference between the asking price and the fair price: above +15% is overpriced, below -15% is undervalued, otherwise fairly priced.

Depreciation is estimated by fitting `retained = exp(k * age)` on log price ratios with NumPy, giving an approximate yearly value loss. No machine learning is used, so every result can be traced and explained.

## Tech stack

Python, NumPy, Pandas, Matplotlib, Seaborn, Streamlit, pytest, CSV storage.

## Project structure

```
second-hand-price-intelligence/
├── app.py                     # Streamlit dashboard
├── generate_data.py           # Synthetic dataset generator
├── data/
│   └── products.csv
├── modules/
│   ├── product.py             # Product, Laptop, Smartphone, Tablet classes
│   ├── inventory.py           # CRUD and search
│   ├── price_analyzer.py      # Fair price and verdict engine
│   ├── depreciation.py        # Depreciation analysis
│   └── data_processor.py      # Cleaning and feature engineering
├── analytics/
│   ├── statistics.py          # Weighted median, IQR filter, summary stats
│   └── visualization.py       # Matplotlib / Seaborn charts
├── utils/
│   ├── validation.py          # Input validation and custom exception
│   └── file_handler.py        # CSV read/write with error handling
├── tests/
│   └── test_analyzer.py
├── requirements.txt
└── README.md
```

## Getting started

```bash
git clone https://github.com/sidharthmalik/second-hand-price-intelligence.git
cd second-hand-price-intelligence
pip install -r requirements.txt
python generate_data.py      # creates data/products.csv (synthetic)
streamlit run app.py
```

Run the tests:

```bash
python -m pytest
```

## Dataset format

`data/products.csv` expects these columns:

`product_id, brand, model, category, release_year, purchase_year, condition, processor, ram_gb, storage_gb, original_price, listed_price`

- `category`: Laptop, Smartphone or Tablet
- `condition`: Like New, Good, Fair or Poor

To use real data, replace the file with real listings in this format (ideally adding collection date and source), then restart the app.

## Concepts demonstrated

- **OOP:** a `Product` base class with `Laptop`, `Smartphone` and `Tablet` subclasses, and a factory function
- **Modular architecture:** separate packages for data, analytics and utilities
- **Exception handling:** a custom `ValidationError` and safe file loading
- **Data analysis:** cleaning, filtering, grouping, aggregation, median, standard deviation, IQR outlier removal
- **Visualization and testing:** an interactive dashboard and unit tests for the statistics, validation and verdict logic

## Limitations and future work

- The estimate is only as good as the dataset; synthetic data demonstrates the method but does not reflect real prices.
- The 15% verdict threshold and similarity weights are fixed choices, not tuned on real data.
- Depreciation fits are unreliable for categories where the data covers a narrow range of product ages.
- Ideas: scrape or import real listings with dates and sources, add price-trend tracking over time, let users tune the thresholds in the UI, add more categories.

## Author

**Sidharth Malik**: MCA (Data Science), Chandigarh University

Built as a university Python mini project.

## License

MIT. Add a `LICENSE` file to the repository root (GitHub can generate one when you create the repo).
