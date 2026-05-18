"""Data Processing & Feature Engineering for Sales Performance Dashboard."""

import pandas as pd
import numpy as np
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class SalesDataProcessor:
    """Handles cleaning, transformation, and feature engineering of raw sales data."""

    def __init__(self, input_path: str = 'data/raw/sales_data.csv',
                 output_path: str = 'data/processed/sales_processed.csv'):
        self.input_path = input_path
        self.output_path = output_path
        self.df = None

    def load(self) -> 'SalesDataProcessor':
        logger.info(f"Loading data from {self.input_path}")
        self.df = pd.read_csv(self.input_path, parse_dates=['date'])
        logger.info(f"Loaded {len(self.df)} rows")
        return self

    def clean(self) -> 'SalesDataProcessor':
        logger.info("Cleaning data...")
        initial = len(self.df)
        self.df.dropna(subset=['order_id', 'date', 'revenue'], inplace=True)
        self.df = self.df[self.df['revenue'] > 0]
        self.df = self.df[self.df['quantity'] > 0]
        self.df.drop_duplicates(subset='order_id', inplace=True)
        logger.info(f"Removed {initial - len(self.df)} invalid rows. Remaining: {len(self.df)}")
        return self

    def engineer_features(self) -> 'SalesDataProcessor':
        logger.info("Engineering features...")
        self.df['year'] = self.df['date'].dt.year
        self.df['month'] = self.df['date'].dt.month
        self.df['month_name'] = self.df['date'].dt.strftime('%b')
        self.df['quarter'] = self.df['date'].dt.quarter
        self.df['week'] = self.df['date'].dt.isocalendar().week.astype(int)
        self.df['day_of_week'] = self.df['date'].dt.day_name()
        self.df['year_month'] = self.df['date'].dt.to_period('M').astype(str)
        self.df['revenue_per_unit'] = (self.df['revenue'] / self.df['quantity']).round(2)
        self.df['is_discounted'] = self.df['discount_pct'] > 0
        return self

    def add_monthly_growth(self) -> 'SalesDataProcessor':
        logger.info("Calculating monthly growth rates...")
        monthly = self.df.groupby('year_month')['revenue'].sum().reset_index()
        monthly.columns = ['year_month', 'monthly_revenue']
        monthly['mom_growth_pct'] = monthly['monthly_revenue'].pct_change() * 100
        monthly['mom_growth_pct'] = monthly['mom_growth_pct'].round(2)
        self.df = self.df.merge(monthly, on='year_month', how='left')
        return self

    def save(self) -> None:
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        self.df.to_csv(self.output_path, index=False)
        logger.info(f"Processed data saved to {self.output_path}")

    def summary(self) -> None:
        print("\n=== Sales Data Summary ===")
        print(f"Total Records: {len(self.df):,}")
        print(f"Total Revenue: ${self.df['revenue'].sum():,.2f}")
        print(f"Avg Order Value: ${self.df['revenue'].mean():.2f}")
        print(f"Date Range: {self.df['date'].min().date()} to {self.df['date'].max().date()}")
        print(f"\nRevenue by Region:")
        print(self.df.groupby('region')['revenue'].sum().sort_values(ascending=False).apply(lambda x: f'${x:,.2f}'))
        print(f"\nRevenue by Category:")
        print(self.df.groupby('category')['revenue'].sum().sort_values(ascending=False).apply(lambda x: f'${x:,.2f}'))


if __name__ == '__main__':
    processor = SalesDataProcessor()
    processor.load().clean().engineer_features().add_monthly_growth().save()
    processor.summary()
    print("\n✅ Data processing complete!")
