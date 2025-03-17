from django.contrib.admin.models import LogEntry

class LogEntriesMiddleware:
    """Middleware to add log entries to the request"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Code to run before the view
        # Only for admin URLs
        if request.path.startswith('/admin/'):
            # Add log entries to the request
            request.log_entries = LogEntry.objects.select_related('content_type', 'user')[:10]
            
        response = self.get_response(request)
        
        # Code to run after the view
        return response