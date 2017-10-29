from datetime import datetime
import pytz

from django.core.exceptions import ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned

from ...models import EjecucionRiego, EstadoEjecucionRiego, ConfiguracionRiego, EstadoConfiguracionRiego, \
    HistoricoEstadoConfiguracionRiego, TipoConfiguracionRiego, MecanismoRiegoFincaSector
from views_constants import *


def iniciar_ejecucion_riego(mecanismo_riego_finca_sector, detalle_riego, configuracion_riego=None,
                            fecha_fin_programada=None):
    """
    Iniciar una ejecucion de riego de un mecanismo_riego_finca_sector
    :param mecanismo_riego_finca_sector:
    :param detalle_riego:
    :param configuracion_riego:
    :param fecha_fin_programada:
    :return:
    """

    cancelar_todos_las_ejecuciones_mecanismo_riego_finca_sector(mecanismo_riego_finca_sector)

    estado_ejecucion_riego_en_ejecucion = EstadoEjecucionRiego.objects.get(
        nombreEstadoEjecucionRiego=ESTADO_EN_EJECUCION)

    ejecucion_riego_nuevo = EjecucionRiego(
        mecanismo_riego_finca_sector=mecanismo_riego_finca_sector,
        fecha_hora_inicio=datetime.now(pytz.utc),
        detalle=detalle_riego,
        estado_ejecucion_riego=estado_ejecucion_riego_en_ejecucion,
        configuracion_riego=configuracion_riego,
        fecha_hora_final_programada=fecha_fin_programada
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

    elif ejecucion_riego.estado_ejecucion_riego == estado_ejecucion_riego_pausado:
        ejecucion_riego.fecha_hora_finalizacion = ejecucion_riego.fecha_hora_ultima_pausa
        ejecucion_riego.fecha_hora_ultimo_reinicio = ejecucion_riego.fecha_hora_ultima_pausa
        ejecucion_riego.estado_ejecucion_riego = estado_ejecucion_riego_cancelado
        # TODO llamar a adaptador mecanismo riego y detener riego
        ejecucion_riego.save()


def detener_riego(ejecucion_riego):
    """
    Detener una ejecucion de riego de un mecanismo_riego_finca_sector
    :param ejecucion_riego:
    :return:
    """
    estado_ejecucion_riego_en_ejecucion = EstadoEjecucionRiego.objects.get(
        nombreEstadoEjecucionRiego=ESTADO_EN_EJECUCION)

    estado_ejecucion_riego_pausado = EstadoEjecucionRiego.objects.get(
        nombreEstadoEjecucionRiego=ESTADO_PAUSADO)

    estado_ejecucion_riego_finalizado = EstadoEjecucionRiego.objects.get(
        nombreEstadoEjecucionRiego=ESTADO_FINALIZADO)

    if ejecucion_riego.estado_ejecucion_riego == estado_ejecucion_riego_en_ejecucion:
        ejecucion_riego.fecha_hora_finalizacion = datetime.now(pytz.utc)
        ejecucion_riego.estado_ejecucion_riego = estado_ejecucion_riego_finalizado
        # TODO llamar a adaptador mecanismo riego y detener riego
        ejecucion_riego.save()

    elif ejecucion_riego.estado_ejecucion_riego == estado_ejecucion_riego_pausado:
        ejecucion_riego.fecha_hora_finalizacion = ejecucion_riego.fecha_hora_ultima_pausa
        ejecucion_riego.fecha_hora_ultimo_reinicio = ejecucion_riego.fecha_hora_ultima_pausa
        ejecucion_riego.estado_ejecucion_riego = estado_ejecucion_riego_finalizado
        # TODO llamar a adaptador mecanismo riego y detener riego
        ejecucion_riego.save()


def cancelar_todos_las_ejecuciones_mecanismo_riego_finca_sector(mecanismo_riego_finca_sector):
    """
    Detener todas las ejecuciones para controlar que no haya mas de una activa al mismo tiempo
    :param mecanismo_riego_finca_sector:
    :return:
    """
    try:
        estado_ejecucion_riego_en_ejecucion = EstadoEjecucionRiego.objects.get(
            nombreEstadoEjecucionRiego=ESTADO_EN_EJECUCION)

        ejecuciones_riego_activas = EjecucionRiego.objects.filter(
            mecanismo_riego_finca_sector=mecanismo_riego_finca_sector,
            estado_ejecucion_riego=estado_ejecucion_riego_en_ejecucion
        )

        for ejecucion_riego in ejecuciones_riego_activas:
            cancelar_riego(ejecucion_riego)

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned):
        pass

    try:
        estado_ejecucion_riego_pausado = EstadoEjecucionRiego.objects.get(
            nombreEstadoEjecucionRiego=ESTADO_PAUSADO)

        ejecuciones_riego_pausadas = EjecucionRiego.objects.filter(
            mecanismo_riego_finca_sector=mecanismo_riego_finca_sector,
            estado_ejecucion_riego=estado_ejecucion_riego_pausado
        )

        for ejecucion_riego in ejecuciones_riego_pausadas:
            cancelar_riego(ejecucion_riego)

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned):
        pass


