from django.contrib.admin.models import LogEntry
from django.template.context_processors import log as log_processor
import types

def apply_patches():
    """
    Apply monkey patches to fix the log_entries issue
    """
    try:
        # Try to import the Unfold admin site
        from unfold.admin import UnfoldAdminSite
        
        # Store the original index method
        original_index = UnfoldAdminSite.index
        
        # Define a new index method that adds log_entries to the context
        def patched_index(self, request, extra_context=None):
            if extra_context is None:
                extra_context = {}
            if 'log_entries' not in extra_context:
                extra_context['log_entries'] = LogEntry.objects.select_related('content_type', 'user')[:10]
            return original_index(self, request, extra_context)
        
        # Replace the method
        UnfoldAdminSite.index = patched_index
        
        print("Patched UnfoldAdminSite.index to include log_entries")
    except ImportError:
        print("Could not patch UnfoldAdminSite - module not found")
    except Exception as e:
        print(f"Error patching UnfoldAdminSite: {e}")
