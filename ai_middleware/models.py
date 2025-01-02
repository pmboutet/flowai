from django.db import models
from django.utils import timezone

class Conversation(models.Model):
    PROVIDER_CHOICES = [
        ('grok', 'Grok'),
        ('openai', 'OpenAI')
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
    name = models.CharField(max_length=200)
    context = models.TextField(help_text='Contexte du client')
    objectives = models.TextField(help_text='Objectifs du client')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Programme(models.Model):
    name = models.CharField(max_length=200)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='programmes')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.client.name}'

class Sponsor(models.Model):
    name = models.CharField(max_length=200)
    job_title = models.CharField(max_length=200)
    objectives = models.TextField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='sponsors')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.job_title} ({self.client.name})'

class Session(models.Model):
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} - {self.client.name}'

class Sequence(models.Model):
    title = models.CharField(max_length=200)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='sequences')
    objective = models.TextField(help_text='Objectif de la séquence')
    input_drive_url = models.URLField(help_text='URL du dossier Google Drive contenant les inputs')
    input_text = models.TextField(help_text='Description des inputs')
    output_drive_url = models.URLField(help_text='URL du dossier Google Drive contenant les outputs')
    output_text = models.TextField(help_text='Description des outputs')
    order = models.IntegerField(help_text='Ordre de la séquence dans la session')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.title} - {self.session.title}'

class BreakOut(models.Model):
    title = models.CharField(max_length=200)
    sequence = models.ForeignKey(Sequence, on_delete=models.CASCADE, related_name='breakouts')
    description = models.TextField()
    objective = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} - {self.sequence.title}'