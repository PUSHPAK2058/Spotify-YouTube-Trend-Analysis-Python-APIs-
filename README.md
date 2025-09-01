# 🎵 Spotify-YouTube-Trend-Analysis-Python-APIs-

## 4. Spotify/YouTube Trend Analysis | Python, APIs, Plotly Dash

Built interactive visual dashboards analyzing trending content via Spotify and YouTube APIs; surfaced top-viewed content and engagement rate trends, uncovering data insights for content strategy.

This project analyzes music and video trends using Python, Spotify and YouTube APIs, and Plotly Dash. It fetches real-time data, processes it for insights, and visualizes popularity patterns, genre shifts, and artist performance through an interactive dashboard with tabbed views.

## ✨ Features

- **📊 Interactive Dashboard**: Tabbed interface with multiple visualization views
- **🎵 Spotify Integration**: Fetch trending tracks, artist popularity, and genre analysis
- **📺 YouTube Integration**: Get trending videos, channel statistics, and engagement metrics
- **🔄 Cross-Platform Comparison**: Dual-axis charts comparing Spotify and YouTube data
- **🎛️ Advanced Filters**: Filter by genre, region, time range, and platform
- **📈 Real-time Updates**: Auto-refresh data every 5 minutes
- **📱 Responsive Design**: Works on desktop and mobile devices

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Spotify Developer Account
- Google Cloud Console Account (for YouTube API)

### 1. Clone and Setup

```bash
git clone <repository-url>
cd spotify-youtube-trends
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Get API Keys

#### Spotify API Setup
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Copy your `Client ID` and `Client Secret`

#### YouTube API Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable YouTube Data API v3
4. Create credentials (API Key)
5. Copy your API Key

### 5. Configure Environment

Update the `.env` file with your API keys:

```env
# Spotify API Credentials
SPOTIFY_CLIENT_ID=your_spotify_client_id_here
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here

# YouTube API Credentials
YOUTUBE_API_KEY=your_youtube_api_key_here

# Application Settings
DEBUG=True
PORT=8050
```

### 6. Run the Application

```bash
python app.py
```

Open your browser and navigate to `http://127.0.0.1:8050`

## 📁 Project Structure

```
spotify-youtube-trends/
│
├── README.md                  # Project documentation
├── .env                       # Environment variables (API keys)
├── requirements.txt           # Python dependencies
├── app.py                     # Main application entry point
│
├── config/
│   └── api_keys.py            # API key management
│
├── data/
│   ├── fetch_spotify.py       # Spotify API integration
│   └── fetch_youtube.py       # YouTube API integration
│
├── dashboard/
│   ├── layout.py              # Dashboard UI components
│   └── callbacks.py           # Interactive logic and data processing
│
├── utils/
│   ├── preprocess.py          # Data cleaning and transformation
│   └── helpers.py             # Utility functions
│
└── TODO.md                    # Development progress tracker
```

## 🎯 Dashboard Features

### 📊 Trending Content Tab
- Top trending tracks and videos
- Engagement score visualization
- Platform-specific rankings

### 📈 Engagement Analysis Tab
- Engagement rate vs views scatter plot
- Like-to-view ratio analysis
- Content performance metrics

### 🔄 Cross-Platform Comparison Tab
- Platform distribution pie chart
- Comparative engagement metrics
- Unified content analysis

### 🎵 Genre/Category Analysis Tab
- Genre popularity distribution
- Category-based filtering
- Trend analysis by content type

### 🎛️ Interactive Filters
- **Platform**: All, Spotify, or YouTube
- **Genre**: Pop, Rock, Hip-Hop, Electronic, etc.
- **Region**: US, UK, Germany, France, Canada
- **Time Range**: 1D, 7D, 30D, 90D

## 🔧 API Integration Details

### Spotify API
- **Endpoints Used**:
  - Search playlists and tracks
  - Get track audio features
  - Retrieve artist information
- **Rate Limits**: 1000 requests per hour
- **Data Points**: Popularity, followers, genres, release dates

### YouTube API
- **Endpoints Used**:
  - Trending videos by region
  - Video statistics and metadata
  - Channel information
- **Rate Limits**: 10,000 units per day
- **Data Points**: Views, likes, comments, duration, categories

## 🛠️ Development

### Adding New Features
1. Update `TODO.md` with new tasks
2. Implement new functions in appropriate modules
3. Add UI components to `dashboard/layout.py`
4. Register callbacks in `dashboard/callbacks.py`
5. Test thoroughly with different data scenarios

### Code Quality
- Follow PEP 8 style guidelines
- Add docstrings to all functions
- Handle API errors gracefully
- Validate data before processing

## 📊 Data Processing

### Preprocessing Steps
1. **Data Cleaning**: Remove null values, standardize formats
2. **Normalization**: Scale metrics for comparison
3. **Merging**: Combine Spotify and YouTube data
4. **Filtering**: Apply user-selected criteria

### Metrics Calculated
- Engagement Rate: (likes/views) × 100
- Popularity Score: Platform-specific ranking
- Trend Velocity: Rate of metric change over time

## 🚨 Troubleshooting

### Common Issues

**API Key Errors**
```
ValueError: Missing required API keys
```
- Check your `.env` file
- Ensure API keys are correctly formatted
- Verify API quotas haven't been exceeded

**Import Errors**
```
ModuleNotFoundError: No module named 'spotipy'
```
- Run `pip install -r requirements.txt`
- Ensure you're in the correct virtual environment

**Port Already in Use**
```
OSError: [Errno 48] Address already in use
```
- Change the PORT in `.env` file
- Kill existing processes on the port

### Debug Mode
Set `DEBUG=True` in `.env` for detailed error messages and auto-reload.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Spotify for providing comprehensive music data
- YouTube for video trending information
- Plotly Dash for the amazing visualization framework
- The open-source community for incredible tools and libraries

---

**Happy Analyzing! 🎉**

