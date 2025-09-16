import uuid
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone
import json


class BaseModel(models.Model):
    """Base model with common fields"""
    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AuditLog(models.Model):
    """Audit log for tracking all model changes"""
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=20, choices=[
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('view', 'View'),
    ])
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    before_data = models.JSONField(null=True, blank=True)
    after_data = models.JSONField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['actor', 'timestamp']),
            models.Index(fields=['action', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.action} {self.content_type} by {self.actor} at {self.timestamp}"


class Settings(models.Model):
    """System settings key-value store"""
    key = models.CharField(max_length=255, unique=True)
    value = models.TextField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Settings"

    def __str__(self):
        return f"{self.key}: {self.value[:50]}"

    @classmethod
    def get(cls, key, default=None):
        try:
            return cls.objects.get(key=key).value
        except cls.DoesNotExist:
            return default

    @classmethod
    def set(cls, key, value, description=''):
        obj, created = cls.objects.get_or_create(
            key=key, 
            defaults={'value': str(value), 'description': description}
        )
        if not created:
            obj.value = str(value)
            if description:
                obj.description = description
            obj.save()
        return obj


class Attachment(models.Model):
    """Generic file attachment model"""
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    file = models.FileField(upload_to='attachments/%Y/%m/')
    name = models.CharField(max_length=255)
    label = models.CharField(max_length=100, blank=True)
    file_size = models.PositiveIntegerField(null=True)
    mime_type = models.CharField(max_length=100, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.name} ({self.label})"

    def save(self, *args, **kwargs):
        if self.file and not self.file_size:
            self.file_size = self.file.size
        if not self.name and self.file:
            self.name = self.file.name
        super().save(*args, **kwargs)


class NumberSequence(models.Model):
    """Centralized number sequence management"""
    prefix = models.CharField(max_length=10, unique=True)
    current_number = models.PositiveIntegerField(default=0)
    year = models.PositiveIntegerField(default=timezone.now().year)
    format_string = models.CharField(max_length=50, default='{prefix}/{year:04d}/{seq:05d}')
    description = models.CharField(max_length=255)

    class Meta:
        unique_together = ['prefix', 'year']

    def __str__(self):
        return f"{self.prefix} - {self.current_number}"

    @classmethod
    def get_next_number(cls, prefix, year=None, reset_yearly=True):
        """Get next number in sequence"""
        if year is None:
            year = timezone.now().year
        
        obj, created = cls.objects.get_or_create(
            prefix=prefix,
            year=year,
            defaults={'current_number': 0, 'description': f'{prefix} sequence for {year}'}
        )
        
        # Reset counter for new year if reset_yearly is True
        if reset_yearly and obj.year != year:
            obj.year = year
            obj.current_number = 0
        
        obj.current_number += 1
        obj.save()
        
        return obj.format_string.format(
            prefix=prefix,
            year=year,
            seq=obj.current_number
        ), obj.current_number