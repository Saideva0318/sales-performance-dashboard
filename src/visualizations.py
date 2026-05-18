"""
Visualizations Module
Plotly chart generation functions for the sales dashboard.
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

COLOR_PALETTE = px.colors.qualitative.Plotly
COLOR_SCALE = "Blues"


def revenue_trend_chart(monthly_df: pd.DataFrame) -> go.Figure:
    """Line chart of monthly revenue trend with year comparison."""
    fig = px.line(
        monthly_df,
        x="month",
        y="revenue",
        color="year",
        markers=True,
        title="Monthly Revenue Trend by Year",
        labels={"month": "Month", "revenue": "Revenue ($)", "year": "Year"},
        color_discrete_sequence=COLOR_PALETTE
    )
    fig.update_layout(
        plot_bgcolor="white",
        hovermode="x unified",
        yaxis_tickprefix="$",
        yaxis_tickformat=",.0f"
    )
    return fig


def regional_bar_chart(regional_df: pd.DataFrame) -> go.Figure:
    """Horizontal bar chart for regional revenue performance."""
    fig = px.bar(
        regional_df,
        x="revenue",
        y="region",
        orientation="h",
        color="revenue",
        color_continuous_scale=COLOR_SCALE,
        title="Revenue by Region",
        labels={"revenue": "Total Revenue ($)", "region": "Region"},
        text_auto=".2s"
    )
    fig.update_layout(plot_bgcolor="white", coloraxis_showscale=False)
    return fig


def top_products_chart(products_df: pd.DataFrame) -> go.Figure:
    """Bar chart for top products by revenue."""
    fig = px.bar(
        products_df,
        x="revenue",
        y="product",
        orientation="h",
        color="category",
        title="Top 10 Products by Revenue",
        labels={"revenue": "Revenue ($)", "product": "Product"},
        text_auto=".2s"
    )
    fig.update_layout(plot_bgcolor="white", yaxis={"categoryorder": "total ascending"})
    return fig


def profit_margin_scatter(df: pd.DataFrame) -> go.Figure:
    """Scatter plot of revenue vs profit margin by category."""
    category_agg = (
        df.groupby("category")
        .agg(revenue=("revenue", "sum"), profit_margin=("profit_margin_pct", "mean"), orders=("transaction_id", "count"))
        .reset_index()
    )
    fig = px.scatter(
        category_agg,
        x="revenue",
        y="profit_margin",
        size="orders",
        color="category",
        title="Revenue vs Profit Margin by Category",
        labels={"revenue": "Total Revenue ($)", "profit_margin": "Avg Profit Margin (%)"},
        hover_data=["orders"]
    )
    fig.update_layout(plot_bgcolor="white")
    return fig
