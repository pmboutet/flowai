from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import (Client, Programme, Sponsor, Session,
                    Sequence, BreakOut, Conversation)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'total_sessions', 'total_programmes', 'total_sponsors', 'created_at']
    search_fields = ['name', 'context', 'objectives']
    list_filter = ['created_at']
    
    def total_sessions(self, obj):
        return obj.sessions.count()
    
    def total_programmes(self, obj):
        return obj.programmes.count()
    
    def total_sponsors(self, obj):
        return obj.sponsors.count()
    
    total_sessions.short_description = 'Sessions'
    total_programmes.short_description = 'Programmes'
    total_sponsors.short_description = 'Sponsors'

@admin.register(Programme)
class ProgrammeAdmin(admin.ModelAdmin):
    list_display = ['name', 'client', 'total_sessions', 'created_at']
    list_filter = ['client', 'created_at']
    search_fields = ['name', 'description']
    
    def total_sessions(self, obj):
        return obj.sessions.count()
    total_sessions.short_description = 'Sessions'

@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ['name', 'job_title', 'client', 'created_at']
    list_filter = ['client', 'created_at']
    search_fields = ['name', 'job_title', 'objectives']

class SequenceInline(admin.TabularInline):
    model = Sequence
    extra = 1
    ordering = ['order']

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'client', 'programme', 'total_sequences', 'created_at']
    list_filter = ['client', 'programme', 'created_at']
    search_fields = ['title', 'context', 'objectives']
    filter_horizontal = ['sponsors']
    inlines = [SequenceInline]
    
    def total_sequences(self, obj):
        return obj.sequences.count()
    total_sequences.short_description = 'Sequences'

class BreakOutInline(admin.TabularInline):
    model = BreakOut
    extra = 1

@admin.register(Sequence)
class SequenceAdmin(admin.ModelAdmin):
    list_display = ['title', 'session', 'order', 'total_breakouts', 'drive_links', 'created_at']
    list_filter = ['session__client', 'session', 'created_at']
    search_fields = ['title', 'objective']
    ordering = ['session', 'order']
    inlines = [BreakOutInline]
    
    def total_breakouts(self, obj):
        return obj.breakouts.count()
    
    def drive_links(self, obj):
        links = []
        if obj.input_drive_url:
            links.append(format_html('<a href="{}" target="_blank">📥 Inputs</a>', obj.input_drive_url))
        if obj.output_drive_url:
            links.append(format_html('<a href="{}" target="_blank">📤 Outputs</a>', obj.output_drive_url))
        return format_html(' | '.join(links) if links else '-')
    
    total_breakouts.short_description = 'Breakouts'
    drive_links.short_description = 'Google Drive'

@admin.register(BreakOut)
class BreakOutAdmin(admin.ModelAdmin):
    list_display = ['title', 'sequence', 'get_session', 'get_client', 'created_at']
    list_filter = ['sequence__session__client', 'sequence__session', 'created_at']
    search_fields = ['title', 'description', 'objective']
    
    def get_session(self, obj):
        return obj.sequence.session
    
    def get_client(self, obj):
        return obj.sequence.session.client
    
    get_session.short_description = 'Session'
    get_client.short_description = 'Client'

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'provider', 'truncated_input', 'total_tokens', 'created_at']
    list_filter = ['provider', 'created_at']
    search_fields = ['user_input', 'ai_response']
    readonly_fields = ['created_at', 'updated_at', 'prompt_tokens', 
                      'completion_tokens', 'total_tokens']
    
    def truncated_input(self, obj):
        return (obj.user_input[:75] + '...') if len(obj.user_input) > 75 else obj.user_input
    truncated_input.short_description = 'Input'

# Personnalisation de l'interface d'administration
admin.site.site_header = 'Administration FlowAI'
admin.site.site_title = 'FlowAI Admin'
admin.site.index_title = 'Tableau de bord FlowAI'