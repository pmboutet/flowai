from django.urls import path
from .views import MarkdownExportView, MarkdownImportView

urlpatterns = [
    path('markdown/export/<str:model_type>/<uuid:uuid>/', MarkdownExportView.as_view(), name='markdown-export'),
    path('markdown/import/', MarkdownImportView.as_view(), name='markdown-import'),
]