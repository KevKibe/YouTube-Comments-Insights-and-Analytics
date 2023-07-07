import dash
import dash_bootstrap_components as dbc
from main import Authenticator, AnalyticsReporter, VideoLister, VideoSelector
from authentication import authenticate
from dash import html
from dash import dcc
import plotly.express as px
import os
from dotenv import load_dotenv
from dash.dependencies import Input, Output, State
load_dotenv()
API_KEY = os.getenv('YT_API_KEY')
credentials = authenticate()

authenticator = Authenticator(credentials)
channel_id = authenticator.authenticate_channel()
analytics_reporter = AnalyticsReporter(credentials, channel_id)

channel_data = analytics_reporter.channel_stats()

channel_report =analytics_reporter.execute_channel_report(credentials)
channel_data = (channel_data.head())
channel_report = (channel_report.head())

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Create the layout
app.layout = html.Div(
    children=[
        dcc.Location(id="url", refresh=False),
        html.H1("Channel Report"),
        dcc.Graph(
            id="channel-report-graph-1",
            figure=px.line(channel_report, x="month", y="views"),
        ),
        dcc.Graph(
            id="channel-report-graph-2",
            figure=px.line(channel_report, x="month", y="estimatedMinutesWatched"),
        ),
        dcc.Graph(
            id="channel-report-graph-3",
            figure=px.line(channel_report, x="month", y="likes"),
        ),
        dcc.Graph(
            id="channel-report-graph-4",
            figure=px.line(channel_report, x="month", y="subscribersGained"),
        )
    ]
)


@app.callback(Output("channel-report-graph-1", "figure"),
              Output("channel-report-graph-2", "figure"),
              Output("channel-report-graph-3", "figure"),
              Output("channel-report-graph-4", "figure"),
              Input("url", "pathname"),
              State("channel-report-graph-1", "figure"),
              State("channel-report-graph-2", "figure"),
              State("channel-report-graph-3", "figure"),
              State("channel-report-graph-4", "figure"))
def update_graphs(pathname, figure1, figure2, figure3, figure4):
    if pathname == "/success":
        # Update the figures based on new data or calculations
        # Replace the following code with your actual logic for updating the figures
        figure1 = px.line(channel_report, x="month", y="views")
        figure2 = px.line(channel_report, x="month", y="estimatedMinutesWatched")
        figure3 = px.line(channel_report, x="month", y="likes")
        figure4 = px.line(channel_report, x="month", y="subscribersGained")

    return figure1, figure2, figure3, figure4


if __name__ == '__main__':
    app.run_server(port=8080,debug=True)
