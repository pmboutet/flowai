from django.urls import reverse
from django.contrib.admin.models import LogEntry

def custom_dashboard(request, context=None):
    """Custom dashboard configuration for Unfold admin"""
    # Ensure context is a dictionary
    if context is None:
        context = {}
        
    # Add log_entries to context if not already present
    if 'log_entries' not in context:
        context['log_entries'] = LogEntry.objects.select_related('content_type', 'user')[:10]
        
    # Return dashboard configuration
    return {
        'cards': [],  # List of cards to display on the dashboard
        'panels': [],  # Custom panels
        'navigation': [  # Custom navigation
            {
                'title': 'Applications',
                'items': [
                    {
                        'title': 'AI Middleware',
                        'icon': 'robot',  # Icon to display
                        'url': reverse('admin:app_list', args=('ai_middleware',)),
                    },
                ],
            },
        ],
    }