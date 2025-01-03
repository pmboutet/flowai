from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import uuid

class Conversation(models.Model):
    PROVIDER_CHOICES = [
        ('grok', 'Grok'),
        ('openai', 'OpenAI'),
        ('claude', 'Claude'),
        ('mistral', 'Mistral')
    ]
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    provider = models.CharField(max_length=10, choices=PROVIDER_CHOICES, default='grok')
    user_input = models.TextField()
    ai_response = models.TextField()
    prompt_tokens = models.IntegerField(default=0)
    completion_tokens = models.IntegerField(default=0)
    total_tokens = models.IntegerField(default=0)

    def __str__(self):
        return f'Conversation {self.id} - {self.provider} - {self.created_at}'

class Client(models.Model):
    STATUS_CHOICES = [
        ('normal', 'Normal'),
        ('deleted', 'Deleted'),
        ('archived', 'Archived'),
    ]

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200)
    context = models.TextField(help_text='Contexte du client')
    objectives = models.TextField(help_text='Objectifs du client')
    email = models.EmailField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='normal')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Programme(models.Model):
    STATUS_CHOICES = [
        ('normal', 'Normal'),
        ('deleted', 'Deleted'),
        ('archived', 'Archived'),
    ]

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='programmes')
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='normal')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.client.name}'

class Sponsor(models.Model):
    STATUS_CHOICES = [
        ('normal', 'Normal'),
        ('deleted', 'Deleted'),
        ('archived', 'Archived'),
    ]

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200)
    job_title = models.CharField(max_length=200)
    objectives = models.TextField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='sponsors')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='normal')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.job_title} ({self.client.name})'

class Session(models.Model):
    STATUS_CHOICES = [
        ('normal', 'Normal'),
        ('deleted', 'Deleted'),
        ('archived', 'Archived'),
    ]

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=200)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE, related_name='sessions', null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='sessions')
    context = models.TextField(help_text='Contexte de la session')
    objectives = models.TextField(help_text='Objectifs de la session')
    inputs = models.TextField(help_text='Inputs nécessaires')
    outputs = models.TextField(help_text='Outputs attendus')
    participants = models.TextField(help_text='Liste et description des participants')
    design_principles = models.TextField(help_text='Principes de design de la session')
    deliverables = models.TextField(help_text='Livrables attendus')
    sponsors = models.ManyToManyField(Sponsor, related_name='sessions')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='normal')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} - {self.client.name}'

class Sequence(models.Model):
    STATUS_CHOICES = [
        ('normal', 'Normal'),
        ('deleted', 'Deleted'),
        ('archived', 'Archived'),
    ]

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=200)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='sequences')
    objective = models.TextField(help_text='Objectif de la séquence')
    input_drive_url = models.URLField(help_text='URL du dossier Google Drive contenant les inputs', blank=True)
    input_text = models.TextField(help_text='Description des inputs')
    output_drive_url = models.URLField(help_text='URL du dossier Google Drive contenant les outputs', blank=True)
    output_text = models.TextField(help_text='Description des outputs')
    order = models.IntegerField(help_text='Ordre de la séquence dans la session')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='normal')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.title} - {self.session.title}'

class BreakOut(models.Model):
    STATUS_CHOICES = [
        ('normal', 'Normal'),
        ('deleted', 'Deleted'),
        ('archived', 'Archived'),
    ]

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=200)
    sequence = models.ForeignKey(Sequence, on_delete=models.CASCADE, related_name='breakouts')
    description = models.TextField()
    objective = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='normal')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} - {self.sequence.title}'

class UserGoogleAuth(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    google_id = models.CharField(max_length=100)
    access_token = models.TextField()
    refresh_token = models.TextField()
    token_expiry = models.DateTimeField()
    drive_enabled = models.BooleanField(default=False)

    def is_token_valid(self):
        return self.token_expiry > timezone.now()

    def __str__(self):
        return f'{self.user.email} - Google Auth'