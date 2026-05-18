# Sales Performance Analysis Dashboard

![CI](https://github.com/Saideva0318/sales-performance-dashboard/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-Dash-3F4F75?logo=plotly)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Production--Ready-brightgreen)

> **End-to-end interactive sales analytics dashboard** that ingests 2 years of transactional data, computes KPIs (revenue, YoY growth, profit margin), and surfaces insights through a drill-down Plotly/Dash interface — enabling data-driven decisions for retail and e-commerce teams.

---

## Business Problem

Retail businesses struggle to get a unified, real-time view of sales performance across regions, product lines, and time periods. Sales leaders rely on static spreadsheets that are error-prone and lag behind. This project replaces those with an automated, interactive analytics pipeline delivering actionable KPIs in seconds.

---

## Architecture & Workflow

```
+------------------+     +---------------------+     +----------------------+
|   Raw Data Layer |     |  Processing Layer   |     |  Presentation Layer  |
|                  |     |                     |     |                      |
|  CSV / Mock API  +---->+  data_loader.py     +---->+  Plotly Dash App     |
|  (5,000 records) |     |  transformations.py |     |  KPI Cards           |
|  2 years data    |     |  kpi_calculator.py  |     |  Regional Heatmap    |
+------------------+     |  logging + errors   |     |  Trend Line Charts   |
                         +---------------------+     |  Product Rankings    |
                                                     +----------------------+
                                   |
                         +---------------------+
                         |   Testing Layer     |
                         |  pytest + coverage  |
                         |  GitHub Actions CI  |
                         +---------------------+
```

---

## Key Features

- **Interactive KPI Dashboard** — Revenue, profit margin, YoY growth, top-N products with drill-down
- **Regional Performance Heatmap** — Compare sales across 4 regions with filters
- **Trend Analysis** — Month-over-month and year-over-year sales trend detection
- **Market Basket Insights** — Top product category combinations
- **Automated Data Generation** — Realistic 5,000-record mock dataset with seasonal patterns
- **Production Logging** — Structured logging with rotating file handlers
- **Exception Handling** — Graceful error recovery in data pipeline stages
- **Unit Tested** — pytest with coverage reporting via GitHub Actions

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|------------|----------|
| Language | Python 3.10+ | Core logic |
| Data Processing | Pandas, NumPy | ETL, aggregations |
| Visualization | Plotly, Dash | Interactive dashboard |
| Reporting | Matplotlib, Seaborn | Static charts/exports |
| Testing | pytest, pytest-cov | Unit tests + coverage |
| Linting | flake8, black, isort | Code quality |
| CI/CD | GitHub Actions | Automated testing pipeline |
| Environment | pip, virtualenv | Dependency management |

---

## Project Structure

```
sales-performance-dashboard/
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI pipeline
├── data/
│   ├── raw/                    # Raw CSV datasets
│   └── processed/              # Cleaned & transformed data
├── notebooks/
│   └── exploratory_analysis.ipynb
├── outputs/
│   └── charts/                 # Exported visualizations
├── src/
│   ├── __init__.py
│   ├── data_loader.py          # Data ingestion with logging
│   ├── transformations.py      # Feature engineering & KPIs
│   ├── kpi_calculator.py       # Business metrics engine
│   ├── visualizations.py       # Plotly chart builders
│   └── dashboard.py            # Dash app entry point
├── tests/
│   ├── test_data_loader.py
│   ├── test_transformations.py
│   └── test_kpi_calculator.py
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/Saideva0318/sales-performance-dashboard.git
cd sales-performance-dashboard

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate mock data & run dashboard
python src/data_loader.py
python src/dashboard.py
# Open http://localhost:8050
```

---

## Sample KPIs Generated

| Metric | Value |
|--------|-------|
| Total Revenue | $4.2M (2-year period) |
| YoY Growth | +18.3% |
| Avg Profit Margin | 34.7% |
| Top Region | West Coast |
| Best Product Category | Electronics |

---

## Running Tests

```bash
pytest tests/ -v --cov=src --cov-report=term-missing
```

---

## Skills Demonstrated

`Python` `Pandas` `Plotly` `Dash` `Data Visualization` `KPI Analysis` `ETL` `pytest` `GitHub Actions` `CI/CD` `Data Analytics` `Business Intelligence`

---

## Author

**Saideva** — Data Engineer & Analytics Professional | [GitHub](https://github.com/Saideva0318) | [LinkedIn](https://linkedin.com/in/saideva)

---

*Built with production-quality code standards — clean, tested, and interview-ready.*
