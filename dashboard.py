import dash
import datetime
import pandas as pd
from datetime import timedelta
import dash_bootstrap_components as dbc
from channel_stats import ChannelAnalytics, Authenticator
from video_stats import VideoAnalytics
from authentication import authenticate
from convo_chain import ConversationChain
from dash import html
from dash import dcc
import plotly.express as px
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], meta_tags=[{'name': 'viewport',
                                                                                   'content': 'width=device-width, initial-scale=1.0'}])

credentials = authenticate()
authenticator = Authenticator(credentials)
channel_id = authenticator.authenticate_channel()
channel_statistics = ChannelAnalytics(credentials, channel_id)
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

def generate_dropdown_options(videos):
    options = []
    for video in videos:
        video_id = video.get('id', {}).get('videoId')
        video_title = video.get('snippet', {}).get('title')
        if video_id and video_title:
            options.append({'label': f"{video_title} ", 'value': video_id})
    return options


heading = dbc.Col(html.H1("Youtube Analytics Dashboard",
                          className='text-center bg-white py-4'),
                  width=12)

card1 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4(str((channel_data.loc['subscriberCount', 'Value'])), className="card-text text-center"),
                html.P(
                    "Total channel Subscribers",
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
                    "Total Channel Views",
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
                    "Total Channel Likes",
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
                    "Total Channel Comments",
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
                    "Total Uploaded Videos",
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

default_column = channel_stats.columns[1]
channel_stats_dropdown = dbc.Col([
    dcc.Dropdown(
        id='column-dropdown',
        options=[{'label': col_name.capitalize(), 'value': col_name} for col_name in channel_stats.columns[1:]],
        value=default_column,
    ),
    
])

channel_days_dropdown = dbc.Col([
    dcc.Dropdown(
        id='channel-days-dropdown',
        options=[
            {'label': '30 days', 'value': 30},
            {'label': '60 days', 'value': 60},
            {'label': '90 days', 'value': 90},
            {'label': 'Lifetime', 'value': 'lifetime'}
        ],
        value='lifetime',
        placeholder="Select days"
    )
])


heading3 = dbc.Col(html.H2("Video Stats",
                           className='text-center bg-white py-4'),
                   width=12)

default_video = videos[0]['id']['videoId'] if videos else None
video_dropdown = dbc.Col([
    dcc.Dropdown(
        id='video-dropdown',
        options=generate_dropdown_options(videos),
        value=default_video,
        placeholder="Select a video"
    )
])

default_y_metric = 'views'
y_dropdown = dbc.Col([
    dcc.Dropdown(
        id='y-dropdown',
        options=[
            {'label': 'Views', 'value': 'views'},
            {'label': 'Estimated Minutes Watched', 'value': 'estimatedMinutesWatched'},
            {'label': 'Average View Duration', 'value': 'averageViewDuration'},
            {'label': 'Average View Percentage', 'value': 'averageViewPercentage'},
            {'label': 'Subscribers Gained', 'value': 'subscribersGained'},
            {'label': 'Comments', 'value': 'comments'},
            {'label': 'Likes', 'value': 'likes'},
            {'label': 'Shares', 'value': 'shares'},
            {'label': 'Annotation Impressions', 'value': 'annotationImpressions'}
        ],
        value=default_y_metric,
        placeholder="Select a metric for y-axis"
    )
])


video_days_dropdown = dbc.Col([
    dcc.Dropdown(
        id='video-days-dropdown',
        options=[
            {'label': '30 days', 'value': 30},
            {'label': '60 days', 'value': 60},
            {'label': '90 days', 'value': 90},
            {'label': 'Lifetime', 'value': 'lifetime'}
        ],
        value='lifetime',
        placeholder="Select days"
    )
])


card6 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4(id='total-views', className="card-text text-center"),
                html.P(
                    "Total Views",
                    className="card-text text-center",
                ),
            ]
        ),
    ],
    className="card-group"
)

card7 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4(id='total-likes', className="card-text text-center"),
                html.P(
                    "Total Likes",
                    className="card-text text-center",
                ),
            ]
        ),
    ],
    className="card-group"
)

card8 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4(id='total-comments', className="card-text text-center"),
                html.P(
                    "Total Comments",
                    className="card-text text-center",
                ),
            ]
        ),
    ],
    className="card-group"
)

card9 = dbc.Card(
    [
        dbc.CardBody(
            [
                dbc.Row([
                    dbc.Col(html.Button("Summarize Video Comments", id="summarize-button", className="btn btn-primary mt-2"))
                ]),
                dbc.Row([dbc.Col(html.Div(id="summary-output", className="mt-4"))])
            ]
        ),
        dbc.CardBody([
            html.Div(id="chat-container", className="chat-container"),
            dbc.Input(id="user-input", type="text", placeholder="Type your message..."),
            html.Button("Send", id="send-button", className="btn btn-primary mt-2")
        ])
    ],
    className="mt-4"
)



