import dash
import dash_bootstrap_components as dbc
from main import Authenticator, AnalyticsReporter, VideoSelector, VideoLister
from authentication import authenticate
from dash import html
from dash import dcc
import plotly.express as px
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], meta_tags=[{'name': 'viewport',
                                                                                   'content': 'width=device-width, initial-scale=1.0'}])

# Authenticate and initialize objects
credentials = authenticate()
authenticator = Authenticator(credentials)
channel_id = authenticator.authenticate_channel()
analytics_reporter = AnalyticsReporter(credentials, channel_id)
channel_data = analytics_reporter.channel_stats()
channel_report = analytics_reporter.execute_channel_report(credentials)

# video_lister = VideoLister(credentials)
# videos = video_lister.list_videos(channel_id)
# video_selector = VideoSelector()
# selected_video_id = video_selector.select_video(videos)
# video_report =analytics_reporter.execute_video_report(selected_video_id, credentials)
# comments = analytics_reporter.get_video_comments(selected_video_id, credentials)



app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP,'style.css'])


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
    style={"width": "18rem"},
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
    style={"width": "18rem"},
)

card3 = dbc.Card(
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
    style={"width": "18rem"},
)


heading2 = dbc.Col(html.H2("Channel Stats",
                        className='text-center bg-white mt-4'),
                width=12)

ch_stat1 = dcc.Graph(
    id="channel-report-graph-1",
    figure={
        "data": [
            {
                "x": channel_report["month"],
                "y": channel_report["views"],
                "type": "line",
            },
        ],
        "layout": {
            "title": "Channel Views"

        },
    },
)


ch_stat2 = dcc.Graph(
    id="channel-report-graph-2",
    figure={
        "data": [
            {
                "x": channel_report["month"],
                "y": channel_report["likes"],
                "type": "line",
            },
        ],
        "layout": {
            "title": "Channel Likes"
     
        },
    },
)

ch_stat3 = dcc.Graph(
    id="channel-report-graph-3",
    figure={
        "data": [
            {
                "x": channel_report["month"],
                "y": channel_report["subscribersGained"],
                "type": "line",
            },
        ],
        "layout": {
            "title": "Subscribers Gained"
        },
    },
)

ch_stat4 = dcc.Graph(
    id="channel-report-graph-4",
    figure={
        "data": [
            {
                "x": channel_report["month"],
                "y": channel_report["estimatedMinutesWatched"],
                "type": "line",
            },
        ],
        "layout": {
            "title": "Minutes Watched"
  
        },
    },
)


# vid_dropdown = dcc.Dropdown(
#         id='dropdown',
#         options=[{'label': row['Title'], 'value': row['Video ID']} for index, row in video_report.iterrows()],
#         value='osQMJwa60Ts'
#     ) 


app.layout = dbc.Container([
    dcc.Location(id="url", refresh=False),
    dbc.Row([dbc.Col(heading)]),

    dbc.Row([

        dbc.Col(card1),
        dbc.Col(card2),
        dbc.Col(card3)
    ]),
    
    dbc.Row([dbc.Col(heading2)]),
   
    dbc.Row([
        dbc.Col([ch_stat1]),
        dbc.Col([ch_stat2]),

    ]),
     dbc.Row([

        dbc.Col([ch_stat3]),
        dbc.Col([ch_stat4]),
    ])
    # dcc.Row([vid_dropdown])


],fluid =True)


@app.callback(
    Output("channel-report-graph-1", "figure"),
    Output("channel-report-graph-2", "figure"),
    Output("channel-report-graph-3", "figure"),
    Output("channel-report-graph-4", "figure"),
    Input("url", "pathname"),
    # Input("dropdown", "value"),
    State("channel-report-graph-1", "figure"),
    State("channel-report-graph-2", "figure"),
    State("channel-report-graph-3", "figure"),
    State("channel-report-graph-4", "figure")
)
def update_graphs(pathname, figure1, figure2, figure3, figure4):
    if pathname == "/success":
        # Update the figures based on new data or calculations
        # Replace the following code with your actual logic for updating the figures
        figure1 = px.line(channel_report, x="month", y="views")
        figure2 = px.line(channel_report, x="month", y="likes")
        figure3 = px.line(channel_report, x="month", y="subscribersGained")
        figure4 = px.line(channel_report, x="month", y="estimatedMinutesWatched")

    return figure1, figure2, figure3, figure4
if __name__ == '__main__':
    app.run_server(port=8080, debug=True)
