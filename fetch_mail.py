import os.path
import base64
import json
import re
import time
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import logging
import requests
from dotenv import load_dotenv

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly','https://www.googleapis.com/auth/gmail.modify']

def save_attachment(service, msg, part):
    filename = part['filename']
    if 'data' in part['body']:
        data = part['body']['data']
    else:
        att_id = part['body']['attachmentId']
        att = service.users().messages().attachments().get(userId='me', messageId=msg['id'], id=att_id).execute()
        data = att['data']
    file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
    load_dotenv()
    save_dir = os.getenv("PATH_TO_DOWNLOADED_FILES_FOLDER")
    path = os.path.join(save_dir, filename)
    with open(path, 'wb') as f:
        f.write(file_data)
    print(f"Attachment {filename} saved to {path}")

def fetch_attachments_of_unread_mail():

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(               
                # your creds file here. Please create json file as here https://cloud.google.com/docs/authentication/getting-started
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
        messages = results.get('messages',[])
        if not messages:
            print('No new messages.')
        else:
            message_count = 0
            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id']).execute()                
                email_data = msg['payload']['headers']
                for values in email_data:
                    name = values['name']
                    if name == 'From':
                        from_name= values['value']                      
                        for part in msg['payload']['parts']:
                            
                            if 'filename' in part and part['filename']:
                                save_attachment(service, msg, part)
                            try:
                                # mark the message as read (optional)
                                msg = service.users().messages().modify(userId='me', id=message['id'], body={'removeLabelIds': ['UNREAD']}).execute()                                                       
                            except BaseException as error:
                                print(error)
                                                            
    except Exception as error:
        print(f'An error occurred: {error}')
        