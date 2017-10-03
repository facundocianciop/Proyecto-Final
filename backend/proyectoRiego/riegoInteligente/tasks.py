# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

from celery import Celery
from celery.schedules import crontab

@shared_task(run_every=(crontab(minute='*/15')), name="some_task", ignore_result=True)
def add(x, y):
    print x + y
    return x + y
