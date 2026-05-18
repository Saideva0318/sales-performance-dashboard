"""Synthetic Sales Data Generator for Sales Performance Dashboard."""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
SEED = 42
NUM_RECORDS = 10000
START_DATE = datetime(2022, 1, 1)
END_DATE = datetime(2023, 12, 31)

REGIONS = ['Northeast', 'Southeast', 'Midwest', 'Southwest', 'West']
CATEGORIES = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Food & Beverage']
PRODUCTS = {
    'Electronics': ['Laptop Pro', 'Wireless Earbuds', 'Smart Watch', 'Tablet X', 'USB-C Hub'],
    'Clothing': ['Running Shoes', 'Winter Jacket', 'Casual T-Shirt', 'Denim Jeans', 'Sports Hoodie'],
    'Home & Garden': ['Coffee Maker', 'Air Purifier', 'Garden Tools Set', 'LED Desk Lamp', 'Blender Pro'],
    'Sports': ['Yoga Mat', 'Resistance Bands', 'Protein Shaker', 'Jump Rope', 'Foam Roller'],
    'Food & Beverage': ['Organic Coffee', 'Protein Bars', 'Green Tea Pack', 'Almond Milk', 'Granola Mix']
}
PRICE_RANGES = {
    'Electronics': (49.99, 1299.99),
    'Clothing': (14.99, 149.99),
    'Home & Garden': (19.99, 299.99),
    'Sports': (9.99, 89.99),
    'Food & Beverage': (4.99, 49.99)
}
SALES_CHANNELS = ['Online', 'In-Store', 'Mobile App', 'Wholesale']


def generate_date_range(start: datetime, end: datetime, n: int) -> list:
    delta = (end - start).days
    return [start + timedelta(days=int(np.random.randint(0, delta))) for _ in range(n)]


def generate_sales_data(n_records: int = NUM_RECORDS) -> pd.DataFrame:
    np.random.seed(SEED)
    logger.info(f"Generating {n_records} sales records...")

    dates = generate_date_range(START_DATE, END_DATE, n_records)
    categories = np.random.choice(CATEGORIES, n_records)
    products = [np.random.choice(PRODUCTS[cat]) for cat in categories]
    regions = np.random.choice(REGIONS, n_records)
    channels = np.random.choice(SALES_CHANNELS, n_records, p=[0.45, 0.30, 0.15, 0.10])

    unit_prices = np.array([
        round(np.random.uniform(*PRICE_RANGES[cat]), 2)
        for cat in categories
    ])
    quantities = np.random.randint(1, 15, n_records)

    # Apply seasonal multipliers (Q4 boost)
    seasonal_boost = np.array([
        1.3 if d.month in [11, 12] else (1.1 if d.month in [7, 8] else 1.0)
        for d in dates
    ])
    revenue = np.round(unit_prices * quantities * seasonal_boost, 2)

    # Add noise / discounts
    discount_pct = np.random.choice([0, 0.05, 0.10, 0.15, 0.20], n_records, p=[0.5, 0.2, 0.15, 0.1, 0.05])
    final_revenue = np.round(revenue * (1 - discount_pct), 2)

    df = pd.DataFrame({
        'order_id': [f'ORD-{str(i).zfill(6)}' for i in range(1, n_records + 1)],
        'date': dates,
        'category': categories,
        'product': products,
        'region': regions,
        'channel': channels,
        'unit_price': unit_prices,
        'quantity': quantities,
        'discount_pct': discount_pct,
        'revenue': final_revenue,
        'customer_id': [f'CUST-{np.random.randint(1000, 9999)}' for _ in range(n_records)]
    })

    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').reset_index(drop=True)
    logger.info(f"Generated {len(df)} records. Revenue range: ${df['revenue'].min():.2f} - ${df['revenue'].max():.2f}")
    return df


def save_data(df: pd.DataFrame, path: str = 'data/raw/sales_data.csv') -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    logger.info(f"Data saved to {path} ({len(df)} rows, {df.shape[1]} columns)")


if __name__ == '__main__':
    df = generate_sales_data()
    save_data(df)
    print(f"\n✅ Sample Data Preview:")
    print(df.head())
    print(f"\nTotal Revenue: ${df['revenue'].sum():,.2f}")
    print(f"Date Range: {df['date'].min().date()} to {df['date'].max().date()}")
