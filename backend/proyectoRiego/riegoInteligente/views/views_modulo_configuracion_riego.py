# -*- coding: UTF-8 -*-

from django.db import IntegrityError

from ..models import MecanismoRiegoFincaSector, EjecucionRiego, EstadoEjecucionRiego
from supportClases.security_util_functions import *  # Se importa para que se ejecuten los handlers de sesion
from supportClases.security_decorators import *
from supportClases.views_util_functions import *
from supportClases.views_constants import *
from supportClases.error_handler import *


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def obtener_riego_en_ejecucion_mecanismo_riego_finca_sector(request):
    """
    Devuelve instancia de riego en ejecucion para un Mecanismo Riego Finca Sector
    :param request: idMecanismoRiegoFincaSector
    :return: datos ejecucion riego
    """
    datos = obtener_datos_json(request)
    response = HttpResponse()

    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")

        if KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR in datos:
            if datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")

            mecanismo_riego_finca_sector_seleccionado = MecanismoRiegoFincaSector.objects.get(
                idMecanismoRiegoFincaSector=datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR])

            """
            Controlar permisos: pasar a un metodo comun
            usuario_finca = mecanismo_riego_finca_sector_seleccionado.mecanismoRiegoFinca.finca.usuariofinca_set.get(
                usuario=request.user.datosusuario
            )

            rol_usuario_finca = usuario_finca.rolUsuarioFincaList.order_by('-fechaAltaRol').first()
            permiso_obtener_riego_en_ejecucion = \
                rol_usuario_finca.conjuntoPermisos.puedeIniciarODetenerRiegoManualmente
            """

            estado_ejecucion_riego_en_ejecucion = EstadoEjecucionRiego.objects.get(
                nombreEstadoEjecucionRiego=ESTADO_EN_EJECUCION)

            estado_ejecucion_riego_pausado = EstadoEjecucionRiego.objects.get(
                nombreEstadoEjecucionRiego=ESTADO_PAUSADO)

            ejecucion_riego = EjecucionRiego.objects.filter(
                mecanismo_riego_finca_sector=mecanismo_riego_finca_sector_seleccionado,
                estado_ejecucion_riego=estado_ejecucion_riego_en_ejecucion).order_by('-fecha_hora_inicio').first()

            if ejecucion_riego is None:
                ejecucion_riego = EjecucionRiego.objects.filter(
                    mecanismo_riego_finca_sector=mecanismo_riego_finca_sector_seleccionado,
                    estado_ejecucion_riego=estado_ejecucion_riego_pausado).order_by('-fecha_hora_inicio').first()

                if ejecucion_riego is None:
                    response.content = armar_response_content(None, "No hay riego en ejecucion o pausados")
                    response.status_code = 200

                    return response
        else:
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")

        response.content = armar_response_content(ejecucion_riego)
        response.status_code = 200

        return response

    except ValueError as err:
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, TypeError, KeyError):
        return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, "Datos incorrectos")


# noinspection PyUnboundLocalVariable
@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def iniciar_riego_manualente(request):
    """
    Inicia el riego para un Mecanismo Riego Finca Sector, si habia un riego anterior lo cancela
    :param request: idMecanismoRiegoFincaSector
    :return:
    """
    datos = obtener_datos_json(request)
    response = HttpResponse()
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")

        if KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR in datos:
            if datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")

            mecanismo_riego_finca_sector_seleccionado = MecanismoRiegoFincaSector.objects.get(
                idMecanismoRiegoFincaSector=datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR])

            estado_ejecucion_riego_en_ejecucion = EstadoEjecucionRiego.objects.get(
                nombreEstadoEjecucionRiego=ESTADO_EN_EJECUCION)

            estado_ejecucion_riego_pausado = EstadoEjecucionRiego.objects.get(
                nombreEstadoEjecucionRiego=ESTADO_PAUSADO)

            ejecucion_riego_actual = EjecucionRiego.objects.filter(
                mecanismo_riego_finca_sector=mecanismo_riego_finca_sector_seleccionado)\
                .order_by('-fecha_hora_inicio').first()

            if ejecucion_riego_actual is not None:
                if ejecucion_riego_actual.estado_ejecucion_riego == estado_ejecucion_riego_en_ejecucion:

                    response.content = armar_response_content(ejecucion_riego_actual, "Riego ya esta en ejecucion")
                    response.status_code = 200

                    return response

                elif ejecucion_riego_actual.estado_ejecucion_riego == estado_ejecucion_riego_pausado:

                    # Se establece fecha de reinicio para calcular la duracion
                    ejecucion_riego_actual.fecha_hora_ultimo_reinicio = datetime.now(pytz.utc)
                    ejecucion_riego_actual.estado_ejecucion_riego = estado_ejecucion_riego_en_ejecucion
                    ejecucion_riego_actual.save()

                    response.content = armar_response_content(ejecucion_riego_actual, "Riego reanudado")
                    response.status_code = 200

                    return response

            ejecucion_riego_nuevo = EjecucionRiego(
                mecanismo_riego_finca_sector=mecanismo_riego_finca_sector_seleccionado,
                fecha_hora_inicio=datetime.now(pytz.utc),
                detalle="Riego iniciado manualmente",
                estado_ejecucion_riego=estado_ejecucion_riego_en_ejecucion
            )
            ejecucion_riego_nuevo.save()

        response.content = armar_response_content(ejecucion_riego_nuevo)
        response.status_code = 200

        return response

    except (ValueError, AttributeError) as err:
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, TypeError, KeyError):
        return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, "Datos incorrectos")


