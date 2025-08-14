# Helper Scripts

This directory contains utility scripts to help set up and manage Google API authentication and Gmail labels for the LangGraph Home Assistant project.

## Scripts Overview

### 1. `get_token.py`
Handles Google OAuth2 authentication and token management for accessing Google APIs (Calendar, Gmail, Sheets).

### 2. `check_gmail_labels.py`
Creates and manages custom Gmail labels needed by the home assistant for email categorization.

## Prerequisites

1. **Google Cloud Project Setup** (see [Google Cloud Console Setup](#google-cloud-console-setup))
2. **Google API Credentials** (see [Creating Google Credentials](#creating-google-credentials))
3. **Python Dependencies** - Install from the main project directory:
   ```bash
   pip install -r requirements.txt
   ```

## Google Cloud Console Setup

### Step 1: Create a Google Cloud Project
1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Enter a project name (e.g., "langgraph-home-assistant")
4. Click "Create"

### Step 2: Enable Required APIs
1. In the Google Cloud Console, go to "APIs & Services" → "Library"
2. Search for and enable the following APIs:
   - **Gmail API**
   - **Google Calendar API**
   - **Google Sheets API**

### Step 3: Configure OAuth Consent Screen
1. Go to "APIs & Services" → "OAuth consent screen"
2. Choose "External" user type (unless you have a Google Workspace)
3. Fill in the required fields:
   - App name: "LangGraph Home Assistant"
   - User support email: Your email
   - Developer contact information: Your email
4. Click "Save and Continue"
5. Add scopes (optional for testing) - Click "Save and Continue"
6. If you chose external: Add your own email as a test user to be able to access the app - Click "Save and Continue"

### Step 4: Create OAuth2 Credentials
1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. Choose "Desktop application" as the application type
4. Enter a name (e.g., "LangGraph Desktop Client")
5. Click "Create"
6. Download the JSON file (this becomes your `google_credentials/credentials.json`)

## Creating Google Credentials

### Step 1: Download and Place Credentials File
1. After creating OAuth2 credentials in Google Cloud Console, download the JSON file
2. Rename it to `credentials.json`
3. Place it in the `google_credentials/` directory:
   ```
   google_credentials/
   ├── credentials.json      # Your actual credentials (DO NOT commit to git)
   ├── credentials.example.json
   └── token.example.json
   ```

### Step 2: Generate Authentication Token
1. Navigate to the helper_scripts directory:
   ```bash
   cd helper_scripts
   ```

2. Run the token generation script:
   ```bash
   python get_token.py
   ```

3. This will:
   - Open your default web browser
   - Prompt you to sign in to your Google account
   - Ask for permission to access your Gmail, Calendar, and Sheets
   - **IMPORTANT:** you will be asked to give permissions to **read, send and delete** all data in Gmail and Google Sheets and Calendar. This may be risky if you will be experimenting with new agents and tools. Currently, no tools to delete things are defined. If you want to be on the safe side when experimenting, modify **get_token.py** to e.g. only request read access.
   - Generate a `token.json` file in the `google_credentials/` directory

### Step 3: Verify Token Creation
After successful authentication, you should see:
```
google_credentials/
├── credentials.json      # Your OAuth2 client credentials (DO NOT commit to git)
├── token.json           # Your access/refresh tokens (DO NOT commit to git)
├── credentials.example.json
└── token.example.json
```

## Running the Helper Scripts



### Create Gmail Labels
```bash
cd helper_scripts
python handle_gmail_labels.py
```

**What it does:**
- Gets your gmail labels (and can be edited to add new labels as well)
- Saves label mappings to `gmail_labels.json`

**When to run:**
- After initial setup
- When you need to recreate deleted labels
- When adding new custom labels to the list

## Troubleshooting

### Common Issues

**"File not found" errors:**
- Ensure `credentials.json` exists in `google_credentials/` directory
- Verify you downloaded the correct OAuth2 credentials from Google Cloud Console

**Browser doesn't open during authentication:**
- Copy the URL from the terminal and paste it into your browser manually
- Ensure port 8080 is available

**"Access denied" errors:**
- Verify all required APIs are enabled in Google Cloud Console
- Check that your Google account has access to the resources
- Ensure OAuth consent screen is properly configured

**Token refresh errors:**
- Delete `token.json` and run `get_token.py` again
- Verify your `credentials.json` file is valid

### Security Notes

- **Never commit `credentials.json` or `token.json` to version control**
- These files contain sensitive authentication information
- The `.gitignore` should already exclude these files
- Only share these files through secure channels if needed

## API Scopes

The scripts request access to the following Google API scopes:
- `https://www.googleapis.com/auth/calendar` - Calendar read/write access
- `https://mail.google.com/` - Full Gmail access
- `https://www.googleapis.com/auth/spreadsheets` - Google Sheets read/write access
- 
- This may be risky if you will be experimenting with agents. If you want to be on the safe side when experimenting, modify **get_token.py** to e.g. only request read access.


## File Structure

```
helper_scripts/
├── README.md                 # This file
├── get_token.py             # OAuth2 token management
├── check_gmail_labels.py    # Gmail label creation
└── gmail_labels.json        # Generated label mappings (created after running check_gmail_labels.py)

google_credentials/
├── credentials.json         # Your OAuth2 credentials (DO NOT commit)
├── token.json              # Your access tokens (DO NOT commit)
├── credentials.example.json # Empty template
└── token.example.json      # Empty template
```