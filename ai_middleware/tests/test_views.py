from django.test import TestCase, Client as TestClient
from django.urls import reverse
from ..models import Client, Session
from rest_framework import status

class MarkdownViewsTests(TestCase):
    def setUp(self):
        self.client = TestClient()
        self.test_client = Client.objects.create(
            name='Test Client',
            context='Test Context',
            objectives='Test Objectives'
        )
        self.session = Session.objects.create(
            title='Test Session',
            client=self.test_client,
            context='Test Context',
            objectives='Test Objectives',
            inputs='Test Inputs',
            outputs='Test Outputs',
            participants='Test Participants',
            design_principles='Test Principles',
            deliverables='Test Deliverables'
        )

    def test_markdown_export(self):
        url = reverse('markdown-export', kwargs={
            'model_type': 'client',
            'uuid': self.test_client.uuid
        })
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('markdown', response.data)
        self.assertIn(f'[@Client::{self.test_client.uuid}]', response.data['markdown'])
        
    def test_markdown_import(self):
        url = reverse('markdown-import')
        markdown = f"""# [@Client::{self.test_client.uuid}]
**name**: Updated Client
**context**: Updated Context"""
        
        response = self.client.post(url, {'markdown': markdown}, content_type='application/json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.test_client.refresh_from_db()
        self.assertEqual(self.test_client.name, 'Updated Client')
        
    def test_markdown_export_invalid_type(self):
        url = reverse('markdown-export', kwargs={
            'model_type': 'invalid',
            'uuid': self.test_client.uuid
        })
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_markdown_import_invalid(self):
        url = reverse('markdown-import')
        response = self.client.post(url, {'markdown': 'Invalid markdown'}, content_type='application/json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)