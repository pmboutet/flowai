from django.contrib import admin
from django.contrib.admin.models import LogEntry

# Register the LogEntry model so it's visible in the admin
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('action_time', 'user', 'content_type', 'object_repr', 'action_flag')
    list_filter = ('action_time', 'user', 'content_type')
    search_fields = ('object_repr', 'change_message')
    readonly_fields = ('action_time', 'user', 'content_type', 'object_repr', 'action_flag', 'change_message', 'object_id')
    date_hierarchy = 'action_time'
    
    def has_add_permission(self, request):
        return False
        
    def has_change_permission(self, request, obj=None):
        return False
        
    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(LogEntry, LogEntryAdmin)
