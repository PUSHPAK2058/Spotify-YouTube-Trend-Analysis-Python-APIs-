import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
import warnings
warnings.filterwarnings('ignore')

def check_stationarity(series):
    """
    Check if the time series is stationary using Augmented Dickey-Fuller test.

    Parameters:
    - series: Time series data

    Returns:
    - Boolean: True if stationary
    """
    result = adfuller(series)
    return result[1] < 0.05  # p-value < 0.05

def make_stationary(series, max_diff=2):
    """
    Make the series stationary by differencing.

    Parameters:
    - series: Time series data
    - max_diff: Maximum differencing order

    Returns:
    - Differenced series, differencing order
    """
    d = 0
    while not check_stationarity(series) and d < max_diff:
        series = series.diff().dropna()
        d += 1
    return series, d

def train_arima(series, order=(1,1,1)):
    """
    Train ARIMA model.

    Parameters:
    - series: Time series data
    - order: (p, d, q) order

    Returns:
    - Fitted model
    """
    model = ARIMA(series, order=order)
    fitted_model = model.fit()
    return fitted_model

def forecast_arima(model, steps=12):
    """
    Forecast using ARIMA model.

    Parameters:
    - model: Fitted ARIMA model
    - steps: Number of steps to forecast

    Returns:
    - Forecasted values
    """
    forecast = model.forecast(steps=steps)
    return forecast

def arima_pipeline(train_data_dict, forecast_steps=12):
    """
    Full ARIMA pipeline for multiple series with train/test split.

    Parameters:
    - train_data_dict: Dictionary of train DataFrames
    - forecast_steps: Number of months to forecast

    Returns:
    - Dictionary of forecasts
    """
    forecasts = {}

    for key, df in train_data_dict.items():
        series = df['sales']
        # Make stationary
        stationary_series, d = make_stationary(series)
        # Train model (simple order, can be optimized)
        order = (1, d, 1)
        model = train_arima(stationary_series, order=order)
        # Forecast
        forecast = forecast_arima(model, steps=forecast_steps)
        forecasts[key] = forecast

    return forecasts

if __name__ == '__main__':
    # Example usage
    from preprocess import load_data, preprocess_data
    df = load_data('ecommerce_sales_forecasting/data/synthetic_sales_data.csv')
    preprocessed = preprocess_data(df)
    forecasts = arima_pipeline(preprocessed)
    print("ARIMA forecasting completed.")