# noinspection PyUnboundLocalVariable
@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def pausar_riego_manualente(request):
    """
    Detiene el riego para un Mecanismo Riego Finca Sector
    :param request: idMecanismoRiegoFincaSector
    :return:
    """
    datos = obtener_datos_json(request)
    response = HttpResponse()
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")

        if KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR in datos:
            if datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")

            mecanismo_riego_finca_sector_seleccionado = MecanismoRiegoFincaSector.objects.get(
                idMecanismoRiegoFincaSector=datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR])

            estado_ejecucion_riego_en_ejecucion = EstadoEjecucionRiego.objects.get(
                nombreEstadoEjecucionRiego=ESTADO_EN_EJECUCION)

            estado_ejecucion_riego_pausado = EstadoEjecucionRiego.objects.get(
                nombreEstadoEjecucionRiego=ESTADO_PAUSADO)

            ejecucion_riego_actual = EjecucionRiego.objects.filter(
                mecanismo_riego_finca_sector=mecanismo_riego_finca_sector_seleccionado)\
                .order_by('-fecha_hora_inicio').first()

            if ejecucion_riego_actual is not None:
                if ejecucion_riego_actual.estado_ejecucion_riego == estado_ejecucion_riego_en_ejecucion:

                    # Cuando se detiene el riego, se guarda la duracion parcial
                    duracion_actual = ejecucion_riego_actual.duracion_parcial

                    if ejecucion_riego_actual.fecha_hora_ultimo_reinicio is not None:
                        ejecucion_riego_actual.duracion_parcial = duracion_actual + (
                            datetime.now(pytz.utc) - ejecucion_riego_actual.fecha_hora_ultimo_reinicio).seconds

                    else:
                        ejecucion_riego_actual.duracion_parcial = duracion_actual + (
                            datetime.now(pytz.utc) - ejecucion_riego_actual.fecha_hora_inicio).seconds

                    ejecucion_riego_actual.estado_ejecucion_riego = estado_ejecucion_riego_pausado
                    ejecucion_riego_actual.save()

                elif ejecucion_riego_actual.estado_ejecucion_riego == estado_ejecucion_riego_pausado:

                    response.content = armar_response_content(ejecucion_riego_actual, "Riego ya esta pausado")
                    response.status_code = 200

                    return response

                else:
                    response.content = armar_response_content(None, "No hay riegos activos")
                    response.status_code = 200

                    return response

        response.content = armar_response_content(ejecucion_riego_actual)
        response.status_code = 200

        return response

    except ValueError as err:
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, TypeError, KeyError):
        return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, "Datos incorrectos")


# noinspection PyUnboundLocalVariable
@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def cancelar_riego_manualente(request):
    """
    Cancela el riego para un Mecanismo Riego Finca Sector
    :param request: idMecanismoRiegoFincaSector
    :return:
    """
    datos = obtener_datos_json(request)
    response = HttpResponse()
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")

        if KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR in datos:
            if datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")

            mecanismo_riego_finca_sector_seleccionado = MecanismoRiegoFincaSector.objects.get(
                idMecanismoRiegoFincaSector=datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR])

            estado_ejecucion_riego_en_ejecucion = EstadoEjecucionRiego.objects.get(
                nombreEstadoEjecucionRiego=ESTADO_EN_EJECUCION)

            estado_ejecucion_riego_pausado = EstadoEjecucionRiego.objects.get(
                nombreEstadoEjecucionRiego=ESTADO_PAUSADO)

            estado_ejecucion_riego_cancelado = EstadoEjecucionRiego.objects.get(
                nombreEstadoEjecucionRiego=ESTADO_CANCELADO)

            ejecucion_riego_actual = EjecucionRiego.objects.filter(
                mecanismo_riego_finca_sector=mecanismo_riego_finca_sector_seleccionado)\
                .order_by('-fecha_hora_inicio').first()

            if ejecucion_riego_actual is not None:
                if ejecucion_riego_actual.estado_ejecucion_riego == estado_ejecucion_riego_en_ejecucion or \
                                ejecucion_riego_actual.estado_ejecucion_riego == estado_ejecucion_riego_pausado:
                    ejecucion_riego_actual.fecha_hora_finalizacion = datetime.now(pytz.utc)
                    ejecucion_riego_actual.estado_ejecucion_riego = estado_ejecucion_riego_cancelado
                    ejecucion_riego_actual.save()

                    response.content = armar_response_content(ejecucion_riego_actual)
                    response.status_code = 200

            response.content = armar_response_content(None, "No hay riegos activos")
            response.status_code = 200

            return response

    except ValueError as err:
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, TypeError, KeyError):
        return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, "Datos incorrectos")
