from django.test import TestCase
from django.utils import timezone
from ..models import Client, Programme, Session, Sequence, BreakOut
from ..services import to_markdown, from_markdown
import uuid

class MarkdownServiceTests(TestCase):
    def setUp(self):
        # Create test data
        self.client = Client.objects.create(
            name='Test Client',
            context='Test Context',
            objectives='Test Objectives'
        )
        
        self.programme = Programme.objects.create(
            name='Test Programme',
            client=self.client,
            description='Test Description'
        )
        
        self.session = Session.objects.create(
            title='Test Session',
            programme=self.programme,
            client=self.client,
            context='Test Context',
            objectives='Test Objectives',
            inputs='Test Inputs',
            outputs='Test Outputs',
            participants='Test Participants',
            design_principles='Test Principles',
            deliverables='Test Deliverables'
        )
        
        self.sequence = Sequence.objects.create(
            title='Test Sequence',
            session=self.session,
            objective='Test Objective',
            input_text='Test Input',
            output_text='Test Output',
            order=1
        )
        
        self.breakout = BreakOut.objects.create(
            title='Test Breakout',
            sequence=self.sequence,
            description='Test Description',
            objective='Test Objective'
        )

    def test_to_markdown(self):
        # Test client to markdown
        markdown = to_markdown(self.client.uuid, 'client')
        self.assertIn(f'[@Client::{self.client.uuid}]', markdown)
        self.assertIn('Test Client', markdown)
        self.assertIn('Test Programme', markdown)

        # Test programme to markdown
        markdown = to_markdown(self.programme.uuid, 'programme')
        self.assertIn(f'[@Programme::{self.programme.uuid}]', markdown)
        self.assertIn('Test Session', markdown)

    def test_from_markdown_create(self):
        markdown = f"""# [@Client::{uuid.uuid4()}]
**name**: New Client
**context**: New Context
**objectives**: New Objectives
"""
        objects = from_markdown(markdown)
        self.assertEqual(len(objects), 1)
        self.assertEqual(objects[0].name, 'New Client')

    def test_from_markdown_update(self):
        markdown = f"""# [@Client::{self.client.uuid}]
**name**: Updated Client
**context**: Updated Context
**objectives**: Updated Objectives
"""
        objects = from_markdown(markdown)
        self.assertEqual(len(objects), 1)
        self.client.refresh_from_db()
        self.assertEqual(self.client.name, 'Updated Client')

    def test_from_markdown_delete(self):
        # Create markdown without the breakout
        markdown = f"""# [@Session::{self.session.uuid}]
**title**: Test Session

# [@Sequence::{self.sequence.uuid}]
**title**: Test Sequence
"""
        from_markdown(markdown)
        
        # Check if breakout is marked as deleted
        self.breakout.refresh_from_db()
        self.assertEqual(self.breakout.status, 'deleted')
