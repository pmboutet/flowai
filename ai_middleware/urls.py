from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.conversation_views import ConversationViewSet
from .views.base_views import BreakOutViewSet, SequenceViewSet
from .views.intermediate_views import SponsorViewSet, SessionViewSet
from .views.high_level_views import ProgrammeViewSet, ClientViewSet

router = DefaultRouter()

# Routes de base
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'breakouts', BreakOutViewSet, basename='breakout')
router.register(r'sequences', SequenceViewSet, basename='sequence')

# Routes intermédiaires
router.register(r'sponsors', SponsorViewSet, basename='sponsor')
router.register(r'sessions', SessionViewSet, basename='session')

# Routes de haut niveau
router.register(r'programmes', ProgrammeViewSet, basename='programme')
router.register(r'clients', ClientViewSet, basename='client')

# Configuration des URLs personnalisées
urlpatterns = [
    # API principale
    path('', include(router.urls)),
    
    # Routes pour l'authentification DRF
    path('auth/', include('rest_framework.urls')),
]