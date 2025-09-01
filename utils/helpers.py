"""
Helper utilities for the Spotify-YouTube trend analysis dashboard.
Includes functions for data manipulation, formatting, and common operations.
"""
import pandas as pd
from typing import Dict, List, Any
import re

def format_number(num: float) -> str:
    """
    Format large numbers with appropriate suffixes (K, M, B).

    Args:
        num: Number to format

    Returns:
        Formatted string
    """
    if num >= 1e9:
        return f"{num/1e9:.1f}B"
    elif num >= 1e6:
        return f"{num/1e6:.1f}M"
    elif num >= 1e3:
        return f"{num/1e3:.1f}K"
    else:
        return str(int(num))

def calculate_engagement_rate(likes: int, views: int) -> float:
    """
    Calculate engagement rate as (likes / views) * 100.

    Args:
        likes: Number of likes
        views: Number of views

    Returns:
        Engagement rate as percentage
    """
    if views == 0:
        return 0.0
    return (likes / views) * 100

def parse_duration(duration: str) -> int:
    """
    Parse YouTube duration string (PT4M13S) to seconds.

    Args:
        duration: YouTube duration string

    Returns:
        Duration in seconds
    """
    if not duration or not isinstance(duration, str):
        return 0

    # Remove 'PT' prefix
    duration = duration.replace('PT', '')

    hours = 0
    minutes = 0
    seconds = 0

    # Extract hours, minutes, seconds
    hour_match = re.search(r'(\d+)H', duration)
    if hour_match:
        hours = int(hour_match.group(1))

    minute_match = re.search(r'(\d+)M', duration)
    if minute_match:
        minutes = int(minute_match.group(1))

    second_match = re.search(r'(\d+)S', duration)
    if second_match:
        seconds = int(second_match.group(1))

    return hours * 3600 + minutes * 60 + seconds

def format_duration(seconds: int) -> str:
    """
    Format duration in seconds to human-readable string.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted duration string
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes}:{seconds:02d}"

def merge_platform_data(spotify_df: pd.DataFrame, youtube_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merge Spotify and YouTube data for cross-platform analysis.

    Args:
        spotify_df: Spotify data DataFrame
        youtube_df: YouTube data DataFrame

    Returns:
        Merged DataFrame with platform comparison data
    """
    # Standardize column names for merging
    spotify_cols = {
        'track_name': 'content_title',
        'artist': 'creator',
        'popularity': 'engagement_score',
        'genre': 'category'
    }

    youtube_cols = {
        'title': 'content_title',
        'channel_title': 'creator',
        'view_count': 'engagement_score',
        'category_id': 'category'
    }

    spotify_merged = spotify_df.rename(columns=spotify_cols)
    youtube_merged = youtube_df.rename(columns=youtube_cols)

    # Add platform identifier
    spotify_merged['platform'] = 'Spotify'
    youtube_merged['platform'] = 'YouTube'

    # Select common columns for comparison
    common_cols = ['content_title', 'creator', 'engagement_score', 'category', 'platform', 'fetched_at']

    spotify_common = spotify_merged[common_cols]
    youtube_common = youtube_merged[common_cols]

    # Combine datasets
    combined_df = pd.concat([spotify_common, youtube_common], ignore_index=True)

    return combined_df

def get_top_content_by_metric(df: pd.DataFrame, metric: str, n: int = 10) -> pd.DataFrame:
    """
    Get top N content items by a specific metric.

    Args:
        df: DataFrame with content data
        metric: Column name to sort by
        n: Number of top items to return

    Returns:
        DataFrame with top N items
    """
    if metric not in df.columns:
        raise ValueError(f"Metric '{metric}' not found in DataFrame columns")

    return df.nlargest(n, metric).reset_index(drop=True)

def calculate_trend_metrics(df: pd.DataFrame, date_col: str = 'fetched_at') -> Dict[str, Any]:
    """
    Calculate trend metrics from time-series data.

    Args:
        df: DataFrame with time-series data
        date_col: Name of the date column

    Returns:
        Dictionary with trend metrics
    """
    if date_col not in df.columns:
        return {}

    df_sorted = df.sort_values(date_col)

    metrics = {
        'total_records': len(df),
        'date_range': {
            'start': df_sorted[date_col].min(),
            'end': df_sorted[date_col].max()
        },
        'avg_engagement': df.get('engagement_score', pd.Series()).mean(),
        'max_engagement': df.get('engagement_score', pd.Series()).max(),
        'unique_creators': df.get('creator', pd.Series()).nunique()
    }

    return metrics
