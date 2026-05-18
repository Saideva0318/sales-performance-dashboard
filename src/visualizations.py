"""Visualization functions for Sales Performance Dashboard."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os


def plot_monthly_revenue(df: pd.DataFrame) -> go.Figure:
    """Line chart of monthly revenue trend."""
    monthly = df.groupby('year_month')['revenue'].sum().reset_index()
    monthly.columns = ['Month', 'Revenue']
    fig = px.line(
        monthly, x='Month', y='Revenue',
        title='Monthly Revenue Trend',
        markers=True,
        color_discrete_sequence=['#2196F3']
    )
    fig.update_layout(template='plotly_white', hovermode='x unified')
    return fig


def plot_revenue_by_region(df: pd.DataFrame) -> go.Figure:
    """Bar chart of revenue by region."""
    regional = df.groupby('region')['revenue'].sum().reset_index().sort_values('revenue', ascending=False)
    fig = px.bar(
        regional, x='region', y='revenue',
        title='Total Revenue by Region',
        color='revenue',
        color_continuous_scale='Blues',
        text_auto='.2s'
    )
    fig.update_layout(template='plotly_white', showlegend=False)
    return fig


def plot_category_breakdown(df: pd.DataFrame) -> go.Figure:
    """Donut chart of revenue by product category."""
    cat_rev = df.groupby('category')['revenue'].sum().reset_index()
    fig = px.pie(
        cat_rev, names='category', values='revenue',
        title='Revenue Share by Category',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig


def plot_top_products(df: pd.DataFrame, n: int = 10) -> go.Figure:
    """Horizontal bar chart of top N products by revenue."""
    top = df.groupby('product')['revenue'].sum().nlargest(n).reset_index()
    top.columns = ['Product', 'Revenue']
    fig = px.bar(
        top, x='Revenue', y='Product',
        orientation='h',
        title=f'Top {n} Products by Revenue',
        color='Revenue',
        color_continuous_scale='Viridis',
        text_auto='.2s'
    )
    fig.update_layout(template='plotly_white', yaxis={'categoryorder': 'total ascending'})
    return fig


def plot_channel_performance(df: pd.DataFrame) -> go.Figure:
    """Grouped bar chart of revenue by channel and quarter."""
    channel_q = df.groupby(['quarter', 'channel'])['revenue'].sum().reset_index()
    channel_q['quarter'] = 'Q' + channel_q['quarter'].astype(str)
    fig = px.bar(
        channel_q, x='quarter', y='revenue',
        color='channel',
        barmode='group',
        title='Revenue by Sales Channel and Quarter',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_layout(template='plotly_white')
    return fig


def save_charts(df: pd.DataFrame, output_dir: str = 'outputs/charts') -> None:
    """Generate and save all charts as HTML files."""
    os.makedirs(output_dir, exist_ok=True)
    charts = {
        'monthly_revenue': plot_monthly_revenue(df),
        'revenue_by_region': plot_revenue_by_region(df),
        'category_breakdown': plot_category_breakdown(df),
        'top_products': plot_top_products(df),
        'channel_performance': plot_channel_performance(df)
    }
    for name, fig in charts.items():
        path = os.path.join(output_dir, f'{name}.html')
        fig.write_html(path)
        print(f"Saved: {path}")
    print(f"\n✅ All {len(charts)} charts saved to {output_dir}/")


if __name__ == '__main__':
    df = pd.read_csv('data/processed/sales_processed.csv', parse_dates=['date'])
    save_charts(df)
