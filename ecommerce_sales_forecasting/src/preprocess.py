import pandas as pd
from sklearn.preprocessing import StandardScaler

def load_data(filepath):
    """
    Load sales data from CSV.

    Parameters:
    - filepath: Path to the CSV file

    Returns:
    - DataFrame
    """
    df = pd.read_csv(filepath, parse_dates=['date'])
    return df

def preprocess_data(df, group_by='product_id', test_size=12):
    """
    Preprocess the data for forecasting, including train/test split.

    Parameters:
    - df: DataFrame with sales data
    - group_by: Column to group by (e.g., 'product_id' or 'category')
    - test_size: Number of months for test set

    Returns:
    - Dictionary of train DataFrames, test DataFrames
    """
    train_data = {}
    test_data = {}
    groups = df.groupby(group_by)

    for name, group in groups:
        # Sort by date
        group = group.sort_values('date')
        # Set date as index
        group.set_index('date', inplace=True)
        # Resample to monthly if needed (assuming already monthly)
        group = group.resample('M').sum()  # Aggregate if multiple entries per month
        # Select relevant columns
        group = group[['sales']]

        # Split into train and test
        train = group.iloc[:-test_size]
        test = group.iloc[-test_size:]

        train_data[name] = train
        test_data[name] = test

    return train_data, test_data

def scale_data(data_dict):
    """
    Scale the sales data.

    Parameters:
    - data_dict: Dictionary of DataFrames

    Returns:
    - Dictionary of scaled DataFrames, scaler objects
    """
    scaled = {}
    scalers = {}

    for key, df in data_dict.items():
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(df[['sales']])
        scaled_df = df.copy()
        scaled_df['sales_scaled'] = scaled_data
        scaled[key] = scaled_df
        scalers[key] = scaler

    return scaled, scalers

if __name__ == '__main__':
    # Example usage
    df = load_data('ecommerce_sales_forecasting/data/synthetic_sales_data.csv')
    preprocessed = preprocess_data(df)
    scaled, scalers = scale_data(preprocessed)
    print("Preprocessing completed.")