def crear_configuracion_riego(nombre, descripcion, duracion_maxima, nombre_tipo_configuracion_riego,
                              id_mecanismo_riego_finca_sector):
    """
    Se crea una configuracion de riego
    :param nombre:
    :param descripcion:
    :param duracion_maxima:
    :param nombre_tipo_configuracion_riego:
    :param id_mecanismo_riego_finca_sector:
    :return:
    """
    # Se obtienen objetos necesarios para crear la configuracion
    tipo_configuracion_riego = TipoConfiguracionRiego.objects.get(nombre=nombre_tipo_configuracion_riego)
    mecanismo_riego_finca_sector = MecanismoRiegoFincaSector.objects.get(
        idMecanismoRiegoFincaSector=id_mecanismo_riego_finca_sector)
    estado_configuracion_riego_habilitado = EstadoConfiguracionRiego.objects.get(
        nombreEstadoConfiguracionRiego=ESTADO_HABILITADO)

    estado_historico = HistoricoEstadoConfiguracionRiego(
        fechaInicioEstadoConfiguracionRiego=datetime.now(pytz.utc),
        estado_configuracion_riego=estado_configuracion_riego_habilitado)

    nueva_configuracion_riego = ConfiguracionRiego(
        nombre=nombre,
        descripcion=descripcion,
        duracionMaxima=duracion_maxima,
        tipoConfiguracionRiego=tipo_configuracion_riego,
        fechaCreacion=datetime.now(pytz.utc),
        mecanismoRiegoFincaSector=mecanismo_riego_finca_sector,
    )
    nueva_configuracion_riego.save()

    estado_historico.configuracion_riego = nueva_configuracion_riego
    estado_historico.save()

    return nueva_configuracion_riego


def eliminar_configuracion_riego(configuracion_riego):
    """
    Se elimina una configuracion de riego
    :param configuracion_riego:
    :return:
    """
    # Se obtienen objetos necesarios para eliminar la configuracion
    estado_configuracion_riego_habilitado = EstadoConfiguracionRiego.objects.get(
        nombreEstadoConfiguracionRiego=ESTADO_HABILITADO)
    estado_configuracion_riego_deshabilitado = EstadoConfiguracionRiego.objects.get(
        nombreEstadoConfiguracionRiego=ESTADO_DESHABILITADO)
    estado_configuracion_riego_eliminado = EstadoConfiguracionRiego.objects.get(
        nombreEstadoConfiguracionRiego=ESTADO_ELIMINADO)

    ultimo_estado_historico = HistoricoEstadoConfiguracionRiego.objects.get(
        configuracion_riego=configuracion_riego, fechaFinEstadoConfiguracionRiego=None)

    if ultimo_estado_historico.estado_configuracion_riego == estado_configuracion_riego_habilitado \
            or ultimo_estado_historico.estado_configuracion_riego == estado_configuracion_riego_deshabilitado:

        ultimo_estado_historico.fechaFinEstadoConfiguracionRiego = datetime.now(pytz.utc)
        ultimo_estado_historico.save()

        estado_historico_eliminado = HistoricoEstadoConfiguracionRiego(
            fechaInicioEstadoConfiguracionRiego=datetime.now(pytz.utc),
            estado_configuracion_riego=estado_configuracion_riego_eliminado)
        estado_historico_eliminado.configuracion_riego = configuracion_riego
        estado_historico_eliminado.save()

        configuracion_riego.fechaFinalizacion = datetime.now(pytz.utc)
        configuracion_riego.save()

        return True

    return False


def configuracion_tiene_riego_activo(configuracion_riego):

    try:
        estado_ejecucion_riego_en_ejecucion = EstadoEjecucionRiego.objects.get(
            nombreEstadoEjecucionRiego=ESTADO_EN_EJECUCION)

        estado_ejecucion_riego_pausado = EstadoEjecucionRiego.objects.get(
            nombreEstadoEjecucionRiego=ESTADO_PAUSADO)

        try:
            ejecucion_riego = EjecucionRiego.objects.filter(configuracion_riego=configuracion_riego,
                                                            estado_ejecucion_riego=estado_ejecucion_riego_en_ejecucion,
                                                            fecha_hora_finalizacion__isnull=True
                                                            )
            if ejecucion_riego:
                return True

        except ObjectDoesNotExist:
            pass

        try:
            ejecucion_riego = EjecucionRiego.objects.filter(configuracion_riego=configuracion_riego,
                                                            estado_ejecucion_riego=estado_ejecucion_riego_pausado,
                                                            fecha_hora_finalizacion__isnull=True
                                                            )
            if ejecucion_riego:
                return True

        except ObjectDoesNotExist:
            pass

        return False

    except ObjectDoesNotExist:
        return False
