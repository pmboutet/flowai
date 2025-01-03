from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ConversationViewSet,
    MarkdownExportView,
    MarkdownImportView,
    ClientViewSet,
    ProgrammeViewSet,
    SessionViewSet,
    SequenceViewSet,
    BreakOutViewSet
)

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'programmes', ProgrammeViewSet)
router.register(r'sessions', SessionViewSet)
router.register(r'sequences', SequenceViewSet)
router.register(r'breakouts', BreakOutViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('markdown/export/<uuid:uuid>/', MarkdownExportView.as_view(), name='markdown-export'),
    path('markdown/import/', MarkdownImportView.as_view(), name='markdown-import'),
]