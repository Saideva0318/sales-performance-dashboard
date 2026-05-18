# 📊 Sales Performance Analysis Dashboard

## Problem Statement
Retail businesses often struggle to get a unified view of sales performance across regions, products, and time periods. This project builds an interactive sales analytics dashboard to identify trends, top performers, and revenue drivers.

## Approach
1. **Extract** – Load mock sales data (CSV) covering 2 years of transactions
2. **Transform** – Clean data, engineer features (MoM growth, regional aggregates, product rankings)
3. **Analyze** – KPI calculations: revenue, profit margin, YoY growth, top-N products
4. **Visualize** – Interactive Plotly dashboard with drill-down capabilities

## Tech Stack
| Layer | Technology |
|-------|------------|
| Language | Python 3.10+ |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly, Dash |
| Reporting | Matplotlib, Seaborn |
| Environment | pip / virtualenv |

## Project Structure
```
sales-performance-dashboard/
├── data/
│   ├── raw/                  # Raw CSV datasets
│   └── processed/            # Cleaned & transformed data
├── notebooks/
│   └── exploratory_analysis.ipynb
├── src/
│   ├── __init__.py
│   ├── data_loader.py        # Data ingestion utilities
│   ├── transformations.py    # Feature engineering & KPIs
│   ├── visualizations.py     # Chart generation functions
│   └── dashboard.py          # Dash app entrypoint
├── tests/
│   └── test_transformations.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Getting Started
```bash
git clone https://github.com/Saideva0318/sales-performance-dashboard.git
cd sales-performance-dashboard
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Generate mock data
python src/data_loader.py

# Launch dashboard
python src/dashboard.py
```
Open `http://127.0.0.1:8050` in your browser.

## Key Metrics
- **Total Revenue** by region, product category, and time period
- **Profit Margin %** analysis with threshold alerts
- **Month-over-Month** and **Year-over-Year** growth rates
- **Top 10 Products** by revenue and volume
- **Sales Rep Performance** leaderboard

## Sample Output
- Revenue trend line chart (monthly)
- Regional heatmap
- Product category bar chart
- KPI summary cards

## License
MIT
