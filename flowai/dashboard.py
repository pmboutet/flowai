from django.urls import reverse
from django.contrib.admin.models import LogEntry

def custom_dashboard(request, context=None):
    """Custom dashboard configuration for Unfold admin"""
    # Return the dashboard data without modifying the context
    # The log_entries will be handled by another part of the application
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