#!/usr/bin/env python3
import os
import sys
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Add the parent directory to the Python module search path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.google_auth import load_auth_client  # Now Python should locate the module

def get_existing_gmail_labels() -> dict:
    """
    Retrieves all existing Gmail labels and returns a mapping of label names to their IDs.
    """
    try:
        creds = load_auth_client()
        service = build("gmail", "v1", credentials=creds)
        
        existing = service.users().labels().list(userId="me").execute().get("labels", [])
        return {label["name"]: label["id"] for label in existing}
    except HttpError as error:
        print(f"An error occurred while fetching labels: {error}")
        return {"error": str(error)}


def add_custom_gmail_labels(custom_labels: list, label_mapping: dict) -> dict:
    """
    Adds any missing custom labels to Gmail and updates the label mapping.
    """
    try:
        creds = load_auth_client()
        service = build("gmail", "v1", credentials=creds)
        
        for label in custom_labels:
            if label not in label_mapping:
                new_label = service.users().labels().create(
                    userId="me",
                    body={
                        "name": label,
                        "labelListVisibility": "labelShow",
                        "messageListVisibility": "show"
                    }
                ).execute()
                label_mapping[label] = new_label["id"]
                print(f"Created label '{label}' with id: {new_label['id']}")
            else:
                print(f"Label '{label}' already exists with id: {label_mapping[label]}")
        
        return label_mapping
    except HttpError as error:
        print(f"An error occurred while creating labels: {error}")
        return {"error": str(error)}


def handle_gmail_labels() -> dict:
    """
    Main function that gets existing Gmail labels, adds custom labels if needed,
    and writes the final label mapping to gmail_labels.json.
    """
    # Add your custom labels here (e.g., ["Work", "Personal", "Important"])
    custom_labels = [
        "Work",
        # "Personal", 
        # "Important"
    ]
    
    label_mapping = get_existing_gmail_labels()
    if "error" in label_mapping:
        return label_mapping
    
    label_mapping = add_custom_gmail_labels(custom_labels, label_mapping)
    
    # Write to gmail_labels.json
    output_file = "gmail_labels.json"
    try:
        with open(output_file, "w") as f:
            json.dump(label_mapping, f, indent=2)
        print(f"Label mapping saved to {output_file}")
    except Exception as error:
        print(f"Error writing to file: {error}")
        label_mapping["file_error"] = str(error)
    
    return label_mapping

if __name__ == "__main__":
    handle_gmail_labels()