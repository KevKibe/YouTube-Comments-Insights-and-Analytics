from googleapiclient.discovery import build
from authentication import authenticate
from analytics_service import get_analytics_service, execute_api_request

def get_authenticated_channel():
    youtube = build('youtube', 'v3', credentials=credentials)

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

def list_videos():
    channel_id = get_authenticated_channel()
    youtube = build('youtube', 'v3', credentials=credentials)

    videos = []
    next_page_token = None

    #fetching videos from the channel
    while True:
        response = youtube.search().list(
            part='id,snippet',
            channelId=channel_id,
            maxResults=50,  #maximum value per request
            pageToken=next_page_token
        ).execute()

        videos.extend(response['items'])
        next_page_token = response.get('nextPageToken')

        if not next_page_token:
            break

    return videos

if __name__ == '__main__':
    credentials = authenticate()
    videos = list_videos()

    #displaying and selecting the list of videos with an index
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

            youtubeAnalytics = get_analytics_service(credentials)

            # Execute analytics report request for the selected video
            execute_api_request(
                youtubeAnalytics.reports().query,
                ids='channel==MINE',
                startDate='2022-01-01',
                endDate='2023-01-01',
                metrics='estimatedMinutesWatched,views,likes,subscribersGained',
                dimensions='month',
                filters=f'video=={selected_video_id}',
                sort='month'
            )
        else:
            print("Invalid video number.")
    except ValueError:
        print("Invalid input. Please enter a number.")


