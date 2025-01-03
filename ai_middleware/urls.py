from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MarkdownExportView, MarkdownImportView

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('markdown/export/<str:model_type>/<uuid:uuid>/', MarkdownExportView.as_view(), name='markdown-export'),
    path('markdown/import/', MarkdownImportView.as_view(), name='markdown-import'),
]