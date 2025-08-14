import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import load_dotenv

load_dotenv()

# Adjust the file paths as needed.
script_dir = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.join(script_dir, '..', 'google_credentials', 'token.json')
CREDENTIALS_PATH = os.path.join(script_dir, '..', 'google_credentials', 'credentials.json')

# Define the Calendar API scopes (modify if you need different scopes)
SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://mail.google.com/',
    'https://www.googleapis.com/auth/spreadsheets',
    ]

def load_auth_client():
    """
    Load OAuth credentials for accessing the Google Calendar API.
    This function loads credentials from disk, refreshes them if expired,
    or initiates a new OAuth flow if necessary.
    """
    # Load client info from the credentials file.
    with open(CREDENTIALS_PATH) as f:
        creds_data = json.load(f)
        # Handle both 'web' and 'installed' app types
        if 'web' in creds_data:
            client_info = creds_data['web']
        elif 'installed' in creds_data:
            client_info = creds_data['installed']
        else:
            raise ValueError("Credentials file must contain either 'web' or 'installed' key")

    # Load token info.
    with open(TOKEN_PATH) as f:
        token_info = json.load(f)

    # Merge dictionaries so that client_id and client_secret are available.
    combined_info = {**client_info, **token_info}

    # Create credentials from the combined information.
    creds = Credentials.from_authorized_user_info(combined_info, SCOPES)

    # Refresh or request new credentials if necessary.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES
            )
            creds = flow.run_local_server(port=0, prompt='consent', access_type='offline')

        # Save the updated credentials back to disk.
        with open(TOKEN_PATH, "w") as token_file:
            token_file.write(creds.to_json())

    return creds