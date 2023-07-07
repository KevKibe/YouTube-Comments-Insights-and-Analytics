import dash
import dash_html_components as html
from dash import dcc
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from authentication import authenticate
from main import AnalyticsReporter
from main import VideoLister
from main import VideoSelector

# Authenticate and initialize necessary objects
credentials = authenticate()
analytics_reporter = AnalyticsReporter(credentials)
video_lister = VideoLister(credentials)
video_selector = VideoSelector()

app = dash.Dash(__name__)

# Define the layout of the web application
layout = html.Div(children=[
    html.H1("YouTube Analytics Dashboard"),

    # Variables channel data
    html.Div([
        html.H2("Variables Channel Data"),
        dcc.Graph(id="variables-channel-graph")
    ]),

    # Channel report
    html.Div([
        html.H2("Channel Report"),
        dcc.Graph(id="channel-report-graph")
    ]),

    # Video report
    html.Div([
        html.H2("Video Report"),
        dcc.Graph(id="video-report-graph"),
        html.Div(id="video-comments")
    ])
])

# Register the callbacks
@app.callback(
    Output("variables-channel-graph", "figure"),
    Output("channel-report-graph", "figure"),
    Output("video-report-graph", "figure"),
    Output("video-comments", "children"),
    Input("video-selector", "value")
)
def update_graphs(selected_video_id):
    analytics_reporter.channel_id = selected_video_id

    # Update Variables Channel Data graph
    variables_channel_fig = go.Figure()
    # Add your code to populate the figure with data for variables channel data

    # Update Channel Report graph
    channel_report_fig = go.Figure()
    # Add your code to populate the figure with data for the channel report

    # Update Video Report graph
    video_report_fig = go.Figure()
    # Add your code to populate the figure with data for the video report

    # Get video comments
    comments = analytics_reporter.get_video_comments(selected_video_id)
    comments_html = html.Div([
        html.H3("Video Comments"),
        html.Ul([html.Li(comment) for comment in comments])
    ])

    return variables_channel_fig, channel_report_fig, video_report_fig, comments_html

if __name__ == '__main__':
    app.run_server(debug=True)
