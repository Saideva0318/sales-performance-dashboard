"""
Transformations Module
Feature engineering, KPI calculations, and data aggregations.
"""

import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean raw sales data: handle nulls, fix dtypes, remove duplicates.
    
    Args:
        df: Raw sales DataFrame
    
    Returns:
        Cleaned DataFrame
    """
    initial_shape = df.shape
    
    # Parse date column if not already datetime
    if not pd.api.types.is_datetime64_any_dtype(df["date"]):
        df["date"] = pd.to_datetime(df["date"])
    
    # Drop duplicates
    df = df.drop_duplicates(subset=["transaction_id"])
    
    # Drop rows with null revenue or date
    df = df.dropna(subset=["revenue", "date"])
    
    # Ensure numeric columns are correct type
    numeric_cols = ["unit_price", "quantity", "discount_pct", "revenue", "cost", "profit"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    
    logger.info(f"Cleaned data: {initial_shape} → {df.shape}")
    return df.reset_index(drop=True)


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add time-based and derived features.
    
    Args:
        df: Cleaned DataFrame
    
    Returns:
        DataFrame with additional feature columns
    """
    df = df.copy()
    
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["month_name"] = df["date"].dt.strftime("%b")
    df["quarter"] = df["date"].dt.quarter
    df["quarter_label"] = "Q" + df["quarter"].astype(str) + " " + df["year"].astype(str)
    df["week"] = df["date"].dt.isocalendar().week.astype(int)
    df["day_of_week"] = df["date"].dt.day_name()
    
    df["profit_margin_pct"] = (df["profit"] / df["revenue"] * 100).round(2)
    df["revenue_per_unit"] = (df["revenue"] / df["quantity"]).round(2)
    
    logger.info("Feature engineering complete")
    return df


def compute_kpis(df: pd.DataFrame) -> dict:
    """
    Compute top-level KPIs for dashboard summary cards.
    
    Args:
        df: Enriched DataFrame
    
    Returns:
        Dictionary of KPI name → value
    """
    total_revenue = df["revenue"].sum()
    total_profit = df["profit"].sum()
    avg_margin = df["profit_margin_pct"].mean()
    total_orders = df["transaction_id"].nunique()
    avg_order_value = df["revenue"].mean()
    
    # YoY growth (comparing latest year vs previous year)
    years = sorted(df["year"].unique())
    yoy_growth = None
    if len(years) >= 2:
        rev_latest = df[df["year"] == years[-1]]["revenue"].sum()
        rev_prev = df[df["year"] == years[-2]]["revenue"].sum()
        yoy_growth = ((rev_latest - rev_prev) / rev_prev * 100).round(2) if rev_prev else None
    
    kpis = {
        "total_revenue": round(total_revenue, 2),
        "total_profit": round(total_profit, 2),
        "avg_profit_margin_pct": round(avg_margin, 2),
        "total_orders": total_orders,
        "avg_order_value": round(avg_order_value, 2),
        "yoy_revenue_growth_pct": yoy_growth
    }
    
    logger.info(f"KPIs computed — Revenue: ${total_revenue:,.2f} | Margin: {avg_margin:.1f}%")
    return kpis


def monthly_revenue_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate monthly revenue and profit."""
    return (
        df.groupby(["year", "month", "month_name"])
        .agg(revenue=("revenue", "sum"), profit=("profit", "sum"), orders=("transaction_id", "count"))
        .reset_index()
        .sort_values(["year", "month"])
    )


def regional_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate revenue and profit by region."""
    return (
        df.groupby("region")
        .agg(revenue=("revenue", "sum"), profit=("profit", "sum"), orders=("transaction_id", "count"))
        .reset_index()
        .sort_values("revenue", ascending=False)
    )


def top_products(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Get top N products by total revenue."""
    return (
        df.groupby(["category", "product"])
        .agg(revenue=("revenue", "sum"), units=("quantity", "sum"))
        .reset_index()
        .sort_values("revenue", ascending=False)
        .head(n)
    )


def sales_rep_leaderboard(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Get top N sales reps by revenue."""
    return (
        df.groupby("sales_rep")
        .agg(revenue=("revenue", "sum"), profit=("profit", "sum"), orders=("transaction_id", "count"))
        .reset_index()
        .sort_values("revenue", ascending=False)
        .head(n)
    )
