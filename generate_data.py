"""Creates a SYNTHETIC dataset (data/products.csv) for development.
Replace it with real, dated and sourced listings for credible results."""
import numpy as np
import pandas as pd
from datetime import date

rng = np.random.default_rng(42)
CURRENT_YEAR = date.today().year

# category, brand, model, release_year, processor, base_ram, base_storage, original_price
CATALOG = [
    ("Laptop", "Lenovo", "ThinkPad T480", 2018, "Intel i5", 8, 256, 65000),
    ("Laptop", "Dell", "Latitude 5490", 2018, "Intel i5", 8, 256, 60000),
    ("Laptop", "HP", "EliteBook 840 G5", 2018, "Intel i5", 8, 256, 70000),
    ("Laptop", "Apple", "MacBook Air M1", 2020, "Apple M1", 8, 256, 92000),
    ("Laptop", "Asus", "VivoBook 15", 2021, "Intel i3", 8, 512, 48000),
    ("Laptop", "Acer", "Aspire 5", 2021, "Intel i5", 8, 512, 45000),
    ("Laptop", "HP", "Pavilion 15", 2020, "Intel i5", 8, 512, 55000),
    ("Smartphone", "Apple", "iPhone 12", 2020, "A14 Bionic", 4, 128, 65000),
    ("Smartphone", "Samsung", "Galaxy S21", 2021, "Exynos 2100", 8, 128, 70000),
    ("Smartphone", "OnePlus", "OnePlus 9", 2021, "Snapdragon 888", 8, 128, 50000),
    ("Smartphone", "Xiaomi", "Redmi Note 10", 2021, "Snapdragon 678", 4, 64, 15000),
    ("Smartphone", "Realme", "Realme 8", 2021, "Helio G95", 6, 128, 16000),
    ("Tablet", "Apple", "iPad 9th Gen", 2021, "A13 Bionic", 3, 64, 30000),
    ("Tablet", "Samsung", "Galaxy Tab A8", 2022, "Unisoc T618", 4, 64, 20000),
]
COND_FACTOR = {"Like New": 1.10, "Good": 1.00, "Fair": 0.88, "Poor": 0.72}
BRAND_PREMIUM = {"Apple": 1.15}


def build(n=1200):
    rows = []
    for i in range(1, n + 1):
        cat, brand, model, rel, proc, ram0, sto0, orig0 = CATALOG[rng.integers(len(CATALOG))]
        ram = ram0 * int(rng.choice([1, 1, 2]))
        storage = sto0 * int(rng.choice([1, 1, 2]))
        orig = round(orig0 * (1 + 0.08 * np.log2(ram / ram0) + 0.06 * np.log2(storage / sto0)), -2)
        cond = rng.choice(list(COND_FACTOR), p=[0.2, 0.45, 0.25, 0.1])
        purchase = int(min(CURRENT_YEAR, rel + rng.integers(0, 3)))
        age = CURRENT_YEAR - rel
        price = (orig * np.exp(-0.17 * age) * COND_FACTOR[cond]
                 * BRAND_PREMIUM.get(brand, 1.0) * rng.lognormal(0, 0.07))
        if rng.random() < 0.10:                       # seed some mispriced listings
            price *= rng.choice([rng.uniform(1.25, 1.5), rng.uniform(0.55, 0.75)])
        rows.append({"product_id": f"P{i:04d}", "brand": brand, "model": model,
                     "category": cat, "release_year": rel, "purchase_year": purchase,
                     "condition": cond, "processor": proc, "ram_gb": ram,
                     "storage_gb": storage, "original_price": orig,
                     "listed_price": max(1000, round(price / 500) * 500)})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = build()
    df.to_csv("data/products.csv", index=False)
    print(f"Saved {len(df)} SYNTHETIC listings to data/products.csv")
