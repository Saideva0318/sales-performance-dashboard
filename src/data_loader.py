"""
Data Loader Module
Generates realistic mock sales data and handles CSV/Excel ingestion.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

RAW_DATA_PATH = Path("data/raw")
PROCESSED_DATA_PATH = Path("data/processed")


def generate_mock_sales_data(n_records: int = 5000, seed: int = 42) -> pd.DataFrame:
    """
    Generate realistic mock sales transaction data.
    
    Args:
        n_records: Number of transaction records to generate
        seed: Random seed for reproducibility
    
    Returns:
        DataFrame with sales transactions
    """
    np.random.seed(seed)
    
    regions = ["Northeast", "Southeast", "Midwest", "West", "Southwest"]
    categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Food & Beverage"]
    products = {
        "Electronics": ["Laptop", "Smartphone", "Tablet", "Headphones", "Smart Watch"],
        "Clothing": ["T-Shirt", "Jeans", "Jacket", "Dress", "Sneakers"],
        "Home & Garden": ["Sofa", "Lamp", "Blender", "Plant Pot", "Rug"],
        "Sports": ["Running Shoes", "Yoga Mat", "Dumbbells", "Bicycle", "Tennis Racket"],
        "Food & Beverage": ["Coffee Beans", "Protein Bar", "Olive Oil", "Tea Set", "Juice Pack"]
    }
    sales_reps = [f"Rep_{i:03d}" for i in range(1, 21)]
    
    dates = pd.date_range(start="2022-01-01", end="2023-12-31", periods=n_records)
    
    cat_choices = np.random.choice(categories, n_records)
    product_choices = [np.random.choice(products[cat]) for cat in cat_choices]
    base_prices = {
        "Electronics": (150, 1500), "Clothing": (20, 200),
        "Home & Garden": (30, 800), "Sports": (25, 500), "Food & Beverage": (5, 80)
    }
    
    unit_prices = np.array([
        np.random.uniform(*base_prices[cat]) for cat in cat_choices
    ]).round(2)
    quantities = np.random.randint(1, 20, n_records)
    discount_pct = np.random.choice([0, 5, 10, 15, 20], n_records, p=[0.5, 0.2, 0.15, 0.1, 0.05])
    cost_pct = np.random.uniform(0.4, 0.75, n_records)
    
    revenue = (unit_prices * quantities * (1 - discount_pct / 100)).round(2)
    cost = (revenue * cost_pct).round(2)
    profit = (revenue - cost).round(2)
    
    df = pd.DataFrame({
        "transaction_id": [f"TXN_{i:06d}" for i in range(1, n_records + 1)],
        "date": dates,
        "region": np.random.choice(regions, n_records),
        "category": cat_choices,
        "product": product_choices,
        "sales_rep": np.random.choice(sales_reps, n_records),
        "unit_price": unit_prices,
        "quantity": quantities,
        "discount_pct": discount_pct,
        "revenue": revenue,
        "cost": cost,
        "profit": profit
    })
    
    logger.info(f"Generated {n_records} sales records from 2022-01-01 to 2023-12-31")
    return df


def load_data(filepath: str = None) -> pd.DataFrame:
    """
    Load data from CSV file or generate mock data if no file provided.
    
    Args:
        filepath: Path to CSV file (optional)
    
    Returns:
        DataFrame with sales data
    """
    if filepath and Path(filepath).exists():
        logger.info(f"Loading data from {filepath}")
        df = pd.read_csv(filepath, parse_dates=["date"])
    else:
        logger.info("No data file found — generating mock sales data")
        df = generate_mock_sales_data()
        
        RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)
        output_path = RAW_DATA_PATH / "sales_data.csv"
        df.to_csv(output_path, index=False)
        logger.info(f"Mock data saved to {output_path}")
    
    return df


if __name__ == "__main__":
    df = load_data()
    print(f"\nDataset Shape: {df.shape}")
    print(f"Date Range: {df['date'].min().date()} → {df['date'].max().date()}")
    print(f"Total Revenue: ${df['revenue'].sum():,.2f}")
    print(f"Total Profit: ${df['profit'].sum():,.2f}")
    print(f"\nSample Records:")
    print(df.head())
