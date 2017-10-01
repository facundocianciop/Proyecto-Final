from datetime import datetime
import pytz

from ...models import EjecucionRiego, EstadoEjecucionRiego
from views_constants import *


def iniciar_ejecucion_riego(mecanismo_riego_finca_sector, detalle_riego):
    """
    Iniciar una ejecucion de riego de un mecanismo_riego_finca_sector
    :param mecanismo_riego_finca_sector:
    :param detalle_riego:
    :return:
    """
    estado_ejecucion_riego_en_ejecucion = EstadoEjecucionRiego.objects.get(
        nombreEstadoEjecucionRiego=ESTADO_EN_EJECUCION)

    ejecucion_riego_nuevo = EjecucionRiego(
        mecanismo_riego_finca_sector=mecanismo_riego_finca_sector,
        fecha_hora_inicio=datetime.now(pytz.utc),
        detalle=detalle_riego,
        estado_ejecucion_riego=estado_ejecucion_riego_en_ejecucion
    )
    # TODO llamar a adaptador mecanismo riego y ejecutar riego
    ejecucion_riego_nuevo.save()

    return ejecucion_riego_nuevo


def resumir_riego(ejecucion_riego):
    """
    Reiniciar una ejecucion de riego de un mecanismo_riego_finca_sector
    :param ejecucion_riego:
    :return:
    """
    estado_ejecucion_riego_en_ejecucion = EstadoEjecucionRiego.objects.get(
        nombreEstadoEjecucionRiego=ESTADO_EN_EJECUCION)

    estado_ejecucion_riego_pausado = EstadoEjecucionRiego.objects.get(
        nombreEstadoEjecucionRiego=ESTADO_PAUSADO)

    if ejecucion_riego.estado_ejecucion_riego == estado_ejecucion_riego_pausado:
        # Se establece fecha de reinicio para calcular la duracion
        ejecucion_riego.fecha_hora_ultimo_reinicio = datetime.now(pytz.utc)
        ejecucion_riego.estado_ejecucion_riego = estado_ejecucion_riego_en_ejecucion
        # TODO llamar a adaptador mecanismo riego y ejecutar riego
        ejecucion_riego.save()


def pausar_riego(ejecucion_riego_en_curso):
    """
    Pausar una ejecucion de riego de un mecanismo_riego_finca_sector
    :param ejecucion_riego_en_curso:
    :return:
    """
    estado_ejecucion_riego_en_ejecucion = EstadoEjecucionRiego.objects.get(
        nombreEstadoEjecucionRiego=ESTADO_EN_EJECUCION)

    estado_ejecucion_riego_pausado = EstadoEjecucionRiego.objects.get(
        nombreEstadoEjecucionRiego=ESTADO_PAUSADO)

    if ejecucion_riego_en_curso.estado_ejecucion_riego == estado_ejecucion_riego_en_ejecucion:

        # Cuando se detiene el riego, se guarda la duracion parcial
        duracion_actual = ejecucion_riego_en_curso.duracion_parcial

        if ejecucion_riego_en_curso.fecha_hora_ultimo_reinicio is not None:
            ejecucion_riego_en_curso.duracion_parcial = duracion_actual + (
                datetime.now(pytz.utc) - ejecucion_riego_en_curso.fecha_hora_ultimo_reinicio).seconds

        else:
            ejecucion_riego_en_curso.duracion_parcial = duracion_actual + (
                datetime.now(pytz.utc) - ejecucion_riego_en_curso.fecha_hora_inicio).seconds

        ejecucion_riego_en_curso.fecha_hora_ultima_pausa = datetime.now(pytz.utc)
        ejecucion_riego_en_curso.estado_ejecucion_riego = estado_ejecucion_riego_pausado
        # TODO llamar a adaptador mecanismo riego y detener riego
        ejecucion_riego_en_curso.save()


def cancelar_riego(ejecucion_riego):
    """
    Cancelar una ejecucion de riego de un mecanismo_riego_finca_sector
    :param ejecucion_riego:
    :return:
    """
    estado_ejecucion_riego_en_ejecucion = EstadoEjecucionRiego.objects.get(
        nombreEstadoEjecucionRiego=ESTADO_EN_EJECUCION)

    estado_ejecucion_riego_pausado = EstadoEjecucionRiego.objects.get(
        nombreEstadoEjecucionRiego=ESTADO_PAUSADO)

    estado_ejecucion_riego_cancelado = EstadoEjecucionRiego.objects.get(
        nombreEstadoEjecucionRiego=ESTADO_CANCELADO)

    if ejecucion_riego.estado_ejecucion_riego == estado_ejecucion_riego_en_ejecucion:
        ejecucion_riego.fecha_hora_finalizacion = datetime.now(pytz.utc)
        ejecucion_riego.estado_ejecucion_riego = estado_ejecucion_riego_cancelado
        # TODO llamar a adaptador mecanismo riego y detener riego
        ejecucion_riego.save()

    if ejecucion_riego.estado_ejecucion_riego == estado_ejecucion_riego_pausado:
        ejecucion_riego.fecha_hora_finalizacion = ejecucion_riego.fecha_hora_ultima_pausa
        ejecucion_riego.fecha_hora_ultimo_reinicio = ejecucion_riego.fecha_hora_ultima_pausa
        ejecucion_riego.estado_ejecucion_riego = estado_ejecucion_riego_cancelado
        # TODO llamar a adaptador mecanismo riego y detener riego
        ejecucion_riego.save()
