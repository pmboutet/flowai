from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# ... [autres modèles existants] ...

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

# Ajout du champ user aux modèles existants
class Session(models.Model):
    # ... [champs existants] ...
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class Sequence(models.Model):
    # ... [champs existants] ...
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)