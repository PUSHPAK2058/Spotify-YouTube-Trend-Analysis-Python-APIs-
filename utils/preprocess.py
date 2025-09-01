"""
Data preprocessing and transformation utilities.
Includes functions to clean, normalize, and prepare data for visualization.
"""
import pandas as pd

def clean_spotify_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and preprocess Spotify data.

    Args:
        df: Raw Spotify data DataFrame

    Returns:
        Cleaned DataFrame
    """
    df = df.copy()
    # Convert release_date to datetime if exists
    if 'release_date' in df.columns:
        df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

    # Fill missing values
    df.fillna({'genre': 'Unknown', 'artist': 'Unknown'}, inplace=True)

    # Normalize popularity to 0-1 scale
    if 'popularity' in df.columns:
        df['popularity_norm'] = df['popularity'] / 100.0

    return df

def clean_youtube_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and preprocess YouTube data.

    Args:
        df: Raw YouTube data DataFrame

    Returns:
        Cleaned DataFrame
    """
    df = df.copy()
    # Convert published_at to datetime
    if 'published_at' in df.columns:
        df['published_at'] = pd.to_datetime(df['published_at'], errors='coerce')

    # Fill missing values
    df.fillna({'title': 'Unknown', 'channel_title': 'Unknown'}, inplace=True)

    # Normalize view_count and like_count to 0-1 scale
    if 'view_count' in df.columns:
        max_views = df['view_count'].max() if not df['view_count'].empty else 1
        df['view_count_norm'] = df['view_count'] / max_views

    if 'like_count' in df.columns:
        max_likes = df['like_count'].max() if not df['like_count'].empty else 1
        df['like_count_norm'] = df['like_count'] / max_likes

    return df
