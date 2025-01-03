from django.contrib import admin
from django.contrib.auth.models import User
from unfold.admin import ModelAdmin
from .models import (
    Conversation,
    Client,
    Programme,
    Sponsor,
    Session,
    Sequence,
    BreakOut,
    UserGoogleAuth
)

@admin.register(Conversation)
class ConversationAdmin(ModelAdmin):
    list_display = ('id', 'provider', 'created_at', 'total_tokens')
    list_filter = ('provider', 'created_at')
    search_fields = ('user_input', 'ai_response')
    ordering = ('-created_at',)

@admin.register(Client)
class ClientAdmin(ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email', 'context', 'objectives')
    ordering = ('name',)

@admin.register(Programme)
class ProgrammeAdmin(ModelAdmin):
    list_display = ('name', 'client', 'created_at')
    list_filter = ('client',)
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(Sponsor)
class SponsorAdmin(ModelAdmin):
    list_display = ('name', 'job_title', 'client')
    list_filter = ('client',)
    search_fields = ('name', 'job_title', 'objectives')
    ordering = ('name',)

@admin.register(Session)
class SessionAdmin(ModelAdmin):
    list_display = ('title', 'client', 'programme', 'user', 'created_at')
    list_filter = ('client', 'programme', 'user')
    search_fields = ('title', 'context', 'objectives')
    filter_horizontal = ('sponsors',)
    ordering = ('-created_at',)

@admin.register(Sequence)
class SequenceAdmin(ModelAdmin):
    list_display = ('title', 'session', 'order', 'user', 'created_at')
    list_filter = ('session', 'user')
    search_fields = ('title', 'objective')
    ordering = ('session', 'order')

@admin.register(BreakOut)
class BreakOutAdmin(ModelAdmin):
    list_display = ('title', 'sequence', 'created_at')
    list_filter = ('sequence',)
    search_fields = ('title', 'description', 'objective')
    ordering = ('sequence', 'title')

@admin.register(UserGoogleAuth)
class UserGoogleAuthAdmin(ModelAdmin):
    list_display = ('user', 'drive_enabled', 'token_expiry')
    list_filter = ('drive_enabled',)
    search_fields = ('user__username', 'user__email')
    ordering = ('user',)