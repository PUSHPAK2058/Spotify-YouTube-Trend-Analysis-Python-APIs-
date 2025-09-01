import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error

def calculate_mape(y_true, y_pred):
    """
    Calculate Mean Absolute Percentage Error (MAPE).

    Parameters:
    - y_true: Actual values
    - y_pred: Predicted values

    Returns:
    - MAPE
    """
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

def evaluate_forecast(actual, predicted):
    """
    Evaluate forecast accuracy.

    Parameters:
    - actual: Actual sales values
    - predicted: Predicted sales values

    Returns:
    - Dictionary with metrics
    """
    mae = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    mape = calculate_mape(actual, predicted)

    return {
        'MAE': mae,
        'RMSE': rmse,
        'MAPE': mape
    }

def compare_models(arima_forecasts, prophet_forecasts, test_data):
    """
    Compare ARIMA and Prophet forecasts on test data.

    Parameters:
    - arima_forecasts: Dictionary of ARIMA forecasts
    - prophet_forecasts: Dictionary of Prophet forecasts
    - test_data: Dictionary of test DataFrames

    Returns:
    - DataFrame with comparison
    """
    results = []

    for key in arima_forecasts.keys():
        if key in test_data:
            actual = test_data[key]['sales'].values
            arima_pred = arima_forecasts[key].values
            prophet_pred = prophet_forecasts[key]['yhat'].values[-len(arima_pred):]  # Last predictions

            arima_metrics = evaluate_forecast(actual, arima_pred)
            prophet_metrics = evaluate_forecast(actual, prophet_pred)

            results.append({
                'Product/Category': key,
                'ARIMA_MAE': arima_metrics['MAE'],
                'ARIMA_RMSE': arima_metrics['RMSE'],
                'ARIMA_MAPE': arima_metrics['MAPE'],
                'Prophet_MAE': prophet_metrics['MAE'],
                'Prophet_RMSE': prophet_metrics['RMSE'],
                'Prophet_MAPE': prophet_metrics['MAPE']
            })

    return pd.DataFrame(results)

if __name__ == '__main__':
    # Example usage
    import pandas as pd
    from preprocess import load_data, preprocess_data
    from arima_model import arima_pipeline
    from prophet_model import prophet_pipeline

    df = load_data('ecommerce_sales_forecasting/data/synthetic_sales_data.csv')
    preprocessed = preprocess_data(df)
    arima_forecasts = arima_pipeline(preprocessed)
    prophet_forecasts = prophet_pipeline(preprocessed)
    comparison = compare_models(arima_forecasts, prophet_forecasts, preprocessed)
    print(comparison)
