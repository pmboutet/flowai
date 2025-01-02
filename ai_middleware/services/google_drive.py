from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from django.conf import settings
from ..models import UserGoogleAuth

class GoogleDriveService:
    def __init__(self, user):
        self.user = user
        self.google_auth = UserGoogleAuth.objects.get(user=user)
        self.credentials = self._get_credentials()

    def _get_credentials(self):
        return Credentials(
            token=self.google_auth.access_token,
            refresh_token=self.google_auth.refresh_token,
            token_uri='https://oauth2.googleapis.com/token',
            client_id=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
            client_secret=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
            scopes=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE
        )

    def create_folder(self, name, parent_id=None):
        service = build('drive', 'v3', credentials=self.credentials)
        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder'
        }

        if parent_id:
            file_metadata['parents'] = [parent_id]

        folder = service.files().create(
            body=file_metadata,
            fields='id, webViewLink'
        ).execute()

        return folder

    def share_file(self, file_id, email, role='reader'):
        service = build('drive', 'v3', credentials=self.credentials)
        batch = service.new_batch_http_request()

        user_permission = {
            'type': 'user',
            'role': role,
            'emailAddress': email
        }

        batch.add(service.permissions().create(
            fileId=file_id,
            body=user_permission,
            fields='id',
            sendNotificationEmail=True
        ))

        batch.execute()

    def get_file_metadata(self, file_id):
        service = build('drive', 'v3', credentials=self.credentials)
        return service.files().get(
            fileId=file_id,
            fields='id, name, webViewLink, mimeType'
        ).execute()