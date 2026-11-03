# Second-Hand Product Price Intelligence System

Python application that estimates fair prices for second-hand electronics and flags
potentially overpriced or undervalued listings.

## Run
```
pip install -r requirements.txt
python generate_data.py        # creates SYNTHETIC data/products.csv
streamlit run app.py
pytest
```

## Method
Fair price = weighted median of the most similar listings (model, brand, RAM, storage,
condition and age similarity), after IQR outlier removal. Listings more than 15% above the
estimate are flagged overpriced, more than 15% below undervalued.

## Data note
The bundled dataset is synthetic. For credible results replace it with real listings
(with collection date and source). Estimates are illustrative, not verified valuations.
