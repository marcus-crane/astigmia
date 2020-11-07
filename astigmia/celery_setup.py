import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'astigmia.settings')

app = Celery('astigmia')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-next-session': {
        'task': 'lobby.check-next-session',
        'schedule': 60 * 60 * 3
    },
    'fetch-notifications': {
        'task': 'dashboard.fetch-notifications',
        'schedule': 60 * 5
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