app.layout = dbc.Container([
    dcc.Location(id="url", refresh=False),
    dbc.Row([dbc.Col(heading)]),

    dbc.Row([dbc.Col(heading2)]),

    dbc.Row([
        dbc.Col(card1),
        dbc.Col(card2),
        dbc.Col(card3),
        dbc.Col(card4),
        dbc.Col(card5)
    ]),

    dbc.Row([
        channel_stats_dropdown,
        channel_days_dropdown
    ]),
    dbc.Row([dbc.Col(dcc.Graph(id='channel-stats-graph'))]),

    dbc.Row([dbc.Col(heading3)]),

    dbc.Row([
        video_dropdown,
        video_days_dropdown,
        y_dropdown,

    ]),

    dbc.Row([
        dbc.Col(card6),
        dbc.Col(card7),
        dbc.Col(card8),
    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(id='video-stats-graph')),
              dbc.Col(dcc.Graph(id='pie-chart')),
              ]),

    dbc.Row([
        dbc.Col(card9)
    ]),
    
    ],
 fluid=True)


# FOR THE CHANNEL STATS GRAPH
@app.callback(
    Output('channel-stats-graph', 'figure'),
    [Input('column-dropdown', 'value'),
     Input('channel-days-dropdown', 'value')]
)
def update_channel_stats_graph(column, days):
    if days == 'lifetime':
        last_days = pd.Timestamp.min
    else:
        last_days = pd.Timestamp.now() - pd.DateOffset(days=days)

    # Convert 'day' column to datetime
    channel_stats['day'] = pd.to_datetime(channel_stats['day'])

    filtered_stats = channel_stats[channel_stats['day'] >= last_days]
    fig = {
        "data": [
            {
                "x": filtered_stats['day'],
                "y": filtered_stats[column],
                "type": "line",
            },
        ],
        "layout": {
            "title": f"{column.capitalize()} over time (Past {days} Days)",
            "xaxis": {"title": "Date"},
            "yaxis": {"title": f"{column.capitalize()}"},
            "height": 500,
            "margin": {"l": 40, "b": 40, "r": 10},
            "hovermode": "closest",
            "style": "18rem"
        },
    }
    return fig



# FOR THE VIDEO STATS GRAPHAND CARDS
@app.callback(
    [Output('video-stats-graph', 'figure'),
     Output('total-views', 'children'),
     Output('total-likes', 'children'),
     Output('total-comments', 'children')],
    [Input('video-dropdown', 'value'),
     Input('y-dropdown', 'value'),
     Input('video-days-dropdown', 'value')]
)
def update_video_stats(video_id, y_column, days):
    if video_id is None:
        video_id = ''

    if days == 'lifetime':
        last_days = pd.Timestamp.min
    else:
        last_days = pd.Timestamp.now() - pd.DateOffset(days=days)

    stats_df = video_analytics.query_video_statistics(video_id)
    filtered_stats = stats_df[pd.to_datetime(stats_df['day']) >= last_days]

    total_views = filtered_stats['views'].sum()
    total_likes = filtered_stats['likes'].sum()
    total_comments = filtered_stats['comments'].sum()

    fig = px.line(filtered_stats, x='day', y=y_column)
    fig.update_layout(
        title=f"{y_column.capitalize()} over time (Past {days} Days)",
        xaxis={"title": "Date"},
        yaxis={"title": f"{y_column.capitalize()}"},
        height=400,
        margin={"l": 40, "b": 40, "r": 10, "t": 40},
    )

    return fig, total_views, total_likes, total_comments

@app.callback(
    Output('pie-chart', 'figure'),
    [Input('video-dropdown', 'value')],
    [State('video-dropdown', 'options')]
)
def update_pie_chart(video_id, video_options):
    video_title = [video['label'] for video in video_options if video['value'] == video_id]
    comments = video_analytics.get_video_comments(video_id)
    
    # Count the number of comments for each sentiment
    sentiment_counts = {'Positive': 0, 'Negative': 0, 'Neutral': 0}
    for _, sentiment in comments:
        sentiment_counts[sentiment] += 1
    
    # Create the pie chart
    labels = list(sentiment_counts.keys())
    values = list(sentiment_counts.values())
    data = go.Pie(labels=labels, values=values)
    layout = go.Layout(title=f'Sentiment Analysis of Video Comments: {video_title[0]}')
    fig = go.Figure(data=[data], layout=layout)
    
    return fig



    
@app.callback(
    Output("summary-output", "children"),
    [Input("summarize-button", "n_clicks")],
    [State("video-dropdown", "value")]
)
def summarize_comments(n_clicks, video_id):
    if n_clicks is not None and video_id is not None:
        conversation_chain = ConversationChain(video_id)
        response = conversation_chain.get_response("summarize the comments in detail")
        return html.P(response)


@app.callback(
    Output("chat-container", "children"),
    [Input("send-button", "n_clicks")],
    [State("user-input", "value"), State("video-dropdown", "value")]
)
def generate_chat_response(n_clicks, user_input, video_id):
    if n_clicks is not None and user_input and video_id:
        conversation_chain = ConversationChain(video_id)
        response = conversation_chain.get_response(user_input)

        chat_bubble_user = dbc.Alert(user_input, color="primary", className="chat-bubble user")
        chat_bubble_bot = dbc.Alert(response, color="light", className="chat-bubble bot")

        return [chat_bubble_user, chat_bubble_bot]
    return []




# @app.callback(
#     Output("chat-container", "children"),
#     [Input("clear-chat-button", "n_clicks")],
#     [State("chat-container", "children")]
# )
# def clear_chat(n_clicks, chat_container_children):
#     if n_clicks is not None:
#         return None
#     return chat_container_children

if __name__ == '__main__':
    app.run_server(port=8080, debug=True)