import streamlit as st
from channel_stats import ChannelAnalytics, Authenticator
from video_stats import VideoAnalytics
from authentication import authenticate
from convo_chain import ConversationChain
import plotly.graph_objects as go
import pandas as pd

st.title("YouTube Analytics Dashboard")

# Create a global variable to store the credentials
credentials = None

# Add a button to trigger authentication


# If the button is clicked, authenticate the user and store the credentials in the global variable

credentials = authenticate()
authenticator = Authenticator(credentials)
channel_id = authenticator.authenticate_channel()
st.write("Authentication successful!")

# Use the credentials to access the channel statistics and videos
if credentials:
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

    st.header("Channel Stats")
    st.write(f"Total channel Subscribers: {channel_data.loc['subscriberCount', 'Value']}")
    st.write(f"Total Channel Views: {channel_data.loc['viewCount', 'Value']}")
    st.write(f"Total Channel Likes: {channel_stats['Likes'].sum()}")
    st.write(f"Total Channel Comments: {channel_stats['Comments'].sum()}")
    st.write(f"Total Uploaded Videos: {channel_data.loc['videoCount', 'Value']}")

    # Dropdowns for the channel stats graph
    column_dropdown_value = st.selectbox("Select column", channel_stats.columns[1:])
    channel_days_dropdown_value = st.selectbox("Select days", ['lifetime', 30, 60, 90])

    if channel_days_dropdown_value == 'lifetime':
        last_days = pd.Timestamp.min
    else:
        last_days = pd.Timestamp.now() - pd.DateOffset(days=channel_days_dropdown_value)

    channel_stats['day'] = pd.to_datetime(channel_stats['day'])
    filtered_stats = channel_stats[channel_stats['day'] >= last_days]

    fig_channel_stats = go.Figure(
        data=[
            go.Scatter(x=filtered_stats['day'], y=filtered_stats[column_dropdown_value], mode='lines')
        ],
        layout=go.Layout(
            title=f"{column_dropdown_value.capitalize()} over time (Past {channel_days_dropdown_value} Days)",
            xaxis={"title": "Date"},
            yaxis={"title": f"{column_dropdown_value.capitalize()}"},
            height=500,
            margin={"l": 40, "b": 40, "r": 10},
            hovermode="closest"
        )
    )

    st.plotly_chart(fig_channel_stats)
