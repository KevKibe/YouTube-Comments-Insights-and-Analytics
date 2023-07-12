from googleapiclient.discovery import build
from authentication import authenticate
from googleapiclient.discovery import build
from tabulate import tabulate
import os
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv('YT_API_KEY')


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

class VideoLister:
    def __init__(self, credentials):
        self.credentials = credentials

    def list_videos(self, channel_id):
        youtube = build('youtube', 'v3', credentials=self.credentials)

        videos = []
        next_page_token = None

        # Fetch videos from the channel
        while True:
            response = youtube.search().list(
                part='id,snippet',
                channelId=channel_id,
                maxResults=50,  # maximum value per request
                pageToken=next_page_token
            ).execute()

            videos.extend(response['items'])
            next_page_token = response.get('nextPageToken')

            if not next_page_token:
                break

        return videos


# class VideoSelector:
    # def select_video(self, videos):
    #     for i, video in enumerate(videos):
    #         video_id = video['id'].get('videoId')
    #         video_title = video['snippet']['title']
    #         if video_id:
    #             f"{i+1}. Video ID: {video_id} | Title: {video_title}"

    #     video_index = ()
    #     video_index = int(video_index)
    #        if 1 <= video_index <= len(videos):
    #             selected_video = videos[video_index - 1]
    #             selected_video_id = selected_video['id'].get('videoId')
    #             return selected_video_id
            




class AnalyticsReporter:
    def __init__(self, credentials, channel_id):
        self.credentials = credentials
        self.channel_id = channel_id

    

    def channel_stats(self):
        youtube = build('youtube', 'v3', credentials=self.credentials, developerKey=API_KEY)
        request = youtube.channels().list(
           part="statistics",
           id=self.channel_id
           ).execute()
        statistics = request['items'][0]['statistics']
        df = pd.DataFrame.from_dict(statistics, orient='index', columns=['Value'])
        return df
    

    def execute_channel_report(self, credentials):
        youtubeAnalytics = build('youtubeAnalytics', 'v2', credentials=credentials)
        result = youtubeAnalytics.reports().query(
            ids='channel==MINE',
            startDate='2022-01-01',
            endDate='2023-01-01',
            metrics='estimatedMinutesWatched,views,likes,subscribersGained',
            dimensions='month',
            sort='month'
        ).execute()
        headers = [header['name'] for header in result['columnHeaders']]
        rows = result['rows']
        df = pd.DataFrame(rows, columns=headers)
        return df
    

    def execute_video_report(self, selected_video_id, credentials):
        youtubeAnalytics = build('youtubeAnalytics', 'v2', credentials=credentials)
        result = youtubeAnalytics.reports().query(
            ids='channel==MINE',
            startDate='2022-01-01',
            endDate='2023-01-01',
            metrics='estimatedMinutesWatched,views,likes,subscribersGained',
            dimensions='month',
            filters=f'video=={selected_video_id}',
            sort='month'
        ).execute()
        column_names = [header['name'] for header in result['columnHeaders']]
        df = tabulate(result['rows'],headers = column_names, tablefmt = 'pretty')
        return df
    

    def get_video_comments(self, selected_video_id, credentials):
        youtube = build('youtube', 'v3', credentials=credentials,developerKey=API_KEY)
        comments = []
        results = youtube.commentThreads().list(
            part="snippet",
            videoId=selected_video_id,
            textFormat="plainText"
        ).execute()
        while results:
            for item in results['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append(comment)

            if 'nextPageToken' in results:
                results = youtube.commentThreads().list(
                    part="snippet",
                    videoId=selected_video_id,
                    pageToken=results['nextPageToken'],
                    textFormat="plainText"
                ).execute()
            else:
                break
        return comments


    


