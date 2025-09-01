"""
Configuration module for loading API keys and application settings from environment variables.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class APIKeys:
    """Class to manage API keys and configuration settings."""

    def __init__(self):
        # Spotify API credentials
        self.spotify_client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.spotify_client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

        # YouTube API credentials
        self.youtube_api_key = os.getenv('YOUTUBE_API_KEY')

        # Application settings
        self.debug = os.getenv('DEBUG', 'False').lower() == 'true'
        self.port = int(os.getenv('PORT', 8050))

    def validate_keys(self):
        """Validate that all required API keys are present."""
        missing_keys = []

        if not self.spotify_client_id:
            missing_keys.append('SPOTIFY_CLIENT_ID')
        if not self.spotify_client_secret:
            missing_keys.append('SPOTIFY_CLIENT_SECRET')
        if not self.youtube_api_key:
            missing_keys.append('YOUTUBE_API_KEY')

        if missing_keys:
            raise ValueError(f"Missing required API keys: {', '.join(missing_keys)}")

        return True

# Global instance for easy access
api_keys = APIKeys()

# Validate keys on import
try:
    api_keys.validate_keys()
    print("✅ All API keys loaded successfully!")
except ValueError as e:
    print(f"⚠️  Warning: {e}")
    print("Please update your .env file with the required API keys.")
