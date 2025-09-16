from django.contrib import admin
from .models import AuditLog, Settings, Attachment, NumberSequence


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'actor', 'action', 'content_type', 'object_id']
    list_filter = ['action', 'content_type', 'timestamp']
    search_fields = ['actor__username', 'actor__email']
    readonly_fields = ['timestamp', 'actor', 'action', 'content_type', 'object_id', 
                      'before_data', 'after_data', 'ip_address', 'user_agent']
    date_hierarchy = 'timestamp'
    ordering = ['-timestamp']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ['key', 'value', 'description', 'updated_at']
    search_fields = ['key', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'label', 'content_type', 'file_size', 'uploaded_at', 'uploaded_by']
    list_filter = ['content_type', 'uploaded_at']
    search_fields = ['name', 'label']
    readonly_fields = ['file_size', 'mime_type', 'uploaded_at', 'uploaded_by']


@admin.register(NumberSequence)
class NumberSequenceAdmin(admin.ModelAdmin):
    list_display = ['prefix', 'year', 'current_number', 'format_string', 'description']
    list_filter = ['year', 'prefix']
    search_fields = ['prefix', 'description']
    readonly_fields = ['current_number']