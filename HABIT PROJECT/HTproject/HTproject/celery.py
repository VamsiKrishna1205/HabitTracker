# from __future__ import absolute_import
# import os
# from celery import Celery

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HTproject.settings')
# app = Celery('HTproject')
# app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks()


from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HTproject.settings')

app = Celery('HTproject')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# Namespace 'CELERY' means all celery-related configs must have 'CELERY_' prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks in installed apps.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')