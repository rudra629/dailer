# caller/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'caller.settings')
app = Celery('caller')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()