"""
visualizer.py — Build interactive Plotly dashboard from processed sales data.
"""
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import logging
from pathlib import Path
from data_processor import clean_data, engineer_features, compute_monthly_revenue, compute_region_summary, compute_top_products
from data_loader import load_sales_data

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

OUTPUT_PATH = Path("outputs/dashboard.html")


def build_dashboard(df: pd.DataFrame) -> go.Figure:
    monthly  = compute_monthly_revenue(df)
    region   = compute_region_summary(df)
    products = compute_top_products(df, n=8)

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Monthly Revenue Trend", "Revenue by Region",
                        "Top Products by Revenue", "Quarterly Revenue Mix"),
        specs=[[{"type": "scatter"}, {"type": "bar"}],
               [{"type": "bar"},     {"type": "pie"}]]
    )

    fig.add_trace(go.Scatter(x=monthly["year_month"], y=monthly["monthly_revenue"],
                             mode="lines+markers", name="Monthly Revenue",
                             line=dict(color="#01696f", width=2)), row=1, col=1)

    fig.add_trace(go.Bar(x=region["region"], y=region["total_revenue"],
                         name="Region Revenue", marker_color="#4f98a3"), row=1, col=2)

    fig.add_trace(go.Bar(x=products["product"], y=products["total_revenue"],
                         name="Product Revenue", marker_color="#437a22"), row=2, col=1)

    quarterly = df.groupby("quarter")["revenue"].sum()
    fig.add_trace(go.Pie(labels=[f"Q{q}" for q in quarterly.index],
                         values=quarterly.values, name="Quarterly"), row=2, col=2)

    fig.update_layout(title_text="Sales Performance Dashboard",
                      title_font_size=22, height=800,
                      template="plotly_white", showlegend=False)
    return fig


if __name__ == "__main__":
    df = load_sales_data()
    df = clean_data(df)
    df = engineer_features(df)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig = build_dashboard(df)
    fig.write_html(str(OUTPUT_PATH))
    logger.info(f"Dashboard saved to {OUTPUT_PATH}")
