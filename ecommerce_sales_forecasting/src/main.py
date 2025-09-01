import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from data.generate_data import generate_synthetic_sales_data
from src.preprocess import load_data, preprocess_data
from src.arima_model import arima_pipeline
from src.prophet_model import prophet_pipeline
from src.evaluate import compare_models
from src.visualize import plot_multiple_forecasts

def main():
    """
    Main pipeline for E-Commerce Sales Forecasting.
    """
    print("Starting E-Commerce Sales Forecasting Pipeline...")

    # Step 1: Generate synthetic data
    print("Generating synthetic sales data...")
    df = generate_synthetic_sales_data()
    df.to_csv('data/synthetic_sales_data.csv', index=False)

    # Step 2: Preprocess data
    print("Preprocessing data...")
    train_data, test_data = preprocess_data(df)

    # Step 3: Train and forecast with ARIMA
    print("Running ARIMA forecasting...")
    arima_forecasts = arima_pipeline(train_data)

    # Step 4: Train and forecast with Prophet
    print("Running Prophet forecasting...")
    prophet_forecasts = prophet_pipeline(train_data)

    # Step 5: Evaluate models
    print("Evaluating models...")
    comparison = compare_models(arima_forecasts, prophet_forecasts, test_data)
    print("Model Comparison:")
    print(comparison)

    # Step 6: Visualize results
    print("Visualizing forecasts...")
    plot_multiple_forecasts(train_data, test_data, arima_forecasts, prophet_forecasts)

    print("Pipeline completed successfully!")

if __name__ == '__main__':
    main()
