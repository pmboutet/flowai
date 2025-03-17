from django.contrib.admin.models import LogEntry
import types
from django.template.response import TemplateResponse
from django.template import loader

def add_log_entries(request, context):
    """Add log_entries to the context if not already present"""
    if 'log_entries' not in context:
        context['log_entries'] = LogEntry.objects.select_related('content_type', 'user')[:10]
    return context

def apply_patches():
    """
    Apply monkey patches to fix the log_entries issue
    """
    # No longer needed since we're not using Unfold
    # Just add a print statement to show this function was called
    print("Patches function called, but not applying any patches")
    pass