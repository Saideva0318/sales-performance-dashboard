"""
data_processor.py — Clean, transform, and engineer features from raw sales data.
"""
import pandas as pd
import logging
from pathlib import Path
from data_loader import load_sales_data

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

PROCESSED_PATH = Path("data/processed/sales_cleaned.csv")


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicates, nulls, and out-of-range values."""
    initial_rows = len(df)
    df = df.drop_duplicates()
    df = df.dropna(subset=["revenue", "region", "product"])
    df = df[df["revenue"] > 0]
    df = df[df["quantity"] > 0]
    logger.info(f"Cleaned: {initial_rows:,} → {len(df):,} rows ({initial_rows - len(df):,} removed)")
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add time-based and derived features."""
    df["year"]       = df["order_date"].dt.year
    df["month"]      = df["order_date"].dt.month
    df["quarter"]    = df["order_date"].dt.quarter
    df["year_month"] = df["order_date"].dt.to_period("M").astype(str)
    df["month_name"] = df["order_date"].dt.strftime("%b %Y")
    logger.info("Feature engineering complete.")
    return df


def compute_monthly_revenue(df: pd.DataFrame) -> pd.DataFrame:
    return (df.groupby("year_month")["revenue"].sum().reset_index()
              .rename(columns={"revenue": "monthly_revenue"})
              .sort_values("year_month"))


def compute_region_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (df.groupby("region").agg(
        total_revenue=("revenue", "sum"),
        total_orders=("revenue", "count"),
        avg_order_value=("revenue", "mean")
    ).reset_index().sort_values("total_revenue", ascending=False))


def compute_top_products(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    return (df.groupby("product")["revenue"].sum().reset_index()
              .rename(columns={"revenue": "total_revenue"})
              .sort_values("total_revenue", ascending=False)
              .head(n))


if __name__ == "__main__":
    df = load_sales_data()
    df = clean_data(df)
    df = engineer_features(df)
    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)
    logger.info(f"Processed data saved to {PROCESSED_PATH}")
    print(compute_region_summary(df))
