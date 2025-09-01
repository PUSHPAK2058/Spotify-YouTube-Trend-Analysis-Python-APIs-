"""
Dashboard layout module for the Spotify-YouTube trend analysis application.
Defines the UI components, charts, and interactive elements.
"""
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

def create_header():
    """Create the dashboard header."""
    return dbc.Row([
        dbc.Col([
            html.H1("🎵 Spotify & YouTube Trend Analysis Dashboard",
                   className="text-center mb-4",
                   style={'color': '#1DB954'}),
            html.P("Analyze trending content, engagement metrics, and cross-platform comparisons",
                  className="text-center text-muted mb-4")
        ], width=12)
    ])

def create_filters():
    """Create filter controls for the dashboard."""
    return dbc.Row([
        dbc.Col([
            html.Label("Platform", className="fw-bold"),
            dcc.Dropdown(
                id='platform-filter',
                options=[
                    {'label': 'All Platforms', 'value': 'all'},
                    {'label': 'Spotify', 'value': 'spotify'},
                    {'label': 'YouTube', 'value': 'youtube'}
                ],
                value='all',
                clearable=False,
                className="mb-3"
            )
        ], md=3),

        dbc.Col([
            html.Label("Genre/Category", className="fw-bold"),
            dcc.Dropdown(
                id='genre-filter',
                options=[
                    {'label': 'All Genres', 'value': 'all'},
                    {'label': 'Pop', 'value': 'pop'},
                    {'label': 'Rock', 'value': 'rock'},
                    {'label': 'Hip-Hop', 'value': 'hip-hop'},
                    {'label': 'Electronic', 'value': 'electronic'},
                    {'label': 'Music', 'value': 'music'}  # YouTube category
                ],
                value='all',
                clearable=False,
                className="mb-3"
            )
        ], md=3),

        dbc.Col([
            html.Label("Region", className="fw-bold"),
            dcc.Dropdown(
                id='region-filter',
                options=[
                    {'label': 'United States', 'value': 'US'},
                    {'label': 'United Kingdom', 'value': 'GB'},
                    {'label': 'Germany', 'value': 'DE'},
                    {'label': 'France', 'value': 'FR'},
                    {'label': 'Canada', 'value': 'CA'}
                ],
                value='US',
                clearable=False,
                className="mb-3"
            )
        ], md=3),

        dbc.Col([
            html.Label("Time Range", className="fw-bold"),
            dcc.Dropdown(
                id='time-filter',
                options=[
                    {'label': 'Last 24 Hours', 'value': '1D'},
                    {'label': 'Last 7 Days', 'value': '7D'},
                    {'label': 'Last 30 Days', 'value': '30D'},
                    {'label': 'Last 90 Days', 'value': '90D'}
                ],
                value='7D',
                clearable=False,
                className="mb-3"
            )
        ], md=3)
    ], className="mb-4")

def create_metric_cards():
    """Create metric summary cards."""
    return dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Total Content", className="card-title text-center"),
                    html.H2(id="total-content", className="text-center text-primary")
                ])
            ], className="mb-3")
        ], md=3),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Avg Engagement", className="card-title text-center"),
                    html.H2(id="avg-engagement", className="text-center text-success")
                ])
            ], className="mb-3")
        ], md=3),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Top Views", className="card-title text-center"),
                    html.H2(id="top-views", className="text-center text-info")
                ])
            ], className="mb-3")
        ], md=3),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Active Creators", className="card-title text-center"),
                    html.H2(id="active-creators", className="text-center text-warning")
                ])
            ], className="mb-3")
        ], md=3)
    ])

def create_charts_section():
    """Create the main charts section with tabs."""
    return dbc.Row([
        dbc.Col([
            dbc.Tabs([
                dbc.Tab([
                    dcc.Graph(id='trending-chart', style={'height': '500px'})
                ], label="Trending Content", tab_id="trending"),

                dbc.Tab([
                    dcc.Graph(id='engagement-chart', style={'height': '500px'})
                ], label="Engagement Analysis", tab_id="engagement"),

                dbc.Tab([
                    dcc.Graph(id='comparison-chart', style={'height': '500px'})
                ], label="Cross-Platform Comparison", tab_id="comparison"),

                dbc.Tab([
                    dcc.Graph(id='genre-chart', style={'height': '500px'})
                ], label="Genre/Category Analysis", tab_id="genre")
            ], id="chart-tabs", active_tab="trending")
        ], width=12)
    ])

def create_data_table():
    """Create data table for detailed content view."""
    return dbc.Row([
        dbc.Col([
            html.H3("Content Details", className="mb-3"),
            dash.dash_table.DataTable(
                id='content-table',
                columns=[
                    {'name': 'Platform', 'id': 'platform'},
                    {'name': 'Title', 'id': 'content_title'},
                    {'name': 'Creator', 'id': 'creator'},
                    {'name': 'Engagement', 'id': 'engagement_score'},
                    {'name': 'Category', 'id': 'category'},
                    {'name': 'Views', 'id': 'view_count', 'type': 'numeric'},
                    {'name': 'Likes', 'id': 'like_count', 'type': 'numeric'}
                ],
                page_size=10,
                style_table={'overflowX': 'auto'},
                style_cell={
                    'textAlign': 'left',
                    'padding': '10px',
                    'whiteSpace': 'normal',
                    'height': 'auto'
                },
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'
                    }
                ]
            )
        ], width=12)
    ])

def create_footer():
    """Create dashboard footer."""
    return dbc.Row([
        dbc.Col([
            html.Hr(),
            html.P("Built with Plotly Dash • Data from Spotify & YouTube APIs",
                  className="text-center text-muted"),
            html.P(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                  className="text-center text-muted small")
        ], width=12)
    ])

def create_layout():
    """Create the complete dashboard layout."""
    return dbc.Container([
        create_header(),
        create_filters(),
        create_metric_cards(),
        create_charts_section(),
        html.Br(),
        create_data_table(),
        create_footer(),

        # Hidden divs for storing intermediate data
        dcc.Store(id='spotify-data-store'),
        dcc.Store(id='youtube-data-store'),
        dcc.Store(id='processed-data-store'),

        # Interval component for auto-refresh
        dcc.Interval(
            id='interval-component',
            interval=300*1000,  # 5 minutes
            n_intervals=0
        )
    ], fluid=True, style={'padding': '20px'})
