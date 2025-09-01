import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_synthetic_sales_data(num_products=10, num_categories=3, start_date='2020-01-01', end_date='2023-12-31'):
    """
    Generate synthetic monthly sales data for e-commerce.

    Parameters:
    - num_products: Number of products
    - num_categories: Number of categories
    - start_date: Start date for data
    - end_date: End date for data

    Returns:
    - DataFrame with columns: date, product_id, category, sales, price, promotion_flag
    """
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    dates = pd.date_range(start, end, freq='M')

    data = []

    for product_id in range(1, num_products + 1):
        category = f'Category_{np.random.randint(1, num_categories + 1)}'
        base_sales = np.random.randint(100, 1000)  # Base monthly sales
        trend = np.random.uniform(-0.05, 0.05)  # Trend factor
        seasonality = np.random.uniform(0.8, 1.2)  # Seasonal factor

        for date in dates:
            month = date.month
            # Seasonal variation
            seasonal_factor = seasonality + 0.1 * np.sin(2 * np.pi * month / 12)
            # Trend
            time_factor = 1 + trend * ((date - start).days / 365)
            # Random noise
            noise = np.random.normal(0, 0.1)
            # Promotion flag (randomly 10% chance)
            promotion = np.random.choice([0, 1], p=[0.9, 0.1])

            sales = int(base_sales * seasonal_factor * time_factor * (1 + noise) * (1.2 if promotion else 1))
            price = np.random.uniform(10, 500)

            data.append({
                'date': date,
                'product_id': product_id,
                'category': category,
                'sales': max(0, sales),  # Ensure non-negative
                'price': price,
                'promotion_flag': promotion
            })

    df = pd.DataFrame(data)
    return df

if __name__ == '__main__':
    df = generate_synthetic_sales_data()
    df.to_csv('ecommerce_sales_forecasting/data/synthetic_sales_data.csv', index=False)
    print("Synthetic data generated and saved to data/synthetic_sales_data.csv")
