"""
Spotify API data fetching module.
Handles authentication, data retrieval, and processing for Spotify trending content.
"""
import time
import requests
from typing import List, Dict, Optional
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from config.api_keys import api_keys

class SpotifyDataFetcher:
    """Class to handle Spotify API data fetching and processing."""

    def __init__(self):
        """Initialize Spotify API client."""
        try:
            client_credentials_manager = SpotifyClientCredentials(
                client_id=api_keys.spotify_client_id,
                client_secret=api_keys.spotify_client_secret
            )
            self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
            self.sp.trace = False
            print("✅ Spotify API client initialized successfully!")
        except Exception as e:
            print(f"❌ Failed to initialize Spotify API client: {e}")
            self.sp = None

    def get_top_tracks_by_genre(self, genre: str = 'pop', limit: int = 50,
                               market: str = 'US') -> List[Dict]:
        """
        Fetch top tracks for a specific genre.

        Args:
            genre: Music genre (e.g., 'pop', 'rock', 'hip-hop')
            limit: Number of tracks to fetch (max 50)
            market: Country market code (e.g., 'US', 'GB', 'DE')

        Returns:
            List of track dictionaries with metadata
        """
        if not self.sp:
            return []

        try:
            # Search for playlists related to the genre
            query = f"{genre} top tracks"
            results = self.sp.search(q=query, type='playlist', limit=5, market=market)

            tracks = []
            for playlist in results['playlists']['items']:
                if playlist:
                    playlist_tracks = self.sp.playlist_tracks(
                        playlist['id'], limit=min(limit//5, 10), market=market
                    )

                    for item in playlist_tracks['items']:
                        if item and item['track']:
                            track = item['track']
                            track_data = {
                                'platform': 'spotify',
                                'track_id': track['id'],
                                'track_name': track['name'],
                                'artist': track['artists'][0]['name'] if track['artists'] else 'Unknown',
                                'album': track['album']['name'] if track['album'] else 'Unknown',
                                'genre': genre,
                                'popularity': track['popularity'],
                                'duration_ms': track['duration_ms'],
                                'external_url': track['external_urls']['spotify'],
                                'release_date': track['album']['release_date'] if track['album'] else None,
                                'market': market,
                                'fetched_at': pd.Timestamp.now()
                            }
                            tracks.append(track_data)

            return tracks[:limit]

        except Exception as e:
            print(f"❌ Error fetching Spotify tracks for genre {genre}: {e}")
            return []

    def get_artist_popularity(self, artist_name: str, market: str = 'US') -> Optional[Dict]:
        """
        Get popularity metrics for a specific artist.

        Args:
            artist_name: Name of the artist
            market: Country market code

        Returns:
            Dictionary with artist popularity data
        """
        if not self.sp:
            return None

        try:
            results = self.sp.search(q=artist_name, type='artist', limit=1, market=market)

            if results['artists']['items']:
                artist = results['artists']['items'][0]
                return {
                    'platform': 'spotify',
                    'artist_id': artist['id'],
                    'artist_name': artist['name'],
                    'popularity': artist['popularity'],
                    'followers': artist['followers']['total'],
                    'genres': artist['genres'],
                    'market': market,
                    'fetched_at': pd.Timestamp.now()
                }

        except Exception as e:
            print(f"❌ Error fetching artist data for {artist_name}: {e}")

        return None

    def get_trending_tracks(self, limit: int = 50, market: str = 'US') -> List[Dict]:
        """
        Fetch currently trending/popular tracks.

        Args:
            limit: Number of tracks to fetch
            market: Country market code

        Returns:
            List of trending track dictionaries
        """
        if not self.sp:
            return []

        try:
            # Get tracks from Spotify's "Top 50" playlists or similar
            results = self.sp.search(q="Top 50", type='playlist', limit=5, market=market)

            tracks = []
            for playlist in results['playlists']['items']:
                if playlist and 'Top' in playlist['name']:
                    playlist_tracks = self.sp.playlist_tracks(
                        playlist['id'], limit=min(limit//5, 10), market=market
                    )

                    for item in playlist_tracks['items']:
                        if item and item['track']:
                            track = item['track']
                            track_data = {
                                'platform': 'spotify',
                                'track_id': track['id'],
                                'track_name': track['name'],
                                'artist': track['artists'][0]['name'] if track['artists'] else 'Unknown',
                                'popularity': track['popularity'],
                                'duration_ms': track['duration_ms'],
                                'external_url': track['external_urls']['spotify'],
                                'market': market,
                                'fetched_at': pd.Timestamp.now()
                            }
                            tracks.append(track_data)

            return tracks[:limit]

        except Exception as e:
            print(f"❌ Error fetching trending tracks: {e}")
            return []

# Global instance for easy access
spotify_fetcher = SpotifyDataFetcher()
