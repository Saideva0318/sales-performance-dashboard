# Sales Performance Analysis Dashboard

## Problem Statement
Organizations struggle to gain real-time visibility into sales performance across regions, products, and time periods. This project builds an interactive analytics dashboard to track KPIs, identify top performers, and uncover revenue trends.

## Approach
1. Load and clean synthetic sales data (CSV)
2. Engineer features: monthly revenue, YoY growth, region-wise breakdown
3. Visualize KPIs using Plotly/Matplotlib dashboards
4. Export summary report as HTML + static charts

## Tech Stack
- **Python** 3.10+
- **Pandas** — data manipulation
- **Plotly** — interactive visualizations
- **Matplotlib / Seaborn** — static charts
- **Jupyter Notebook** — exploratory analysis
- **CSV** — sample dataset

## Project Structure
```
sales-performance-dashboard/
├── data/
│   ├── raw/
│   │   └── sales_data.csv
│   └── processed/
│       └── sales_cleaned.csv
├── notebooks/
│   └── exploratory_analysis.ipynb
├── src/
│   ├── data_loader.py
│   ├── data_processor.py
│   └── visualizer.py
├── outputs/
│   └── dashboard.html
├── requirements.txt
└── README.md
```

## How to Run
```bash
pip install -r requirements.txt
python src/data_processor.py
python src/visualizer.py
```

## Key Insights Extracted
- Monthly and quarterly revenue trends
- Top 5 products by revenue
- Region-wise sales distribution
- Sales rep performance ranking
- YoY and MoM growth rates
