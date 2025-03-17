from django.contrib.admin import AdminSite
from django.contrib.admin.models import LogEntry

class FlowAIAdminSite(AdminSite):
    def index(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        if 'log_entries' not in extra_context:
            extra_context['log_entries'] = LogEntry.objects.select_related('content_type', 'user')[:10]
        return super().index(request, extra_context)