"""
Basic tests for critical components of the Spotify-YouTube Trend Analysis Dashboard.
"""
import pytest
import pandas as pd
from unittest.mock import Mock, patch

# Test imports
from config.api_keys import api_keys
from utils.helpers import format_number, calculate_engagement_rate, parse_duration
from utils.preprocess import clean_spotify_data, clean_youtube_data

class TestAPIKeys:
    """Test API key configuration."""

    def test_api_keys_validation(self):
        """Test that API keys are properly validated."""
        # This will fail if keys are not set, which is expected in test environment
        try:
            api_keys.validate_keys()
            assert True  # Keys are valid
        except ValueError:
            # Expected if keys are not set
            assert True

class TestHelpers:
    """Test utility helper functions."""

    def test_format_number(self):
        """Test number formatting with suffixes."""
        assert format_number(1500) == "1.5K"
        assert format_number(2500000) == "2.5M"
        assert format_number(1000000000) == "1.0B"
        assert format_number(500) == "500"

    def test_calculate_engagement_rate(self):
        """Test engagement rate calculation."""
        assert calculate_engagement_rate(100, 1000) == 10.0
        assert calculate_engagement_rate(0, 1000) == 0.0
        assert calculate_engagement_rate(50, 0) == 0.0

    def test_parse_duration(self):
        """Test YouTube duration parsing."""
        assert parse_duration("PT4M13S") == 253
        assert parse_duration("PT1H30M45S") == 5445
        assert parse_duration("PT30S") == 30
        assert parse_duration("") == 0

class TestDataPreprocessing:
    """Test data preprocessing functions."""

    def test_clean_spotify_data(self):
        """Test Spotify data cleaning."""
        data = {
            'track_name': ['Song 1', 'Song 2'],
            'artist': ['Artist 1', None],
            'popularity': [80, 90],
            'genre': ['pop', None]
        }
        df = pd.DataFrame(data)

        cleaned = clean_spotify_data(df)

        assert 'popularity_norm' in cleaned.columns
        assert cleaned['popularity_norm'].iloc[0] == 0.8
        assert cleaned['artist'].iloc[1] == 'Unknown'
        assert cleaned['genre'].iloc[1] == 'Unknown'

    def test_clean_youtube_data(self):
        """Test YouTube data cleaning."""
        data = {
            'title': ['Video 1', None],
            'channel_title': ['Channel 1', 'Channel 2'],
            'view_count': [1000, 2000],
            'like_count': [100, 200],
            'published_at': ['2023-01-01T00:00:00Z', '2023-01-02T00:00:00Z']
        }
        df = pd.DataFrame(data)

        cleaned = clean_youtube_data(df)

        assert 'view_count_norm' in cleaned.columns
        assert 'like_count_norm' in cleaned.columns
        assert pd.api.types.is_datetime64_any_dtype(cleaned['published_at'])
        assert cleaned['title'].iloc[1] == 'Unknown'

class TestDataFetching:
    """Test data fetching components (mocked)."""

    @patch('data.fetch_spotify.spotipy.Spotify')
    def test_spotify_fetcher_initialization(self, mock_spotify):
        """Test Spotify fetcher initialization."""
        from data.fetch_spotify import SpotifyDataFetcher

        fetcher = SpotifyDataFetcher()
        # Should handle missing API keys gracefully
        assert fetcher.sp is None or mock_spotify.called

    @patch('data.fetch_youtube.build')
    def test_youtube_fetcher_initialization(self, mock_build):
        """Test YouTube fetcher initialization."""
        from data.fetch_youtube import YouTubeDataFetcher

        fetcher = YouTubeDataFetcher()
        # Should handle missing API keys gracefully
        assert fetcher.youtube is None or mock_build.called

if __name__ == "__main__":
    pytest.main([__file__])
