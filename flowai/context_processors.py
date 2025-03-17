from django.contrib.admin.models import LogEntry

def admin_log_entries(request):
    """
    Adds log_entries to the template context for admin pages
    """
    return {
        'log_entries': LogEntry.objects.all()[:10]
    }