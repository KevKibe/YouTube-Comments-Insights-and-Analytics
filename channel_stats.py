import pandas as pd
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from authentication import authenticate
import datetime
import os 
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('YT_API_KEY')
API_SERVICE_NAME = 'youtubeAnalytics'
API_VERSION = 'v2'
CLIENT_SECRETS_FILE = 'client_secret.json'

class Authenticator:
    def __init__(self, credentials):
        self.credentials = credentials

    def authenticate_channel(self):
        youtube = build('youtube', 'v3', credentials=self.credentials)

        # Retrieve the authorized user's channel
        response = youtube.channels().list(
            part='id',
            mine=True
        ).execute()

        if 'items' in response:
            channel_id = response['items'][0]['id']
            return channel_id
        else:
            raise Exception('Failed to retrieve authenticated channel.')
        

class ChannelAnalytics:
    def __init__(self, credentials, channel_id):
        self.credentials = credentials
        self.channel_id = channel_id
        self.youtube_analytics = build('youtubeAnalytics', 'v2', credentials=self.credentials)
        self.youtube_data = build('youtube', 'v3', credentials=self.credentials, developerKey=API_KEY)


    def channel_data(self):       
        request = self.youtube_data.channels().list(
           part="statistics",
           id=self.channel_id
           ).execute()
        statistics = request['items'][0]['statistics']
        df = pd.DataFrame.from_dict(statistics, orient='index', columns=['Value'])
        return df


    def query_channel_statistics(self):
        end_date = datetime.date.today()
        response = self.youtube_analytics.reports().query(
            ids=f'channel==MINE',
            startDate='1970-01-01',
            endDate=end_date.strftime('%Y-%m-%d'),
            metrics='views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained,comments,likes,shares',
            dimensions='day'
        ).execute()
        headers = [header['name'] for header in response['columnHeaders']]
        rows = response['rows']
        stats_df = pd.DataFrame(rows, columns=headers)
        return stats_df


# credentials = authenticate()

# authenticator = Authenticator(credentials)
# channel_id = authenticator.authenticate_channel()

# channel_statistics= ChannelAnalytics(credentials, channel_id)

# channel_stats = channel_statistics.query_channel_statistics()
# print(channel_stats.info())

# channel_data = channel_statistics.channel_data()
# print(channel_data.info())

#  0   day                      347 non-null    object
#  1   views                    347 non-null    int64
#  2   estimatedMinutesWatched  347 non-null    int64
#  3   averageViewDuration      347 non-null    int64
#  4   averageViewPercentage    347 non-null    float64
#  5   subscribersGained        347 non-null    int64
#  6   comments                 347 non-null    int64
#  7   likes                    347 non-null    int64
#  8   shares                   347 non-null    int64
#  9   annotationImpressions    347 non-null    int64