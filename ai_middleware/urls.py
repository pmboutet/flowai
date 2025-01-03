from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
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

class CustomRouter(DefaultRouter):
    def get_api_root_view(self, api_urls=None):
        api_root_dict = {}
        list_name = self.routes[0].name
        for prefix, viewset, basename in self.registry:
            api_root_dict[prefix] = list_name.format(basename=basename)
        api_root_dict['markdown/export'] = 'markdown-export'
        api_root_dict['markdown/import'] = 'markdown-import'
        return self.APIRootView.as_view(api_root_dict=api_root_dict)

router = CustomRouter()
router.register(r'conversations', ConversationViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'programmes', ProgrammeViewSet)
router.register(r'sessions', SessionViewSet)
router.register(r'sequences', SequenceViewSet)
router.register(r'breakouts', BreakOutViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('markdown/export/<str:model_type>/<uuid:uuid>/', MarkdownExportView.as_view(), name='markdown-export'),
    path('markdown/import/', MarkdownImportView.as_view(), name='markdown-import'),
]