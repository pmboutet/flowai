from django.urls import reverse
from django.contrib.admin.models import LogEntry

def custom_dashboard(request, context=None):
    """Custom dashboard configuration for Unfold admin"""
    # Make sure context exists
    if context is None:
        context = {}
    
    # Add log_entries to context if not already present
    if 'log_entries' not in context:
        context['log_entries'] = LogEntry.objects.select_related('content_type', 'user')[:10]
    
    # Return the dashboard configuration
    return {
        'cards': [],  # Liste des cartes à afficher sur le dashboard
        'panels': [],  # Panneaux personnalisés
        'navigation': [  # Navigation personnalisée
            {
                'title': 'Applications',
                'items': [
                    {
                        'title': 'AI Middleware',
                        'icon': 'robot',  # Icône à afficher
                        'url': reverse('admin:app_list', args=('ai_middleware',)),
                    },
                ],
            },
        ],
    }