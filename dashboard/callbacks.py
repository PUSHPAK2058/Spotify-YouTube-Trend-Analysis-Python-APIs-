"""
Dashboard callbacks module for the Spotify-YouTube trend analysis application.
Handles interactive logic, data processing, and chart updates.
"""
from dash import Input, Output, State, callback_context
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

from data.fetch_spotify import spotify_fetcher
from data.fetch_youtube import youtube_fetcher
from utils.preprocess import clean_spotify_data, clean_youtube_data
from utils.helpers import (
    format_number, calculate_engagement_rate, merge_platform_data,
    get_top_content_by_metric, calculate_trend_metrics
)

def register_callbacks(app):
    """Register all dashboard callbacks."""

    @app.callback(
        [Output('spotify-data-store', 'data'),
         Output('youtube-data-store', 'data')],
        [Input('interval-component', 'n_intervals'),
         Input('region-filter', 'value')]
    )
    def update_data_stores(n_intervals, region):
        """Update data stores with fresh API data."""
        # Fetch Spotify data
        spotify_tracks = spotify_fetcher.get_trending_tracks(limit=50, market=region)
        spotify_df = pd.DataFrame(spotify_tracks) if spotify_tracks else pd.DataFrame()

        # Fetch YouTube data
        youtube_videos = youtube_fetcher.get_trending_videos(
            region_code=region, max_results=50
        )
        youtube_df = pd.DataFrame(youtube_videos) if youtube_videos else pd.DataFrame()

        return spotify_df.to_dict('records'), youtube_df.to_dict('records')

    @app.callback(
        Output('processed-data-store', 'data'),
        [Input('spotify-data-store', 'data'),
         Input('youtube-data-store', 'data'),
         Input('platform-filter', 'value'),
         Input('genre-filter', 'value'),
         Input('time-filter', 'value')]
    )
    def process_data(spotify_data, youtube_data, platform, genre, time_range):
        """Process and filter data based on user selections."""
        # Convert stored data back to DataFrames
        spotify_df = pd.DataFrame(spotify_data) if spotify_data else pd.DataFrame()
        youtube_df = pd.DataFrame(youtube_data) if youtube_data else pd.DataFrame()

        # Clean data
        if not spotify_df.empty:
            spotify_df = clean_spotify_data(spotify_df)
        if not youtube_df.empty:
            youtube_df = clean_youtube_data(youtube_df)

        # Apply platform filter
        if platform == 'spotify':
            combined_df = spotify_df
        elif platform == 'youtube':
            combined_df = youtube_df
        else:
            combined_df = merge_platform_data(spotify_df, youtube_df)

        if combined_df.empty:
            return []

        # Apply genre filter
        if genre != 'all':
            if 'category' in combined_df.columns:
                combined_df = combined_df[combined_df['category'].str.lower() == genre.lower()]

        # Apply time filter
        if time_range != 'all' and 'fetched_at' in combined_df.columns:
            days = int(time_range.replace('D', ''))
            cutoff_date = datetime.now() - timedelta(days=days)
            combined_df['fetched_at'] = pd.to_datetime(combined_df['fetched_at'])
            combined_df = combined_df[combined_df['fetched_at'] >= cutoff_date]

        return combined_df.to_dict('records')

    @app.callback(
        [Output('total-content', 'children'),
         Output('avg-engagement', 'children'),
         Output('top-views', 'children'),
         Output('active-creators', 'children')],
        [Input('processed-data-store', 'data')]
    )
    def update_metric_cards(processed_data):
        """Update metric summary cards."""
        if not processed_data:
            return "0", "0", "0", "0"

        df = pd.DataFrame(processed_data)

        if df.empty:
            return "0", "0", "0", "0"

        # Calculate metrics
        total_content = len(df)

        # Average engagement (handle different metrics for different platforms)
        if 'engagement_score' in df.columns:
            avg_engagement = df['engagement_score'].mean()
            avg_engagement_str = format_number(avg_engagement)
        else:
            avg_engagement_str = "N/A"

        # Top views (YouTube specific)
        if 'view_count' in df.columns:
            top_views = df['view_count'].max()
            top_views_str = format_number(top_views)
        else:
            top_views_str = "N/A"

        # Active creators
        if 'creator' in df.columns:
            active_creators = df['creator'].nunique()
            active_creators_str = str(active_creators)
        else:
            active_creators_str = "N/A"

        return str(total_content), avg_engagement_str, top_views_str, active_creators_str

    @app.callback(
        Output('trending-chart', 'figure'),
        [Input('processed-data-store', 'data'),
         Input('chart-tabs', 'active_tab')]
    )
    def update_trending_chart(processed_data, active_tab):
        """Update trending content chart."""
        if not processed_data or active_tab != 'trending':
            return go.Figure()

        df = pd.DataFrame(processed_data)

        if df.empty:
            return go.Figure()

        # Create trending chart based on available data
        if 'engagement_score' in df.columns and 'content_title' in df.columns:
            # Sort by engagement score
            top_content = get_top_content_by_metric(df, 'engagement_score', 10)

            fig = px.bar(
                top_content,
                x='engagement_score',
                y='content_title',
                orientation='h',
                title='Top Trending Content by Engagement',
                labels={'engagement_score': 'Engagement Score', 'content_title': 'Content Title'},
                color='platform' if 'platform' in top_content.columns else None
            )

            fig.update_layout(
                height=500,
                xaxis_title="Engagement Score",
                yaxis_title="Content Title",
                yaxis={'categoryorder': 'total ascending'}
            )

            return fig

        return go.Figure()

    @app.callback(
        Output('engagement-chart', 'figure'),
        [Input('processed-data-store', 'data'),
         Input('chart-tabs', 'active_tab')]
    )
    def update_engagement_chart(processed_data, active_tab):
        """Update engagement analysis chart."""
        if not processed_data or active_tab != 'engagement':
            return go.Figure()

        df = pd.DataFrame(processed_data)

        if df.empty:
            return go.Figure()

        # Create engagement analysis chart
        if 'view_count' in df.columns and 'like_count' in df.columns:
            # Calculate engagement rate
            df['engagement_rate'] = df.apply(
                lambda row: calculate_engagement_rate(row['like_count'], row['view_count']),
                axis=1
            )

            fig = px.scatter(
                df,
                x='view_count',
                y='engagement_rate',
                size='like_count',
                color='platform' if 'platform' in df.columns else None,
                hover_name='content_title' if 'content_title' in df.columns else 'title',
                title='Engagement Rate vs Views',
                labels={
                    'view_count': 'Views',
                    'engagement_rate': 'Engagement Rate (%)',
                    'like_count': 'Likes'
                }
            )

            fig.update_layout(height=500)
            return fig

        return go.Figure()

    @app.callback(
        Output('comparison-chart', 'figure'),
        [Input('processed-data-store', 'data'),
         Input('chart-tabs', 'active_tab')]
    )
    def update_comparison_chart(processed_data, active_tab):
        """Update cross-platform comparison chart."""
        if not processed_data or active_tab != 'comparison':
            return go.Figure()

        df = pd.DataFrame(processed_data)

        if df.empty or 'platform' not in df.columns:
            return go.Figure()

        # Create comparison chart
        platform_counts = df['platform'].value_counts()

        fig = px.pie(
            values=platform_counts.values,
            names=platform_counts.index,
            title='Content Distribution by Platform',
            hole=0.4
        )

        fig.update_layout(height=500)
        return fig

    @app.callback(
        Output('genre-chart', 'figure'),
        [Input('processed-data-store', 'data'),
         Input('chart-tabs', 'active_tab')]
    )
    def update_genre_chart(processed_data, active_tab):
        """Update genre/category analysis chart."""
        if not processed_data or active_tab != 'genre':
            return go.Figure()

        df = pd.DataFrame(processed_data)

        if df.empty:
            return go.Figure()

        # Create genre/category chart
        if 'category' in df.columns:
            genre_counts = df['category'].value_counts().head(10)

            fig = px.bar(
                x=genre_counts.index,
                y=genre_counts.values,
                title='Content Distribution by Genre/Category',
                labels={'x': 'Genre/Category', 'y': 'Count'}
            )

            fig.update_layout(height=500)
            return fig

        return go.Figure()

    @app.callback(
        Output('content-table', 'data'),
        [Input('processed-data-store', 'data')]
    )
    def update_content_table(processed_data):
        """Update content details table."""
        if not processed_data:
            return []

        df = pd.DataFrame(processed_data)

        if df.empty:
            return []

        # Prepare data for table display
        table_data = []
        for _, row in df.iterrows():
            table_row = {
                'platform': row.get('platform', 'N/A'),
                'content_title': row.get('content_title', row.get('title', 'N/A')),
                'creator': row.get('creator', row.get('channel_title', 'N/A')),
                'engagement_score': row.get('engagement_score', 0),
                'category': row.get('category', 'N/A'),
                'view_count': row.get('view_count', 'N/A'),
                'like_count': row.get('like_count', 'N/A')
            }
            table_data.append(table_row)

        return table_data
