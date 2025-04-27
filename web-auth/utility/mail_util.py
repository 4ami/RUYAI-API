from jinja2 import Environment, FileSystemLoader
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv
import os
import base64
load_dotenv()


env = Environment(loader=FileSystemLoader('template'))

class MailUtil:
    SCOPE=['https://www.googleapis.com/auth/gmail.modify']
    cred = None
    service = None

    @classmethod
    def authenticate(self):
        if self.service:
            return self.service
        
        token_path = os.getenv('TOKEN_PATH')
        credentials_path = os.getenv('CREDENTIALS_PATH')

        if os.path.exists(token_path):
            self.cred = Credentials.from_authorized_user_file(token_path, self.SCOPE)
        
        if not self.cred or not self.cred.valid:
            if self.cred and self.cred.expired and self.cred.refresh_token:
                self.cred.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, self.SCOPE)
                self.cred = flow.run_local_server(port=3004)
            
            with open(token_path, 'w') as token:
                token.write(self.cred.to_json())
        
        self.service = build('gmail', 'v1', credentials=self.cred)
        return self.service

    @staticmethod
    def create_message(to:str, subject:str, html_content:str)->dict[str, str]:
        message:MIMEText = MIMEText(html_content, 'html')
        message['to'] = to
        message['from'] = os.getenv('EMAIL_ID')
        message['subject'] = subject
        encoded:str = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        return {'raw': encoded}


    @classmethod
    async def send_reset(self, to:str, link:str):
        template = env.get_template('forget_password.html')
        html_contetn:str = template.render(reset_link=link)
        service = self.authenticate()

        message= self.create_message(to=to, subject='Password Reset Request', html_content=html_contetn)
        service.users().messages().send(userId='me', body=message).execute()

    @classmethod
    async def send_unlock(self, to:str, link:str):
        template = env.get_template('unlock_account.html')
        html_content:str = template.render(unlock_link=link)
        message = self.create_message(to=to, subject='Unlock Account Request', html_content=html_content)

        service = self.authenticate()
        service.users().messages().send(userId='me', body=message).execute()