from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_project.settings')

app = Celery('celery_project')
app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Kolkata')
app.config_from_object(settings, namespace='CELERY')


# CELERY BEAT SETTINGS
app.conf.beat_schedule = {
    'create_game_round_after_every_30_second': {
        'task': 'club.tasks.test_func',
        # 'schedule': crontab(hour=12 , minute=48),
        'schedule': 30.0,
        # 'args': () 
    }
}


app.autodiscover_tasks()
@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")