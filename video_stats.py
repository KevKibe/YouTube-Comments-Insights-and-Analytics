import pandas as pd
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from authentication import authenticate
import datetime
from googletrans import Translator
from textblob import TextBlob
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
        

class VideoAnalytics:
    def __init__(self, credentials):
        self.credentials = credentials
        self.youtube_analytics = build('youtubeAnalytics', 'v2', credentials=self.credentials,developerKey=API_KEY)
    
    def get_channel_videos(self, channel_id):
        youtube = build('youtube', 'v3', credentials=self.credentials)

        videos = []
        next_page_token = None

        while True:
            request = youtube.search().list(
                part='snippet',
                channelId=channel_id,
                maxResults=100, 
                pageToken=next_page_token,
                type='video'
            )

            response = request.execute()

            videos.extend(response['items'])

            next_page_token = response.get('nextPageToken')

            if not next_page_token:
                break

        return videos    
        

    def query_video_statistics(self,video_id ):
        end_date = datetime.date.today()
        response = self.youtube_analytics.reports().query(
                ids=f'channel==MINE',
                filters=f'video=={video_id}',
                startDate='1970-01-01',
                endDate=end_date.strftime('%Y-%m-%d'),
                metrics='views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained,comments,likes,shares',
                dimensions='day'
            ).execute()
        headers = [header['name'] for header in response['columnHeaders']]
        rows = response['rows']
        stats_df = pd.DataFrame(rows, columns=headers)
        return stats_df
    

    def get_video_comments(self, video_id):
        youtube = build('youtube', 'v3', credentials=self.credentials)
        comments = []
        results = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText"
        ).execute()
        while results:
            for item in results['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                translator = Translator()
                translation = translator.translate(comment, dest='en').text
                blob = TextBlob(translation)
                sentiment = blob.sentiment.polarity
                if sentiment > 0:
                    sentiment_label = 'Positive'
                elif sentiment < 0:
                    sentiment_label = 'Negative'
                else:
                    sentiment_label = 'Neutral'
                comments.append((comment, sentiment_label))   

            if 'nextPageToken' in results:
                results = youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    pageToken=results['nextPageToken'],
                    textFormat="plainText"
                ).execute()
            else:
                break
        
        return comments

    
# credentials = authenticate() 
# video_analytics = VideoAnalytics(credentials)
# video_id = 'cDedvKJJ6Xg'
# # video_stats = video_analytics.query_video_statistics(video_id)
# # print(video_stats)
# comments = video_analytics.get_video_comments(video_id)
# print(comments)

# 0   day                      338 non-null    object
#  1   views                    338 non-null    int64
#  2   estimatedMinutesWatched  338 non-null    int64
#  3   averageViewDuration      338 non-null    int64
#  4   averageViewPercentage    338 non-null    float64
#  5   subscribersGained        338 non-null    int64
#  6   comments                 338 non-null    int64
#  7   likes                    338 non-null    int64
#  8   shares                   338 non-null    int64
#  9   annotationImpressions    338 non-null    int64
# 1. Video ID: lvJWSvFZIQg | Title: Kenya VS Canada Malaga 7S 2022 #Spain7S
# 2. Video ID: epZTJBvjdn0 | Title: Kenya vs Spain Seville 7s 2022 #spain7s
# 3. Video ID: FKsHOZcMXIM | Title: Kenya vs France Malaga 7s 2022 #spain7s
# 4. Video ID: w9j3QXgnd_w | Title: Kenya vs Wales Malaga 7s 2022 #spain7s
# 5. Video ID: ZzLWURb70vA | Title: Kenya vs Scotland Seville 7s 2022 #spain7s
# 6. Video ID: osQMJwa60Ts | Title: Kenya vs Japan Malaga 7s 2022 #spain7s
# 7. Video ID: cDedvKJJ6Xg | Title: Kenya vs Australia Seville 7s 2022 #spain7s
# 8. Video ID: Cj8_3VgxUu0 | Title: Kenya vs Canada Seville 7s 2022 #spain7s
# 10. Video ID: HMnQqeMqIGU | Title: 1ST HALF KENYA VS SOUTHAFRICA CUP QUARTERFINAL DUBAI 7s 2021
# 11. Video ID: b1WLS68UTh0 | Title: 2ND HALF KENYA VS SOUTHAFRICA CUP QUARTER FINALS DUBAI 7s 2021
# 12. Video ID: ednaSzGa8Ew 
