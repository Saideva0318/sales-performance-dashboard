"""
Dash Dashboard Entrypoint
Interactive sales performance dashboard using Plotly Dash.
"""

import dash
from dash import dcc, html, Input, Output
import plotly.express as px

from data_loader import load_data
from transformations import clean_data, engineer_features, compute_kpis, monthly_revenue_trend, regional_performance, top_products, sales_rep_leaderboard
from visualizations import revenue_trend_chart, regional_bar_chart, top_products_chart, profit_margin_scatter

# ─── Load & Prepare Data ──────────────────────────────────────────────────────
raw_df = load_data()
df = engineer_features(clean_data(raw_df))
kpis = compute_kpis(df)
monthly_df = monthly_revenue_trend(df)
regional_df = regional_performance(df)
products_df = top_products(df)

# ─── App Layout ───────────────────────────────────────────────────────────────
app = dash.Dash(__name__, title="Sales Performance Dashboard")

app.layout = html.Div([
    html.H1("📊 Sales Performance Dashboard", style={"textAlign": "center", "color": "#2c3e50", "padding": "20px"}),

    # KPI Cards
    html.Div([
        html.Div([html.H4("Total Revenue"), html.H2(f"${kpis['total_revenue']:,.0f}")], className="kpi-card", style={"background": "#3498db", "color": "white", "padding": "20px", "margin": "10px", "borderRadius": "8px", "textAlign": "center", "flex": "1"}),
        html.Div([html.H4("Total Profit"), html.H2(f"${kpis['total_profit']:,.0f}")], className="kpi-card", style={"background": "#2ecc71", "color": "white", "padding": "20px", "margin": "10px", "borderRadius": "8px", "textAlign": "center", "flex": "1"}),
        html.Div([html.H4("Avg Margin"), html.H2(f"{kpis['avg_profit_margin_pct']:.1f}%")], className="kpi-card", style={"background": "#9b59b6", "color": "white", "padding": "20px", "margin": "10px", "borderRadius": "8px", "textAlign": "center", "flex": "1"}),
        html.Div([html.H4("Total Orders"), html.H2(f"{kpis['total_orders']:,}")], className="kpi-card", style={"background": "#e74c3c", "color": "white", "padding": "20px", "margin": "10px", "borderRadius": "8px", "textAlign": "center", "flex": "1"}),
        html.Div([html.H4("YoY Growth"), html.H2(f"{kpis['yoy_revenue_growth_pct']:+.1f}%" if kpis['yoy_revenue_growth_pct'] else "N/A")], className="kpi-card", style={"background": "#f39c12", "color": "white", "padding": "20px", "margin": "10px", "borderRadius": "8px", "textAlign": "center", "flex": "1"}),
    ], style={"display": "flex", "flexWrap": "wrap", "margin": "0 20px"}),

    # Charts Row 1
    html.Div([
        dcc.Graph(figure=revenue_trend_chart(monthly_df), style={"flex": "2"}),
        dcc.Graph(figure=regional_bar_chart(regional_df), style={"flex": "1"}),
    ], style={"display": "flex", "margin": "10px"}),

    # Charts Row 2
    html.Div([
        dcc.Graph(figure=top_products_chart(products_df), style={"flex": "1"}),
        dcc.Graph(figure=profit_margin_scatter(df), style={"flex": "1"}),
    ], style={"display": "flex", "margin": "10px"}),

], style={"fontFamily": "Arial, sans-serif", "backgroundColor": "#f5f6fa"})


if __name__ == "__main__":
    app.run(debug=True)
