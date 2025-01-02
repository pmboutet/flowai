from django.db import models
from django.utils import timezone

class Conversation(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    user_input = models.TextField()
    ai_response = models.TextField()
    prompt_tokens = models.IntegerField(default=0)
    completion_tokens = models.IntegerField(default=0)
    total_tokens = models.IntegerField(default=0)

    def __str__(self):
        return f'Conversation {self.id} - {self.created_at}'