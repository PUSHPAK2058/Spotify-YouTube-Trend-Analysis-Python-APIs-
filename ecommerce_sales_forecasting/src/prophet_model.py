import pandas as pd
from prophet import Prophet

def train_prophet(df):
    """
    Train Prophet model on sales data.

    Parameters:
    - df: DataFrame with 'date' and 'sales' columns

    Returns:
    - Trained Prophet model
    """
    df_prophet = df.reset_index()[['date', 'sales']].rename(columns={'date': 'ds', 'sales': 'y'})
    model = Prophet()
    model.fit(df_prophet)
    return model

def forecast_prophet(model, periods=12):
    """
    Forecast using Prophet model.

    Parameters:
    - model: Trained Prophet model
    - periods: Number of months to forecast

    Returns:
    - DataFrame with forecast
    """
    future = model.make_future_dataframe(periods=periods, freq='M')
    forecast = model.predict(future)
    return forecast

def prophet_pipeline(train_data_dict, forecast_steps=12):
    """
    Full Prophet pipeline for multiple series with train/test split.

    Parameters:
    - train_data_dict: Dictionary of train DataFrames
    - forecast_steps: Number of months to forecast

    Returns:
    - Dictionary of forecasts
    """
    forecasts = {}

    for key, df in train_data_dict.items():
        model = train_prophet(df)
        forecast = forecast_prophet(model, periods=forecast_steps)
        forecasts[key] = forecast

    return forecasts

if __name__ == '__main__':
    # Example usage
    from preprocess import load_data, preprocess_data
    df = load_data('ecommerce_sales_forecasting/data/synthetic_sales_data.csv')
    preprocessed = preprocess_data(df)
    forecasts = prophet_pipeline(preprocessed)
    print("Prophet forecasting completed.")
