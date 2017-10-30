from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
from celery.schedules import crontab

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
# celery -A proyectoRiego purge


# noinspection PyUnusedLocal
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    # Llamar cada 30 segundos
    sender.add_periodic_task(60.0, obtener_mediciones_climaticas.s(), name='Obtener mediciones climaticas')

    # Llamar cada 2 segundos
    sender.add_periodic_task(2.0, comprobar_riego_hora.s(), name='Comprobar inicio y fin riego por hora y volumen')

    # Llamar todos los dias a las 12
    sender.add_periodic_task(
        crontab(minute=0, hour=5),
        aprendizaje_actualizar_dataset.s(),
    )

    # Llamar cada 15 min
    sender.add_periodic_task(
        crontab(minute='*/15'),
        aprendizaje_control_ejecucion_riego.s(),
    )


    # Calls test('world') every 30 seconds
    # sender.add_periodic_task(30.0, test.s('world'), expires=10)
    # http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html


@app.task
def obtener_mediciones_climaticas():
    from riegoInteligente.views.supportClases.procesosBackground.procesos_background import \
        obtener_mediciones_climaticas
    obtener_mediciones_climaticas()


@app.task
def comprobar_riego_hora():
    from riegoInteligente.views.supportClases.procesosBackground.procesos_background import \
        comprobar_fin_riego_criterio_hora_volumen
    # comprobar_incio_riego_criterio_hora()
    comprobar_fin_riego_criterio_hora_volumen()


@app.task
def aprendizaje_actualizar_dataset():
    from riegoInteligente.views.supportClases.procesosBackground.procesos_aprendizaje import \
        proceso_actualizar_data_set
    proceso_actualizar_data_set()


@app.task
def aprendizaje_control_ejecucion_riego():
    from riegoInteligente.views.supportClases.procesosBackground.procesos_aprendizaje import \
        proceso_controlar_ejecucion_riego_por_aprendizaje
    proceso_controlar_ejecucion_riego_por_aprendizaje()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
