-- =============================================================
-- Sales Performance Analytics - Advanced SQL Queries
-- Database: PostgreSQL 14+
-- Author: Saideva0318
-- Description: Production-grade analytics queries for sales KPIs
-- =============================================================

-- ---------------------------------------------------------------
-- TABLE SCHEMA
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sales (
    sale_id       SERIAL PRIMARY KEY,
    sale_date     DATE NOT NULL,
    region        VARCHAR(50) NOT NULL,
    product       VARCHAR(100) NOT NULL,
    category      VARCHAR(50) NOT NULL,
    quantity      INTEGER NOT NULL,
    unit_price    NUMERIC(10, 2) NOT NULL,
    discount      NUMERIC(5, 2) DEFAULT 0,
    revenue       NUMERIC(12, 2) GENERATED ALWAYS AS (quantity * unit_price * (1 - discount)) STORED,
    cost          NUMERIC(12, 2) NOT NULL,
    profit        NUMERIC(12, 2) GENERATED ALWAYS AS (quantity * unit_price * (1 - discount) - cost) STORED,
    sales_rep     VARCHAR(100),
    customer_id   INTEGER
);

CREATE INDEX idx_sales_date ON sales(sale_date);
CREATE INDEX idx_sales_region ON sales(region);
CREATE INDEX idx_sales_category ON sales(category);

-- ---------------------------------------------------------------
-- QUERY 1: Year-over-Year Revenue Growth by Region
-- Window function: LAG to compare current vs previous year
-- ---------------------------------------------------------------
WITH yearly_revenue AS (
    SELECT
        region,
        EXTRACT(YEAR FROM sale_date)::INT AS year,
        SUM(revenue) AS total_revenue
    FROM sales
    GROUP BY region, EXTRACT(YEAR FROM sale_date)
),
growth_calc AS (
    SELECT
        region,
        year,
        total_revenue,
        LAG(total_revenue) OVER (PARTITION BY region ORDER BY year) AS prev_year_revenue
    FROM yearly_revenue
)
SELECT
    region,
    year,
    ROUND(total_revenue, 2) AS total_revenue,
    ROUND(prev_year_revenue, 2) AS prev_year_revenue,
    ROUND(
        ((total_revenue - prev_year_revenue) / NULLIF(prev_year_revenue, 0)) * 100, 2
    ) AS yoy_growth_pct
FROM growth_calc
WHERE prev_year_revenue IS NOT NULL
ORDER BY region, year;

-- ---------------------------------------------------------------
-- QUERY 2: Rolling 3-Month Revenue (Moving Average)
-- Window function: AVG OVER with ROWS BETWEEN
-- ---------------------------------------------------------------
SELECT
    DATE_TRUNC('month', sale_date) AS month,
    region,
    SUM(revenue) AS monthly_revenue,
    ROUND(
        AVG(SUM(revenue)) OVER (
            PARTITION BY region
            ORDER BY DATE_TRUNC('month', sale_date)
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ), 2
    ) AS rolling_3m_avg
FROM sales
GROUP BY DATE_TRUNC('month', sale_date), region
ORDER BY region, month;

-- ---------------------------------------------------------------
-- QUERY 3: Top 10 Products by Revenue with Rank
-- Window function: DENSE_RANK
-- ---------------------------------------------------------------
WITH product_totals AS (
    SELECT
        product,
        category,
        SUM(revenue) AS total_revenue,
        SUM(profit) AS total_profit,
        SUM(quantity) AS total_units,
        ROUND(AVG(unit_price), 2) AS avg_price,
        ROUND(SUM(profit) / NULLIF(SUM(revenue), 0) * 100, 2) AS profit_margin_pct
    FROM sales
    GROUP BY product, category
)
SELECT
    DENSE_RANK() OVER (ORDER BY total_revenue DESC) AS revenue_rank,
    product,
    category,
    ROUND(total_revenue, 2) AS total_revenue,
    ROUND(total_profit, 2) AS total_profit,
    total_units,
    avg_price,
    profit_margin_pct
FROM product_totals
LIMIT 10;

-- ---------------------------------------------------------------
-- QUERY 4: Customer Lifetime Value (CLTV) Segmentation
-- CTE + CASE for RFM-style bucketing
-- ---------------------------------------------------------------
WITH customer_metrics AS (
    SELECT
        customer_id,
        COUNT(DISTINCT sale_id) AS purchase_count,
        SUM(revenue) AS lifetime_revenue,
        MAX(sale_date) AS last_purchase_date,
        CURRENT_DATE - MAX(sale_date) AS days_since_last_purchase
    FROM sales
    WHERE customer_id IS NOT NULL
    GROUP BY customer_id
)
SELECT
    customer_id,
    purchase_count,
    ROUND(lifetime_revenue, 2) AS lifetime_revenue,
    last_purchase_date,
    days_since_last_purchase,
    CASE
        WHEN lifetime_revenue >= 10000 AND days_since_last_purchase <= 30 THEN 'Champions'
        WHEN lifetime_revenue >= 5000  AND days_since_last_purchase <= 60 THEN 'Loyal Customers'
        WHEN lifetime_revenue >= 1000  AND days_since_last_purchase <= 90 THEN 'Potential Loyalists'
        WHEN days_since_last_purchase > 180 THEN 'At Risk'
        ELSE 'New Customers'
    END AS customer_segment
FROM customer_metrics
ORDER BY lifetime_revenue DESC;

-- ---------------------------------------------------------------
-- QUERY 5: Monthly Cohort Revenue Analysis
-- Identifies revenue by first-purchase cohort month
-- ---------------------------------------------------------------
WITH first_purchase AS (
    SELECT
        customer_id,
        DATE_TRUNC('month', MIN(sale_date)) AS cohort_month
    FROM sales
    WHERE customer_id IS NOT NULL
    GROUP BY customer_id
),
cohort_data AS (
    SELECT
        fp.cohort_month,
        DATE_TRUNC('month', s.sale_date) AS purchase_month,
        SUM(s.revenue) AS revenue
    FROM sales s
    JOIN first_purchase fp ON s.customer_id = fp.customer_id
    GROUP BY fp.cohort_month, DATE_TRUNC('month', s.sale_date)
)
SELECT
    cohort_month,
    purchase_month,
    EXTRACT(MONTH FROM AGE(purchase_month, cohort_month)) AS months_since_first_purchase,
    ROUND(revenue, 2) AS cohort_revenue
FROM cohort_data
ORDER BY cohort_month, purchase_month;

-- ---------------------------------------------------------------
-- QUERY 6: Sales Rep Performance Scorecard
-- Percentile ranking using NTILE
-- ---------------------------------------------------------------
SELECT
    sales_rep,
    COUNT(DISTINCT sale_id) AS total_sales,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(AVG(revenue), 2) AS avg_deal_size,
    ROUND(SUM(profit) / NULLIF(SUM(revenue), 0) * 100, 2) AS avg_margin_pct,
    NTILE(4) OVER (ORDER BY SUM(revenue) DESC) AS performance_quartile
FROM sales
WHERE sales_rep IS NOT NULL
GROUP BY sales_rep
ORDER BY total_revenue DESC;
