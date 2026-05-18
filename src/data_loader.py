"""
data_loader.py — Load and validate raw sales CSV data.
"""
import pandas as pd
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

RAW_DATA_PATH = Path("data/raw/sales_data.csv")


def load_sales_data(filepath: Path = RAW_DATA_PATH) -> pd.DataFrame:
    """Load raw sales CSV into a DataFrame with basic validation."""
    if not filepath.exists():
        raise FileNotFoundError(f"Data file not found: {filepath}")

    df = pd.read_csv(filepath, parse_dates=["order_date"])
    logger.info(f"Loaded {len(df):,} rows from {filepath}")

    required_cols = {"order_date", "region", "product", "sales_rep", "quantity", "unit_price", "revenue"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    logger.info("Schema validation passed.")
    return df


if __name__ == "__main__":
    df = load_sales_data()
    print(df.head())
    print(df.dtypes)
