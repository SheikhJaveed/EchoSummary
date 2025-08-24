import os
import re
from typing import Tuple
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying scopes, delete token.json.
SCOPES = ['https://www.googleapis.com/auth/documents']

def _get_creds():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                raise RuntimeError("Missing credentials.json for Google OAuth. Place it in project root.")
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def clean_markdown(text: str) -> str:
    # Remove bold (**text** → text)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    # Remove italic (*text* → text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    # Remove headers (#, ##, ### → just keep text)
    text = re.sub(r'#+\s', '', text)
    # Remove leading list markers (*, -, +) while keeping content
    text = re.sub(r'^[\*\-\+]\s+', '', text, flags=re.MULTILINE)
    return text.strip()


def create_doc_with_text(title: str, markdown_text: str) -> str:
    creds = _get_creds()
    docs = build('docs', 'v1', credentials=creds)

    # 1) Create the doc
    doc = docs.documents().create(body={'title': title}).execute()
    doc_id = doc.get('documentId')

    # 2) Clean markdown before inserting
    plain_text = clean_markdown(markdown_text)

    requests = [{
        'insertText': {
            'location': {'index': 1},
            'text': plain_text
        }
    }]
    docs.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()

    # 3) Print preview (also cleaned)
    print("\nSummary preview:\n")
    print(plain_text)

    return f"https://docs.google.com/document/d/{doc_id}/edit"
