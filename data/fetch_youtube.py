"""
YouTube API data fetching module.
Handles authentication, data retrieval, and processing for YouTube trending content.
"""
import time
import requests
from typing import List, Dict, Optional
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
from config.api_keys import api_keys

class YouTubeDataFetcher:
    """Class to handle YouTube API data fetching and processing."""

    def __init__(self):
        """Initialize YouTube API client."""
        try:
            self.youtube = build('youtube', 'v3', developerKey=api_keys.youtube_api_key)
            print("✅ YouTube API client initialized successfully!")
        except Exception as e:
            print(f"❌ Failed to initialize YouTube API client: {e}")
            self.youtube = None

    def get_trending_videos(self, region_code: str = 'US', max_results: int = 50,
                           category_id: Optional[str] = None) -> List[Dict]:
        """
        Fetch trending videos from YouTube.

        Args:
            region_code: Region code (e.g., 'US', 'GB', 'DE')
            max_results: Maximum number of videos to fetch (max 50)
            category_id: Video category ID for filtering

        Returns:
            List of trending video dictionaries with metadata
        """
        if not self.youtube:
            return []

        try:
            request = self.youtube.videos().list(
                part='snippet,statistics,contentDetails',
                chart='mostPopular',
                regionCode=region_code,
                maxResults=min(max_results, 50),
                videoCategoryId=category_id
            )

            response = request.execute()

            videos = []
            for item in response.get('items', []):
                snippet = item.get('snippet', {})
                statistics = item.get('statistics', {})
                content_details = item.get('contentDetails', {})

                video_data = {
                    'platform': 'youtube',
                    'video_id': item['id'],
                    'title': snippet.get('title', ''),
                    'channel_title': snippet.get('channelTitle', ''),
                    'description': snippet.get('description', ''),
                    'published_at': snippet.get('publishedAt', ''),
                    'category_id': snippet.get('categoryId', ''),
                    'tags': snippet.get('tags', []),
                    'view_count': int(statistics.get('viewCount', 0)),
                    'like_count': int(statistics.get('likeCount', 0)),
                    'comment_count': int(statistics.get('commentCount', 0)),
                    'duration': content_details.get('duration', ''),
                    'region_code': region_code,
                    'thumbnail_url': snippet.get('thumbnails', {}).get('default', {}).get('url', ''),
                    'video_url': f"https://www.youtube.com/watch?v={item['id']}",
                    'fetched_at': pd.Timestamp.now()
                }
                videos.append(video_data)

            return videos

        except HttpError as e:
            print(f"❌ YouTube API error: {e}")
            return []
        except Exception as e:
            print(f"❌ Error fetching YouTube trending videos: {e}")
            return []

    def search_videos(self, query: str, max_results: int = 25,
                     order: str = 'relevance', region_code: str = 'US') -> List[Dict]:
        """
        Search for videos based on a query.

        Args:
            query: Search query string
            max_results: Maximum number of results (max 50)
            order: Sort order ('relevance', 'viewCount', 'rating', 'date')
            region_code: Region code for search

        Returns:
            List of video dictionaries matching the search query
        """
        if not self.youtube:
            return []

        try:
            request = self.youtube.search().list(
                part='snippet',
                q=query,
                type='video',
                order=order,
                regionCode=region_code,
                maxResults=min(max_results, 50)
            )

            response = request.execute()

            video_ids = [item['id']['videoId'] for item in response.get('items', [])
                        if item['id']['kind'] == 'youtube#video']

            # Get detailed statistics for the videos
            if video_ids:
                stats_request = self.youtube.videos().list(
                    part='statistics,contentDetails',
                    id=','.join(video_ids)
                )
                stats_response = stats_request.execute()

                videos = []
                for item, stats_item in zip(response.get('items', []), stats_response.get('items', [])):
                    snippet = item.get('snippet', {})
                    statistics = stats_item.get('statistics', {})
                    content_details = stats_item.get('contentDetails', {})

                    video_data = {
                        'platform': 'youtube',
                        'video_id': item['id']['videoId'],
                        'title': snippet.get('title', ''),
                        'channel_title': snippet.get('channelTitle', ''),
                        'description': snippet.get('description', ''),
                        'published_at': snippet.get('publishedAt', ''),
                        'view_count': int(statistics.get('viewCount', 0)),
                        'like_count': int(statistics.get('likeCount', 0)),
                        'comment_count': int(statistics.get('commentCount', 0)),
                        'duration': content_details.get('duration', ''),
                        'region_code': region_code,
                        'thumbnail_url': snippet.get('thumbnails', {}).get('default', {}).get('url', ''),
                        'video_url': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                        'fetched_at': pd.Timestamp.now()
                    }
                    videos.append(video_data)

                return videos

        except HttpError as e:
            print(f"❌ YouTube API error: {e}")
            return []
        except Exception as e:
            print(f"❌ Error searching YouTube videos: {e}")
            return []

        return []

    def get_channel_stats(self, channel_id: str) -> Optional[Dict]:
        """
        Get statistics for a specific YouTube channel.

        Args:
            channel_id: YouTube channel ID

        Returns:
            Dictionary with channel statistics
        """
        if not self.youtube:
            return None

        try:
            request = self.youtube.channels().list(
                part='snippet,statistics',
                id=channel_id
            )

            response = request.execute()

            if response.get('items'):
                channel = response['items'][0]
                snippet = channel.get('snippet', {})
                statistics = channel.get('statistics', {})

                return {
                    'platform': 'youtube',
                    'channel_id': channel_id,
                    'channel_title': snippet.get('title', ''),
                    'description': snippet.get('description', ''),
                    'subscriber_count': int(statistics.get('subscriberCount', 0)),
                    'video_count': int(statistics.get('videoCount', 0)),
                    'view_count': int(statistics.get('viewCount', 0)),
                    'published_at': snippet.get('publishedAt', ''),
                    'country': snippet.get('country', ''),
                    'fetched_at': pd.Timestamp.now()
                }

        except HttpError as e:
            print(f"❌ YouTube API error: {e}")
        except Exception as e:
            print(f"❌ Error fetching channel stats for {channel_id}: {e}")

        return None

# Global instance for easy access
youtube_fetcher = YouTubeDataFetcher()
