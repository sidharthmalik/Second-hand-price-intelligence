# Second-Hand Product Price Intelligence System

A Python application that estimates the **fair market price** of second-hand electronics (laptops, smartphones and tablets) and flags listings that are **overpriced or undervalued**. It uses transparent statistics instead of a black-box model, so every result can be traced and explained.
<img width="1470" height="832" alt="Screenshot 2026-11-03 at 7 48 34 AM" src="https://github.com/user-attachments/assets/9ac74668-01ca-4315-b7bb-25bbf5879b63" />

---

## Why this project?

Listings for the same second-hand product are often priced very differently. Buyers struggle to spot a fair deal, and sellers struggle to price sensibly. This project compares a listing against similar listings and shows how far its asking price sits from the estimated market price.

## Features

| Feature | What it does |
|---|---|
| **Product management** | Add, update, delete and search listings (CSV-backed CRUD) |
| **Fair price estimation** | Weighted median of the most similar listings |
| **Overpricing / undervaluation detection** | Flags listings more than 15% above or below the estimate |
| **Price comparison** | Shows the asking price against the distribution of comparable listings |
| **Brand analysis** | Average, median and spread of prices by brand, plus value retained |
| **Depreciation analysis** | Value retained by product age and an estimated yearly depreciation rate |
| **Analytics dashboard** | Price distributions, price vs age, verdict counts, top over- and under-priced listings |

## Example

Checking a **Lenovo ThinkPad T480** (Intel i5, 8 GB RAM, 256 GB SSD, Good condition) listed at **Rs 22,000** against the synthetic dataset:

| Metric | Result |
|---|---|
| Estimated fair price | Rs 16,500 |
| Market average (weighted) | Rs 16,607 |
| Difference | +33.3% |
| Comparable listings used | 26 |
| Verdict | **Potentially overpriced** |

## How the estimate works

1. **Filter** to listings in the same category, excluding the listing being checked.
2. **Score similarity** for every candidate:

   | Match | Points |
   |---|---|
   | Same model | +4 |
   | Same brand | +2 |
   | Same condition | +1.5 |
   | Same RAM | +1 |
   | Same storage | +1 |
   | Similar age | bonus |

3. **Select** the 30 most similar listings.
4. **Remove outliers** with the IQR rule (1.5 × IQR fences).
5. **Fair price** = weighted median of the remaining prices, using the similarity scores as weights.
6. **Verdict** = difference between the asking price and the fair price:
   - above **+15%** → potentially overpriced
   - below **-15%** → potentially undervalued
   - otherwise → fairly priced

**Depreciation** is estimated by fitting `retained = exp(k × age)` to the log price ratios with NumPy, which gives an approximate yearly value loss. No machine learning is used.

## Tech stack

Python · NumPy · Pandas · Matplotlib · Seaborn · Streamlit · pytest · CSV storage

## Project structure

```
second-hand-price-intelligence/
├── app.py                  # Streamlit dashboard
├── generate_data.py        # Synthetic dataset generator
├── data/
│   └── products.csv
├── modules/
│   ├── product.py          # Product, Laptop, Smartphone, Tablet classes
│   ├── inventory.py        # CRUD and search
│   ├── price_analyzer.py   # Fair price and verdict engine
│   ├── depreciation.py     # Depreciation analysis
│   └── data_processor.py   # Cleaning and feature engineering
├── analytics/
│   ├── statistics.py       # Weighted median, IQR filter, summary stats
│   └── visualization.py    # Matplotlib / Seaborn charts
├── utils/
│   ├── validation.py       # Input validation and custom exception
│   └── file_handler.py     # CSV read/write with error handling
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
python generate_data.py          # creates data/products.csv (synthetic)
python -m streamlit run app.py   # opens the dashboard in your browser
```

> **Note:** Streamlit apps must be started with `streamlit run`. Running `python app.py` directly will not open the dashboard.

Run the tests:

```bash
python -m pytest
```

## Dataset format

`data/products.csv` expects these columns:

```
product_id, brand, model, category, release_year, purchase_year,
condition, processor, ram_gb, storage_gb, original_price, listed_price
```

- **category:** `Laptop`, `Smartphone` or `Tablet`
- **condition:** `Like New`, `Good`, `Fair` or `Poor`

To use real data, replace the file with real listings in this format (ideally adding a collection date and source), then restart the app.

## Concepts demonstrated

- **Object-oriented programming:** a `Product` base class with `Laptop`, `Smartphone` and `Tablet` subclasses, and a factory function
- **Modular architecture:** separate packages for data, analytics and utilities
- **Exception handling:** a custom `ValidationError` and safe file loading
- **Data analysis:** cleaning, filtering, grouping, aggregation, median, standard deviation and IQR outlier removal
- **Visualization and testing:** an interactive dashboard and unit tests for the statistics, validation and verdict logic

## Limitations and future work

**Limitations**

- The estimate is only as good as the dataset. The synthetic data demonstrates the method but does not reflect real prices.
- The 15% verdict threshold and the similarity weights are fixed choices, not tuned on real data.
- Depreciation fits are unreliable for categories where the data covers a narrow range of product ages.

**Ideas for the future**

- Scrape or import real listings with dates and sources
- Add price-trend tracking over time
- Let users tune the thresholds in the UI
- Add more product categories

## Author

**Sidharth Malik**: MCA (Data Science), Chandigarh University

Built as a university Python mini project.
