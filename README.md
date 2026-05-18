# 📊 Sales Performance Analysis Dashboard

## Problem Statement
Retail businesses often struggle to gain timely insights from fragmented sales data spread across regions, products, and time periods. Without a unified analytical view, decision-makers miss opportunities to optimize revenue, identify underperforming segments, and forecast future sales trends.

## Approach
1. **Data Generation** — Synthetic sales dataset simulating 2 years of retail transactions across regions and product categories
2. **EDA & Cleaning** — Handle missing values, outliers, and data type normalization
3. **Feature Engineering** — Month-over-month growth, rolling averages, revenue per unit
4. **Visualization** — Interactive Plotly/Dash dashboard with KPI cards, trend lines, regional heatmaps
5. **Insights** — Top-performing products, seasonal trends, regional breakdowns

## Tech Stack
| Tool | Purpose |
|------|---------|
| Python 3.10+ | Core language |
| Pandas | Data manipulation |
| NumPy | Numerical operations |
| Plotly / Dash | Interactive dashboards |
| Matplotlib / Seaborn | Static visualizations |
| Jupyter Notebook | Exploratory analysis |
| SQLite | Local data storage |

## Project Structure
```
sales-performance-dashboard/
├── data/
│   ├── raw/                  # Raw generated CSV data
│   └── processed/            # Cleaned and transformed data
├── notebooks/
│   └── 01_eda_analysis.ipynb # Exploratory Data Analysis
├── src/
│   ├── data_generator.py     # Synthetic data creation
│   ├── data_processor.py     # Cleaning & feature engineering
│   ├── visualizations.py     # Chart generation functions
│   └── dashboard.py          # Dash app entry point
├── outputs/
│   └── charts/               # Exported chart images
├── requirements.txt
└── README.md
```

## Getting Started
```bash
# Clone the repo
git clone https://github.com/Saideva0318/sales-performance-dashboard.git
cd sales-performance-dashboard

# Install dependencies
pip install -r requirements.txt

# Generate mock data
python src/data_generator.py

# Run data processing
python src/data_processor.py

# Launch interactive dashboard
python src/dashboard.py
# Open http://127.0.0.1:8050 in your browser
```

## Key Metrics Tracked
- Total Revenue, Units Sold, Average Order Value
- Month-over-Month (MoM) and Year-over-Year (YoY) growth
- Top 10 products by revenue
- Regional sales heatmap
- Seasonal trend forecasting
