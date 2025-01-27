from django.contrib import admin
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.admin import TokenAdmin
from .models import Client, Programme, Session, Sequence, BreakOut

# Register Token model for API key management
admin.site.register(Token, TokenAdmin)

# Register the application models
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'uuid')
    search_fields = ('name',)

@admin.register(Programme)
class ProgrammeAdmin(admin.ModelAdmin):
    list_display = ('name', 'client', 'uuid')
    list_filter = ('client',)
    search_fields = ('name',)

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'programme', 'client', 'uuid')
    list_filter = ('programme', 'client')
    search_fields = ('title',)

@admin.register(Sequence)
class SequenceAdmin(admin.ModelAdmin):
    list_display = ('title', 'session', 'order', 'uuid')
    list_filter = ('session',)
    search_fields = ('title',)
    ordering = ('session', 'order')

@admin.register(BreakOut)
class BreakOutAdmin(admin.ModelAdmin):
    list_display = ('title', 'sequence', 'uuid')
    list_filter = ('sequence',)
    search_fields = ('title',)