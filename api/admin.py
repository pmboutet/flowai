from django.contrib import admin
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.admin import TokenAdmin
from .models import Client, Programme, Session, Sequence, BreakOut

# Register Token model for API key management
admin.site.register(Token, TokenAdmin)

# Register your models
admin.site.register(Client)
admin.site.register(Programme)
admin.site.register(Session)
admin.site.register(Sequence)
admin.site.register(BreakOut)
