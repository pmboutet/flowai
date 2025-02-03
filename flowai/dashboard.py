from django.urls import reverse

def custom_dashboard(request):
    """Custom dashboard configuration for Unfold admin"""
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