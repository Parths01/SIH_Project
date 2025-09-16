from celery import Celery
import os

# Set default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'College_ERP.settings')

app = Celery('College_ERP')

# Load configuration from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all Django apps
app.autodiscover_tasks()

# Celery Beat Schedule for periodic tasks
app.conf.beat_schedule = {
    'daily-snapshot': {
        'task': 'dashboards.tasks.create_daily_snapshot',
        'schedule': 86400.0,  # Run daily at midnight
    },
    'send-fee-reminders': {
        'task': 'finance.tasks.send_fee_reminders',
        'schedule': 3600.0,  # Run every hour
    },
    'backup-database': {
        'task': 'common.tasks.backup_database',
        'schedule': 43200.0,  # Run twice daily
    },
    'process-alerts': {
        'task': 'dashboards.tasks.process_alert_rules',
        'schedule': 300.0,  # Run every 5 minutes
    },
}

app.conf.timezone = 'Asia/Kolkata'