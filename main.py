from googleapiclient.discovery import build
from authentication import authenticate
from googleapiclient.discovery import build
from tabulate import tabulate
import os
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


class VideoSelector:
    def select_video(self, videos):
        # Display and select the list of videos with an index
        for i, video in enumerate(videos):
            video_id = video['id'].get('videoId')
            video_title = video['snippet']['title']
            if video_id:
                print(f"{i+1}. Video ID: {video_id} | Title: {video_title}")

        video_index = input("Select the video: ")
        try:
            video_index = int(video_index)
            if 1 <= video_index <= len(videos):
                selected_video = videos[video_index - 1]
                selected_video_id = selected_video['id'].get('videoId')
                print(f"Selected Video ID: {selected_video_id}")
                return selected_video_id

            else:
                print("Invalid video number.")
        except ValueError:
            print("Invalid input. Please enter a number.")


class AnalyticsReporter:
    def __init__(self, credentials):
        self.credentials = credentials
        self.channel_id = channel_id


    def get_analytics_service(self, credentials):
        youtubeAnalytics = build('youtubeAnalytics', 'v2', credentials=credentials)
        return youtubeAnalytics
    

    def channel_stats(self):
        youtube = build('youtube', 'v3', credentials=self.credentials, developerKey=API_KEY)
        request = youtube.channels().list(
           part="statistics",
           id=self.channel_id
           ).execute()
        column_names = [header for header in request['items'][0]['statistics']]
        data = [[value for value in request['items'][0]['statistics'].values()]]
        df = tabulate(data,headers = column_names, tablefmt = 'pretty')
        return request
    

    def execute_channel_report(self, youtubeAnalytics):
        result = youtubeAnalytics.reports().query(
            ids='channel==MINE',
            startDate='2022-01-01',
            endDate='2023-01-01',
            metrics='estimatedMinutesWatched,views,likes,subscribersGained',
            dimensions='month',
            sort='month'
        ).execute()
        column_names = [header['name'] for header in result['columnHeaders']]
        df = tabulate(result['rows'],headers = column_names, tablefmt = 'pretty')
        return result
    

    def execute_video_report(self, selected_video_id, youtubeAnalytics):
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
        return result
    

    def get_video_comments(self, selected_video_id):
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



if __name__ == '__main__':
    credentials = authenticate()

    authenticator = Authenticator(credentials)
    channel_id = authenticator.authenticate_channel()
    analytics_reporter = AnalyticsReporter(credentials)

    youtube_analytics = AnalyticsReporter(credentials).get_analytics_service(credentials)
    channel_data = analytics_reporter.channel_stats()
    print(channel_data)

    channel_report =analytics_reporter.execute_channel_report( youtube_analytics)
    print(channel_report)

    video_lister = VideoLister(credentials)
    videos = video_lister.list_videos(channel_id)

    video_selector = VideoSelector()
    selected_video_id = video_selector.select_video(videos)

    if selected_video_id:
        video_report =analytics_reporter.execute_video_report(selected_video_id, youtube_analytics)
        print(video_report)
        comments = analytics_reporter.get_video_comments(selected_video_id)
        print(comments)



