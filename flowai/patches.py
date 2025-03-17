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
    # Store the original TemplateResponse render method
    original_render = TemplateResponse.render
    
    # Define a new render method that adds log_entries to the context
    def patched_render(self):
        # Add log_entries to the context
        self.context_data = add_log_entries(self._request, self.context_data)
        # Call the original render method
        return original_render(self)
    
    # Replace the method
    TemplateResponse.render = patched_render
    
    # Also patch the get_template method to handle missing templates
    original_get_template = loader.get_template
    
    def patched_get_template(template_name, using=None):
        # Check if this is the problematic template
        if template_name == 'unfold/index.html':
            try:
                # Try to load the original template
                return original_get_template(template_name, using)
            except Exception:
                # If it fails, fall back to the admin template
                print(f"Warning: Template '{template_name}' not found, falling back to admin/index.html")
                return original_get_template('admin/index.html', using)
        # For all other templates, use the original method
        return original_get_template(template_name, using)
    
    # Replace the method
    loader.get_template = patched_get_template
    
    print("Applied patches to TemplateResponse.render and loader.get_template")
