from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyectoRiego.settings')

app = Celery('proyectoRiego')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# redis-server /usr/local/etc/redis.conf
# celery -A proyectoRiego beat -l info
# celery -A proyectoRiego worker -l info


# noinspection PyUnusedLocal
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(30.0, obtener_mediciones_climaticas.s(), name='Obtener mediciones climaticas')

    sender.add_periodic_task(1.0, comprobar_riego_hora.s(), name='Comprobar inicio y fin riego por hora')

    # Calls test('world') every 30 seconds
    # sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    # sender.add_periodic_task(
    #    crontab(hour=7, minute=30, day_of_week=1),
    #    test.s('Happy Mondays!'),
    # )


@app.task
def obtener_mediciones_climaticas():
    from riegoInteligente.views.supportClases.procesosBackground.procesos_background import *
    obtener_mediciones_climaticas()


@app.task
def comprobar_riego_hora():
    from riegoInteligente.views.supportClases.procesosBackground.procesos_background import *
    comprobar_incio_riego_criterio_hora()
    comprobar_fin_riego_criterio_hora()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
