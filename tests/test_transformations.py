"""
Unit Tests — Transformations Module
"""

import pytest
import pandas as pd
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from data_loader import generate_mock_sales_data
from transformations import clean_data, engineer_features, compute_kpis


@pytest.fixture
def sample_df():
    return generate_mock_sales_data(n_records=500)


def test_generate_data_shape(sample_df):
    assert sample_df.shape[0] == 500
    assert "transaction_id" in sample_df.columns
    assert "revenue" in sample_df.columns


def test_clean_data_no_nulls(sample_df):
    cleaned = clean_data(sample_df)
    assert cleaned["revenue"].isnull().sum() == 0
    assert cleaned["date"].isnull().sum() == 0


def test_engineer_features_columns(sample_df):
    enriched = engineer_features(clean_data(sample_df))
    for col in ["year", "month", "quarter", "profit_margin_pct"]:
        assert col in enriched.columns


def test_kpi_total_revenue_positive(sample_df):
    enriched = engineer_features(clean_data(sample_df))
    kpis = compute_kpis(enriched)
    assert kpis["total_revenue"] > 0
    assert kpis["total_orders"] > 0


def test_no_negative_revenue(sample_df):
    cleaned = clean_data(sample_df)
    assert (cleaned["revenue"] >= 0).all()
