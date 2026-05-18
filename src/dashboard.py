"""Interactive Dash Dashboard for Sales Performance Analysis."""

import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
from visualizations import (
    plot_monthly_revenue, plot_revenue_by_region,
    plot_category_breakdown, plot_top_products, plot_channel_performance
)

# Load data
df = pd.read_csv('data/processed/sales_processed.csv', parse_dates=['date'])

# KPI Calculations
total_revenue = df['revenue'].sum()
total_orders = len(df)
avg_order_value = df['revenue'].mean()
total_units = df['quantity'].sum()

app = dash.Dash(__name__, title='Sales Performance Dashboard')

app.layout = html.Div([
    html.H1('📊 Sales Performance Dashboard',
            style={'textAlign': 'center', 'color': '#1565C0', 'fontFamily': 'Arial'}),

    # KPI Cards
    html.Div([
        html.Div([html.H3('Total Revenue'), html.H2(f'${total_revenue:,.0f}')],
                 className='kpi-card', style={'background': '#E3F2FD', 'padding': '20px',
                                              'borderRadius': '10px', 'textAlign': 'center', 'flex': 1, 'margin': '10px'}),
        html.Div([html.H3('Total Orders'), html.H2(f'{total_orders:,}')],
                 className='kpi-card', style={'background': '#E8F5E9', 'padding': '20px',
                                              'borderRadius': '10px', 'textAlign': 'center', 'flex': 1, 'margin': '10px'}),
        html.Div([html.H3('Avg Order Value'), html.H2(f'${avg_order_value:.2f}')],
                 className='kpi-card', style={'background': '#FFF3E0', 'padding': '20px',
                                              'borderRadius': '10px', 'textAlign': 'center', 'flex': 1, 'margin': '10px'}),
        html.Div([html.H3('Units Sold'), html.H2(f'{total_units:,}')],
                 className='kpi-card', style={'background': '#F3E5F5', 'padding': '20px',
                                              'borderRadius': '10px', 'textAlign': 'center', 'flex': 1, 'margin': '10px'}),
    ], style={'display': 'flex', 'justifyContent': 'space-around', 'padding': '20px'}),

    # Filters
    html.Div([
        html.Label('Filter by Region:'),
        dcc.Dropdown(
            id='region-filter',
            options=[{'label': 'All Regions', 'value': 'All'}] +
                    [{'label': r, 'value': r} for r in df['region'].unique()],
            value='All', clearable=False, style={'width': '300px'}
        ),
        html.Label('Filter by Category:', style={'marginLeft': '20px'}),
        dcc.Dropdown(
            id='category-filter',
            options=[{'label': 'All Categories', 'value': 'All'}] +
                    [{'label': c, 'value': c} for c in df['category'].unique()],
            value='All', clearable=False, style={'width': '300px', 'marginLeft': '10px'}
        ),
    ], style={'display': 'flex', 'alignItems': 'center', 'padding': '10px 20px'}),

    # Charts
    dcc.Graph(id='monthly-trend'),
    html.Div([
        dcc.Graph(id='region-chart', style={'flex': 1}),
        dcc.Graph(id='category-chart', style={'flex': 1}),
    ], style={'display': 'flex'}),
    dcc.Graph(id='top-products'),
    dcc.Graph(id='channel-chart'),
], style={'fontFamily': 'Arial', 'backgroundColor': '#F9FAFB', 'padding': '20px'})


@app.callback(
    [Output('monthly-trend', 'figure'),
     Output('region-chart', 'figure'),
     Output('category-chart', 'figure'),
     Output('top-products', 'figure'),
     Output('channel-chart', 'figure')],
    [Input('region-filter', 'value'),
     Input('category-filter', 'value')]
)
def update_charts(region, category):
    filtered = df.copy()
    if region != 'All':
        filtered = filtered[filtered['region'] == region]
    if category != 'All':
        filtered = filtered[filtered['category'] == category]
    return (
        plot_monthly_revenue(filtered),
        plot_revenue_by_region(filtered),
        plot_category_breakdown(filtered),
        plot_top_products(filtered),
        plot_channel_performance(filtered)
    )


if __name__ == '__main__':
    print("🚀 Starting Sales Performance Dashboard...")
    print("📊 Open http://127.0.0.1:8050 in your browser")
    app.run(debug=True)
