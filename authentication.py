import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Scopes for the requested permissions
SCOPES = [
    'https://www.googleapis.com/auth/yt-analytics.readonly',
    'https://www.googleapis.com/auth/youtube',
    'https://www.googleapis.com/auth/youtubepartner',
    'https://www.googleapis.com/auth/youtube.force-ssl'

]



def authenticate():
    credentials = load_credentials()

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print('Refreshing Access Token...')
            credentials.refresh(Request())
        else:
            print('Fetching New Tokens...')
            credentials = run_authentication_flow()
            save_credentials(credentials)

    return credentials

def load_credentials():
    credentials = None

    if os.path.exists('token.pickle'):
        print('Loading Credentials from File...')
        try:
            with open('token.pickle', 'rb') as token:
                credentials = pickle.load(token)
        except Exception as e:
            print(f'Error loading credentials: {str(e)}')

    return credentials

def run_authentication_flow():
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secret.json',
        scopes=SCOPES
    )

    flow.run_local_server(port=8080, prompt='consent', authorization_prompt_message='')

    return flow.credentials

def save_credentials(credentials):
    try:
        with open('token.pickle', 'wb') as f:
            print('Saving Credentials for Future Use...')
            pickle.dump(credentials, f)
    except Exception as e:
        print(f'Error saving credentials: {str(e)}')