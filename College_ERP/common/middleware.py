import threading
from django.contrib.contenttypes.models import ContentType
from django.utils.deprecation import MiddlewareMixin
from .models import AuditLog
import json


_user = threading.local()


def get_current_user():
    """Get current user from thread local storage"""
    return getattr(_user, 'user', None)


def set_current_user(user):
    """Set current user in thread local storage"""
    _user.user = user


class AuditMiddleware(MiddlewareMixin):
    """Middleware to track user for audit logging"""
    
    def process_request(self, request):
        set_current_user(request.user if hasattr(request, 'user') and request.user.is_authenticated else None)
        return None

    def process_response(self, request, response):
        set_current_user(None)
        return response


def log_model_change(sender, instance, created=False, **kwargs):
    """Signal handler to log model changes"""
    user = get_current_user()
    action = 'create' if created else 'update'
    
    # Get before data for updates (would need to be stored in instance)
    before_data = getattr(instance, '_audit_before_data', None) if not created else None
    after_data = {}
    
    # Serialize model data
    for field in instance._meta.fields:
        try:
            value = getattr(instance, field.name)
            if hasattr(value, 'isoformat'):  # DateTime fields
                value = value.isoformat()
            elif hasattr(value, 'pk'):  # Foreign key fields
                value = value.pk
            after_data[field.name] = value
        except:
            continue
    
    AuditLog.objects.create(
        actor=user,
        action=action,
        content_type=ContentType.objects.get_for_model(instance),
        object_id=instance.pk,
        before_data=before_data,
        after_data=after_data,
        ip_address=getattr(_user, 'ip_address', None),
        user_agent=getattr(_user, 'user_agent', '')
    )