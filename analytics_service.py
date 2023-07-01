from googleapiclient.discovery import build

def get_analytics_service(credentials):
    # Build the YouTube Analytics service using the provided credentials
    youtubeAnalytics = build('youtubeAnalytics', 'v2', credentials=credentials)
    return youtubeAnalytics

def execute_api_request(client_library_function, **kwargs):
    response = client_library_function(**kwargs).execute()
    print(response)
