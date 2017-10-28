# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task
def add(x, y):
    logger.info('Suma ejecutada')
    return x + y


@shared_task
def mul(x, y):
    logger.info('Multiplicacion ejecutada')
    return x * y


# noinspection PyBroadException
@shared_task
def accion_recepcion_medicion_sensor(oid_sector, oid_medicion_cabecera):
    try:
        from riegoInteligente.views.supportClases.procesosBackground.procesos_background import procesar_medicion_sensor
        print "Acciones recepcion medicion"
        procesar_medicion_sensor(oid_sector, oid_medicion_cabecera)
    except Exception:
        pass


# noinspection PyBroadException
@shared_task
def accion_recepcion_medicion_externa(oid_finca, oid_medicion_informacion_climatica_cabecera):
    try:
        from riegoInteligente.views.supportClases.procesosBackground.procesos_background import \
            procesar_medicion_informacion_climatica
        print "Acciones recepcion medicion externa"
        procesar_medicion_informacion_climatica(oid_finca, oid_medicion_informacion_climatica_cabecera)
    except Exception:
        pass


# noinspection PyBroadException
@shared_task
def envio_notificacion_evento(oid_configuracion_evento, mensaje=None):
    try:
        from riegoInteligente.views.supportClases.procesosBackground.procesos_background import \
            enviar_notificacion_evento_personalizado
        print "Envio notificacion evento"
        enviar_notificacion_evento_personalizado(oid_configuracion_evento, mensaje=mensaje)
    except Exception:
        pass


# noinspection PyUnusedLocal,PyBroadException
@shared_task
def envio_notificacion_riego(oid_ejecucion_riego, mensaje):
    try:
        print "Envio notificacion riego"
    except Exception:
        pass
