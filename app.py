"""
Main application entry point for the Spotify-YouTube Trend Analysis Dashboard.
Initializes and runs the Plotly Dash web application.
"""
import dash
from dash import html
import dash_bootstrap_components as dbc

from config.api_keys import api_keys
from dashboard.layout import create_layout
from dashboard.callbacks import register_callbacks

# Initialize the Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]
)

# Set app title
app.title = "Spotify & YouTube Trend Analysis Dashboard"

# Create and set the layout
app.layout = create_layout()

# Register all callbacks
register_callbacks(app)

# Server configuration
server = app.server

if __name__ == '__main__':
    print("🚀 Starting Spotify-YouTube Trend Analysis Dashboard...")
    print(f"📊 Dashboard will be available at: http://127.0.0.1:{api_keys.port}")
    print("📝 Make sure your .env file contains valid API keys!")

    # Run the app
    app.run(
        debug=api_keys.debug,
        port=api_keys.port,
        host='0.0.0.0'
    )
