import matplotlib.pyplot as plt
import pandas as pd

def plot_sales_forecast(actual, arima_forecast, prophet_forecast, title='Sales Forecast'):
    """
    Plot actual sales and forecasts.

    Parameters:
    - actual: DataFrame with actual sales
    - arima_forecast: Series with ARIMA forecast
    - prophet_forecast: DataFrame with Prophet forecast
    - title: Plot title
    """
    plt.figure(figsize=(12, 6))

    # Plot actual
    plt.plot(actual.index, actual['sales'], label='Actual Sales', color='blue')

    # Plot ARIMA forecast
    forecast_index = pd.date_range(start=actual.index[-1] + pd.Timedelta(days=1), periods=len(arima_forecast), freq='M')
    plt.plot(forecast_index, arima_forecast, label='ARIMA Forecast', color='red', linestyle='--')

    # Plot Prophet forecast
    plt.plot(prophet_forecast['ds'], prophet_forecast['yhat'], label='Prophet Forecast', color='green', linestyle='--')

    # Add confidence intervals for Prophet
    plt.fill_between(prophet_forecast['ds'], prophet_forecast['yhat_lower'], prophet_forecast['yhat_upper'], color='green', alpha=0.2)

    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Sales')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_multiple_forecasts(train_data, test_data, arima_forecasts, prophet_forecasts):
    """
    Plot forecasts for multiple products/categories with train/test split.

    Parameters:
    - train_data: Dictionary of train DataFrames
    - test_data: Dictionary of test DataFrames
    - arima_forecasts: Dictionary of ARIMA forecasts
    - prophet_forecasts: Dictionary of Prophet forecasts
    """
    num_items = len(train_data)
    fig, axes = plt.subplots(num_items, 1, figsize=(12, 6 * num_items))

    if num_items == 1:
        axes = [axes]

    for i, (key, train) in enumerate(train_data.items()):
        ax = axes[i]
        # Plot train data
        ax.plot(train.index, train['sales'], label='Train', color='blue')
        # Plot test data
        test = test_data[key]
        ax.plot(test.index, test['sales'], label='Test', color='orange')

        # ARIMA forecast
        forecast_index = pd.date_range(start=test.index[0], periods=len(arima_forecasts[key]), freq='M')
        ax.plot(forecast_index, arima_forecasts[key], label='ARIMA Forecast', color='red', linestyle='--')

        # Prophet forecast
        prophet_df = prophet_forecasts[key]
        future_forecast = prophet_df[prophet_df['ds'] >= test.index[0]]
        ax.plot(future_forecast['ds'], future_forecast['yhat'], label='Prophet Forecast', color='green', linestyle='--')
        ax.fill_between(future_forecast['ds'], future_forecast['yhat_lower'], future_forecast['yhat_upper'], color='green', alpha=0.2)

        ax.set_title(f'Sales Forecast for {key}')
        ax.legend()
        ax.grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    # Example usage
    from preprocess import load_data, preprocess_data
    from arima_model import arima_pipeline
    from prophet_model import prophet_pipeline

    df = load_data('ecommerce_sales_forecasting/data/synthetic_sales_data.csv')
    preprocessed = preprocess_data(df)
    arima_forecasts = arima_pipeline(preprocessed)
    prophet_forecasts = prophet_pipeline(preprocessed)

    # Plot for first item
    first_key = list(preprocessed.keys())[0]
    plot_sales_forecast(preprocessed[first_key], arima_forecasts[first_key], prophet_forecasts[first_key], title=f'Sales Forecast for {first_key}')
