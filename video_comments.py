from googleapiclient.discovery import build
from authentication import authenticate
from main import list_videos

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

def get_video_comments(video_id):
    youtube = build('youtube', 'v3', credentials=credentials)

    comments = []
    next_page_token = None

    # Fetch all comments for the video using pagination
    while True:
        response = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=100,  # Maximum value allowed per request
            pageToken=next_page_token
        ).execute()

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)

        next_page_token = response.get('nextPageToken')

        if not next_page_token:
            break

    return comments

if __name__ == '__main__':
    credentials = authenticate()
    videos = list_videos()  # Assuming you have the list_videos() function available

    # Display the list of videos with an index
    for i, video in enumerate(videos):
        video_id = video['id'].get('videoId')
        video_title = video['snippet']['title']
        if video_id:
            print(f"{i+1}. Video ID: {video_id} | Title: {video_title}")

    # Input the number corresponding to the desired video
    video_index = input("Enter the number corresponding to the video you want to retrieve comments for: ")
    try:
        video_index = int(video_index)
        if 1 <= video_index <= len(videos):
            selected_video = videos[video_index - 1]
            selected_video_id = selected_video['id'].get('videoId')
            print(f"Selected Video ID: {selected_video_id}")

            # Retrieve video comments
            comments = get_video_comments(selected_video_id)

            # Print the comments
            print("Video Comments:")
            for i, comment in enumerate(comments):
                print(f"{i+1}. {comment}")
        else:
            print("Invalid video number.")
    except ValueError:
        print("Invalid input. Please enter a number.")
