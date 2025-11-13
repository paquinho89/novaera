import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    creds = None
    token_path = os.path.join('credentials', 'token.json')

    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.path.join('newsletter', 'credentials', 'credentials.json'), SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)


def send_gmail_message(to_emails, subject, html_content, text_content=None, attachments=None):
    """Envía un correo HTML con Gmail API"""
    service = get_gmail_service()
    message = MIMEMultipart('mixed')
    message['to'] = ', '.join(to_emails)
    message['subject'] = subject

    # Parte alternativa: texto + HTML
    alternative_part = MIMEMultipart('alternative')
    if text_content:
        alternative_part.attach(MIMEText(text_content, 'plain'))
    alternative_part.attach(MIMEText(html_content, 'html'))
    message.attach(alternative_part)

    # Engadir adxuntos (imaxes ou ficheiros)
    if attachments:
        for path in attachments:
            with open(path, 'rb') as f:
                if path.endswith('.png') or path.endswith('.jpg'):
                    part = MIMEImage(f.read())
                else:
                    part = MIMEApplication(f.read())
                part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(path))
                message.attach(part)

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return service.users().messages().send(userId='me', body={'raw': raw}).execute()
