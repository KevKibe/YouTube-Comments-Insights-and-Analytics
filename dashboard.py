import dash
import datetime
from datetime import timedelta
import dash_bootstrap_components as dbc
from channel_stats import ChannelAnalytics , Authenticator
from video_stats import VideoAnalytics
from authentication import authenticate
from dash import html
from dash import dcc
import plotly.express as px
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], meta_tags=[{'name': 'viewport',
                                                                                   'content': 'width=device-width, initial-scale=1.0'}])

credentials = authenticate()
authenticator = Authenticator(credentials)
channel_id = authenticator.authenticate_channel()
channel_statistics= ChannelAnalytics(credentials, channel_id)
column_names = {
    'views': 'Views',
    'estimatedMinutesWatched': 'Estimated Minutes Watched',
    'averageViewDuration': 'Average View Duration',
    'averageViewPercentage': 'Average View Percentage',
    'subscribersGained': 'Subscribers Gained',
    'comments': 'Comments',
    'likes': 'Likes',
    'shares': 'Shares',
    'annotationImpressions': 'Annotation Impressions'
}
channel_stats = channel_statistics.query_channel_statistics()
channel_stats = channel_stats.rename(columns=column_names)
channel_data = channel_statistics.channel_data()

video_analytics = VideoAnalytics(credentials)
videos = video_analytics.get_channel_videos(channel_id)  
video_stats = video_analytics.query_video_statistics(video_id)

def generate_dropdown_options(videos):
    options = []
    for video in videos:
        video_id = video.get('id', {}).get('videoId')
        video_title = video.get('snippet', {}).get('title')
        if video_id and video_title:
            options.append({'label': f"{video_title} ({video_id})", 'value': video_id})
    return options
videos = channel_data['videoCount'][0] 


heading = dbc.Col(html.H1("Youtube Analytics Dashboard",
                          className='text-center bg-white py-4'),
                  width=12)


card1 = dbc.Card( 
    [
        dbc.CardBody( 
            [
                html.H4(str((channel_data.loc['subscriberCount', 'Value'])), className="card-text text-center"),
                html.P(
                    "Subscribers",
                    className="card-text text-center",
                ),
            ]
        ),
    ],
    
    className="card-group"
)

card2 = dbc.Card( 
    [
        dbc.CardBody(
            [
                html.H4(str((channel_data.loc['viewCount', 'Value'])), className="card-text text-center"),
                html.P(
                    "Total Views",
                    className="card-text text-center",
                ),
            ]
        ),
    ],
     className="card-group"
)

card3 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4(str(channel_stats['Likes'].sum()), className="card-text text-center"),
                html.P(
                    "Total Likes",
                    className="card-text text-center",
                ),
            ]
        ),
    ],
   
     className="card-group"
)

card4 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4(str(channel_stats['Comments'].sum()), className="card-text text-center"),
                html.P(
                    "Total Comments",
                    className="card-text text-center",
                ),
            ]
        ),
    ],
    
     className="card-group"
)

card5 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4(str((channel_data.loc['videoCount', 'Value'])), className="card-text text-center"),
                html.P(
                    "Uploaded Videos",
                    className="card-text text-center",
                ),
            ]
        ),
    ],
     className="card-group"
)

heading2 = dbc.Col(html.H2("Channel Stats",
                           className='text-center bg-white py-4'),
                   width=14)


channel_stats_dropdown = dbc.Col([dcc.Dropdown(
        id='column-dropdown',
        options=[{'label': col_name.capitalize(), 'value': col_name} for col_name in channel_stats.columns[1:]],
        value='views'
    ),
    dcc.Graph(id='graph')
])


heading3 = dbc.Col(html.H2("Video Stats",
                           className='text-center bg-white py-4'),
                   width=12)

video_dropdown = dbc.Col([dcc.Dropdown(
    id='video-dropdown',
    options=generate_dropdown_options(videos),
    placeholder="Select a video"
)])

y_dropdown = dbc.Col([dcc.Dropdown(
    id='y-dropdown',
    options=[{'label': col_name.capitalize(), 'value': col_name} for col_name in video_stats.columns[1:]],
    placeholder="Select a metric for y-axis"
)])


app.layout = dbc.Container([
    dcc.Location(id="url", refresh=False),
    dbc.Row([dbc.Col(heading)]),

    dbc.Row([
        dbc.Col(card1),
        dbc.Col(card2),
        dbc.Col(card3),
        dbc.Col(card4),
        dbc.Col(card5)
    ]),

    dbc.Row([dbc.Col(heading2)]),

    dbc.Row([
        channel_stats_dropdown
    ]),

    dbc.Row([dbc.Col(heading3)
             ]),
    
    dbc.Row([
        video_dropdown,
        y_dropdown
    ]),
    
    dbc.Row([dbc.Col(dcc.Graph(id='line-plot'))])

], fluid=True)



@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    dash.dependencies.Input('column-dropdown', 'value')
)
def update_graph(column):
    fig = {
        "data": [
            {
                "x": channel_stats['day'],
                "y": channel_stats[column],
                "type": "line",
            },
        ],
        "layout": {
            "title": f"{column.capitalize()} over time",
            "xaxis": {"title": "Date"},
            "yaxis": {"title": f"{column.capitalize()}"},
            "height": 500,
            "margin": {"l": 40, "b": 40, "r": 10},
            "hovermode": "closest",
            "style" : "18rem"
        },
    }
    return fig


@app.callback(
    Output('line-plot', 'figure'),
    Input('video-dropdown', 'value'),
    Input('y-dropdown', 'value')
)
def update_video_graph(video_id, y_column):
    if video_id is None:
        video_id = ''  # Set a default value if video_id is None

    stats_df = video_analytics.query_video_statistics(video_id)
    fig = px.line(stats_df, x='day', y=y_column)
    return fig


if __name__ == '__main__':
    app.run_server(port=8080, debug=True)
