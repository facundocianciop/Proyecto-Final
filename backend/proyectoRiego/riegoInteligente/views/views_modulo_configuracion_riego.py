# -*- coding: UTF-8 -*-

from django.db import transaction
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned

from ..models import MecanismoRiegoFincaSector, Finca, ConfiguracionRiego, EstadoConfiguracionRiego, \
    HistoricoEstadoConfiguracionRiego, TipoConfiguracionRiego, CriterioRiegoPorHora, CriterioRiegoPorMedicion, \
    CriterioRiegoVolumenAgua

from supportClases.configuracion_riego_util_functions import *
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
    :param request: idMecanismoRiegoFincaSector, idFinca
    :return: datos ejecucion riego
    """
    datos = obtener_datos_json(request)
    response = HttpResponse()

    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

        if KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR in datos and KEY_ID_FINCA in datos:
            if datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
            if datos[KEY_ID_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

            finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])

            mecanismo_riego_finca_sector_seleccionado = MecanismoRiegoFincaSector.objects.get(
                idMecanismoRiegoFincaSector=datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR])

            if not mecanismo_riego_finca_sector_seleccionado.mecanismoRiegoFinca.finca == finca:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

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

            if ejecucion_riego is not None:
                response.content = armar_response_content(ejecucion_riego)
                response.status_code = 200

                return response

            else:
                response.content = armar_response_content(None, DETALLE_RIEGO_NO_ACTIVO)
                response.status_code = 200

                return response

        else:
            raise KeyError

    except KeyError as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

    except (ValueError, TypeError, IntegrityError) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (SystemError, RuntimeError) as err:
        if len(err.args) == 2:
            return build_internal_server_error(response, err.args[0], err.args[1])
        else:
            return build_internal_server_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_DESCONOCIDO)


# noinspection PyUnboundLocalVariable
@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def iniciar_riego_manualente(request):
    """
    Inicia el riego para un Mecanismo Riego Finca Sector, si habia un riego anterior lo cancela
    :param request: idMecanismoRiegoFincaSector, idFinca
    :return:
    """
    datos = obtener_datos_json(request)
    response = HttpResponse()
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

        if KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR in datos and KEY_ID_FINCA in datos:
            if datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
            if datos[KEY_ID_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

            finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])

            mecanismo_riego_finca_sector_seleccionado = MecanismoRiegoFincaSector.objects.get(
                idMecanismoRiegoFincaSector=datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR])

            if not mecanismo_riego_finca_sector_seleccionado.mecanismoRiegoFinca.finca == finca:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

            estado_ejecucion_riego_en_ejecucion = EstadoEjecucionRiego.objects.get(
                nombreEstadoEjecucionRiego=ESTADO_EN_EJECUCION)

            estado_ejecucion_riego_pausado = EstadoEjecucionRiego.objects.get(
                nombreEstadoEjecucionRiego=ESTADO_PAUSADO)

            ejecucion_riego_actual = EjecucionRiego.objects.filter(
                mecanismo_riego_finca_sector=mecanismo_riego_finca_sector_seleccionado)\
                .order_by('-fecha_hora_inicio').first()

            if ejecucion_riego_actual is not None:
                if ejecucion_riego_actual.estado_ejecucion_riego == estado_ejecucion_riego_en_ejecucion:

                    response.content = armar_response_content(ejecucion_riego_actual,
                                                              DETALLE_RIEGO_EJECUCION_EN_PROCESO)
                    response.status_code = 200

                    return response

                elif ejecucion_riego_actual.estado_ejecucion_riego == estado_ejecucion_riego_pausado:

                    resumir_riego(ejecucion_riego_actual)

                    response.content = armar_response_content(ejecucion_riego_actual, DETALLE_RIEGO_REANUDADO)
                    response.status_code = 200

                    return response

            ejecucion_riego_nuevo = iniciar_ejecucion_riego(mecanismo_riego_finca_sector_seleccionado,
                                                            "Riego iniciado manualmente")
            if ejecucion_riego_nuevo:
                response.content = armar_response_content(ejecucion_riego_nuevo)
                response.status_code = 200
                return response
            else:
                raise SystemError(ERROR_EJECUCION_RIEGO, DETALLE_ERROR_EJECUION_RIEGO)

        else:
            raise KeyError

    except KeyError as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

    except (ValueError, TypeError, IntegrityError) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (SystemError, RuntimeError) as err:
        if len(err.args) == 2:
            return build_internal_server_error(response, err.args[0], err.args[1])
        else:
            return build_internal_server_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_DESCONOCIDO)


# noinspection PyUnboundLocalVariable
@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def pausar_riego_manualente(request):
    """
    Detiene el riego para un Mecanismo Riego Finca Sector
    :param request: idMecanismoRiegoFincaSector, idFinca
    :return:
    """
    datos = obtener_datos_json(request)
    response = HttpResponse()
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

        if KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR in datos and KEY_ID_FINCA in datos:
            if datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
            if datos[KEY_ID_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

            finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])

            mecanismo_riego_finca_sector_seleccionado = MecanismoRiegoFincaSector.objects.get(
                idMecanismoRiegoFincaSector=datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR])

            if not mecanismo_riego_finca_sector_seleccionado.mecanismoRiegoFinca.finca == finca:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

            estado_ejecucion_riego_en_ejecucion = EstadoEjecucionRiego.objects.get(
                nombreEstadoEjecucionRiego=ESTADO_EN_EJECUCION)

            estado_ejecucion_riego_pausado = EstadoEjecucionRiego.objects.get(
                nombreEstadoEjecucionRiego=ESTADO_PAUSADO)

            ejecucion_riego_actual = EjecucionRiego.objects.filter(
                mecanismo_riego_finca_sector=mecanismo_riego_finca_sector_seleccionado)\
                .order_by('-fecha_hora_inicio').first()

            if ejecucion_riego_actual is not None:
                if ejecucion_riego_actual.estado_ejecucion_riego == estado_ejecucion_riego_en_ejecucion:

                    pausar_riego(ejecucion_riego_actual)

                    response.content = armar_response_content(ejecucion_riego_actual, DETALLE_RIEGO_PAUSADO)
                    response.status_code = 200

                    return response

                elif ejecucion_riego_actual.estado_ejecucion_riego == estado_ejecucion_riego_pausado:

                    response.content = armar_response_content(ejecucion_riego_actual, DETALLE_RIEGO_YA_PAUSADO)
                    response.status_code = 200

                    return response

            response.content = armar_response_content(None, DETALLE_RIEGO_NO_ACTIVO)
            response.status_code = 200

            return response

        else:
            raise KeyError

    except KeyError as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

    except (ValueError, TypeError, IntegrityError) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (SystemError, RuntimeError) as err:
        if len(err.args) == 2:
            return build_internal_server_error(response, err.args[0], err.args[1])
        else:
            return build_internal_server_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_DESCONOCIDO)


# noinspection PyUnboundLocalVariable
@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def cancelar_riego_manualente(request):
    """
    Cancela el riego para un Mecanismo Riego Finca Sector
    :param request: idMecanismoRiegoFincaSector, idFinca
    :return:
    """
    datos = obtener_datos_json(request)
    response = HttpResponse()
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

        if KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR in datos and KEY_ID_FINCA in datos:
            if datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
            if datos[KEY_ID_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

            finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])

            mecanismo_riego_finca_sector_seleccionado = MecanismoRiegoFincaSector.objects.get(
                idMecanismoRiegoFincaSector=datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR])

            if not mecanismo_riego_finca_sector_seleccionado.mecanismoRiegoFinca.finca == finca:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

            estado_ejecucion_riego_en_ejecucion = EstadoEjecucionRiego.objects.get(
                nombreEstadoEjecucionRiego=ESTADO_EN_EJECUCION)

            estado_ejecucion_riego_pausado = EstadoEjecucionRiego.objects.get(
                nombreEstadoEjecucionRiego=ESTADO_PAUSADO)

            ejecucion_riego_actual = EjecucionRiego.objects.filter(
                mecanismo_riego_finca_sector=mecanismo_riego_finca_sector_seleccionado)\
                .order_by('-fecha_hora_inicio').first()

            if ejecucion_riego_actual is not None:
                if (ejecucion_riego_actual.estado_ejecucion_riego == estado_ejecucion_riego_en_ejecucion
                        or ejecucion_riego_actual.estado_ejecucion_riego == estado_ejecucion_riego_pausado):

                    cancelar_riego(ejecucion_riego_actual)

                    response.content = armar_response_content(ejecucion_riego_actual, DETALLE_RIEGO_CANCELADO)
                    response.status_code = 200

                    return response

            response.content = armar_response_content(None, DETALLE_RIEGO_NO_ACTIVO)
            response.status_code = 200

            return response

        else:
            raise KeyError

    except KeyError as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

    except (ValueError, TypeError, IntegrityError) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (SystemError, RuntimeError) as err:
        if len(err.args) == 2:
            return build_internal_server_error(response, err.args[0], err.args[1])
        else:
            return build_internal_server_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_DESCONOCIDO)


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def obtener_configuraciones_riego_mecanismo_riego_finca_sector(request):
    """
    Obtener las configuraciones de riego de un mecanismo finca sector
    :param request: idFinca, idMecanismoRiegoFincaSector
    :return:
    """
    datos = obtener_datos_json(request)
    response = HttpResponse()
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

        if KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR in datos and KEY_ID_FINCA in datos:
            if datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
            if datos[KEY_ID_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

            finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])

            mecanismo_riego_finca_sector_seleccionado = MecanismoRiegoFincaSector.objects.get(
                idMecanismoRiegoFincaSector=datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR])

            if not mecanismo_riego_finca_sector_seleccionado.mecanismoRiegoFinca.finca == finca:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

            # TODO

            # Se obtienen estados de configuracion riego
            estado_configuracion_riego_habilitado = EstadoConfiguracionRiego.objects.get(
                nombreEstadoConfiguracionRiego=ESTADO_HABILITADO)
            estado_configuracion_riego_deshabilitado = EstadoConfiguracionRiego.objects.get(
                nombreEstadoConfiguracionRiego=ESTADO_DESHABILITADO)

            # Se obtienen todos las configuraciones de riego del sector seleccionado
            configuraciones_riego_mecanismo_sector = ConfiguracionRiego.objects.filter(
                mecanismoRiegoFincaSector=mecanismo_riego_finca_sector_seleccionado)

            # Se obtienen todos las configuraciones de riego del sector activas (habilitadas o deshabilitadas)
            configuraciones_riego_activas = []
            for configuracion_riego in configuraciones_riego_mecanismo_sector:
                ultimo_estado_historico = HistoricoEstadoConfiguracionRiego.objects.get(
                    configuracion_riego=configuracion_riego, fechaFinEstadoConfiguracionRiego=None)
                if ultimo_estado_historico.estado_configuracion_riego == estado_configuracion_riego_habilitado \
                        or ultimo_estado_historico.estado_configuracion_riego \
                        == estado_configuracion_riego_deshabilitado:
                    configuraciones_riego_activas.extend([configuracion_riego])

            if configuraciones_riego_activas is not None and not len(configuraciones_riego_activas) == 0:

                response.content = armar_response_list_content(configuraciones_riego_activas)
                response.status_code = 200

                return response

            response.content = armar_response_content(None)
            response.status_code = 200

            return response

        else:
            raise KeyError

    except KeyError as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

    except (ValueError, TypeError, IntegrityError) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (SystemError, RuntimeError) as err:
        if len(err.args) == 2:
            return build_internal_server_error(response, err.args[0], err.args[1])
        else:
            return build_internal_server_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_DESCONOCIDO)


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def obtener_criterios_iniciales_configuracion_riego_mecanismo_riego_finca_sector(request):
    """
    Obtener los criterios iniciales de una configuracion de riego
    :param request: idFinca, idMecanismoRiegoFincaSector, idConfiguracionRiego
    :return:
    """
    datos = obtener_datos_json(request)
    response = HttpResponse()
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

        if KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR in datos and KEY_ID_FINCA in datos:
            if datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
            if datos[KEY_ID_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

            finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])

            mecanismo_riego_finca_sector_seleccionado = MecanismoRiegoFincaSector.objects.get(
                idMecanismoRiegoFincaSector=datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR])

            if not mecanismo_riego_finca_sector_seleccionado.mecanismoRiegoFinca.finca == finca:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

            # TODO
            if KEY_ID_CONFIGURACION_RIEGO not in datos:
                raise KeyError

            if datos[KEY_ID_CONFIGURACION_RIEGO] == "":
                raise ValueError

            configuracion_riego = ConfiguracionRiego.objects.get(
                id_configuracion_riego=datos[KEY_ID_CONFIGURACION_RIEGO])

            if not configuracion_riego.mecanismoRiegoFincaSector == mecanismo_riego_finca_sector_seleccionado:
                raise ValueError

            criterios_riego_iniciales = configuracion_riego.criterioRiegoInicial

            response.content = armar_response_list_content(criterios_riego_iniciales)
            response.status_code = 200

            return response

        else:
            raise KeyError

    except KeyError as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

    except (ValueError, TypeError, IntegrityError) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (SystemError, RuntimeError) as err:
        if len(err.args) == 2:
            return build_internal_server_error(response, err.args[0], err.args[1])
        else:
            return build_internal_server_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_DESCONOCIDO)


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def obtener_criterios_finales_configuracion_riego_mecanismo_riego_finca_sector(request):
    """
    Obtener los criterios finales de una configuracion de riego
    :param request: idFinca, idMecanismoRiegoFincaSector, idConfiguracionRiego
    :return:
    """
    datos = obtener_datos_json(request)
    response = HttpResponse()
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

        if KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR in datos and KEY_ID_FINCA in datos:
            if datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
            if datos[KEY_ID_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

            finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])

            mecanismo_riego_finca_sector_seleccionado = MecanismoRiegoFincaSector.objects.get(
                idMecanismoRiegoFincaSector=datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR])

            if not mecanismo_riego_finca_sector_seleccionado.mecanismoRiegoFinca.finca == finca:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

            # TODO
            if KEY_ID_CONFIGURACION_RIEGO not in datos:
                raise KeyError

            if datos[KEY_ID_CONFIGURACION_RIEGO] == "":
                raise ValueError

            configuracion_riego = ConfiguracionRiego.objects.get(
                id_configuracion_riego=datos[KEY_ID_CONFIGURACION_RIEGO])

            if not configuracion_riego.mecanismoRiegoFincaSector == mecanismo_riego_finca_sector_seleccionado:
                raise ValueError

            criterios_riego_finales = configuracion_riego.criterioRiegoFinal

            response.content = armar_response_list_content(criterios_riego_finales)
            response.status_code = 200

        else:
            raise KeyError

    except KeyError as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

    except (ValueError, TypeError, IntegrityError) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (SystemError, RuntimeError) as err:
        if len(err.args) == 2:
            return build_internal_server_error(response, err.args[0], err.args[1])
        else:
            return build_internal_server_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_DESCONOCIDO)


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def crear_configuracion_riego_automatico_mecanismo_riego_finca_sector(request):
    datos = obtener_datos_json(request)
    response = HttpResponse()
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

        if KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR in datos and KEY_ID_FINCA in datos:
            if datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
            if datos[KEY_ID_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

            finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])

            mecanismo_riego_finca_sector_seleccionado = MecanismoRiegoFincaSector.objects.get(
                idMecanismoRiegoFincaSector=datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR])

            if not mecanismo_riego_finca_sector_seleccionado.mecanismoRiegoFinca.finca == finca:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

            # TODO
            


            response.content = armar_response_content(None)
            response.status_code = 200

            return response

        else:
            raise KeyError

    except KeyError as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

    except (ValueError, TypeError, IntegrityError) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (SystemError, RuntimeError) as err:
        if len(err.args) == 2:
            return build_internal_server_error(response, err.args[0], err.args[1])
        else:
            return build_internal_server_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_DESCONOCIDO)


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def crear_configuracion_riego_manual_mecanismo_riego_finca_sector(request):
    datos = obtener_datos_json(request)
    response = HttpResponse()
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

        if KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR in datos and KEY_ID_FINCA in datos:
            if datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
            if datos[KEY_ID_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

            finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])

            mecanismo_riego_finca_sector_seleccionado = MecanismoRiegoFincaSector.objects.get(
                idMecanismoRiegoFincaSector=datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR])

            if not mecanismo_riego_finca_sector_seleccionado.mecanismoRiegoFinca.finca == finca:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

            # TODO

            response.content = armar_response_content(None)
            response.status_code = 200

            return response

        else:
            raise KeyError

    except KeyError as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

    except (ValueError, TypeError, IntegrityError) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (SystemError, RuntimeError) as err:
        if len(err.args) == 2:
            return build_internal_server_error(response, err.args[0], err.args[1])
        else:
            return build_internal_server_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_DESCONOCIDO)


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def cambiar_estado_configuracion_riego_mecanismo_riego_finca_sector(request):
    datos = obtener_datos_json(request)
    response = HttpResponse()
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

        if KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR in datos and KEY_ID_FINCA in datos:
            if datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
            if datos[KEY_ID_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

            finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])

            mecanismo_riego_finca_sector_seleccionado = MecanismoRiegoFincaSector.objects.get(
                idMecanismoRiegoFincaSector=datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR])

            if not mecanismo_riego_finca_sector_seleccionado.mecanismoRiegoFinca.finca == finca:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

            # TODO

            response.content = armar_response_content(None)
            response.status_code = 200

            return response

        else:
            raise KeyError

    except KeyError as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

    except (ValueError, TypeError, IntegrityError) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (SystemError, RuntimeError) as err:
        if len(err.args) == 2:
            return build_internal_server_error(response, err.args[0], err.args[1])
        else:
            return build_internal_server_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_DESCONOCIDO)


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def modificar_configuracion_riego_mecanismo_riego_finca_sector(request):
    datos = obtener_datos_json(request)
    response = HttpResponse()
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

        if KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR in datos and KEY_ID_FINCA in datos:
            if datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
            if datos[KEY_ID_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

            finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])

            mecanismo_riego_finca_sector_seleccionado = MecanismoRiegoFincaSector.objects.get(
                idMecanismoRiegoFincaSector=datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR])

            if not mecanismo_riego_finca_sector_seleccionado.mecanismoRiegoFinca.finca == finca:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

            # TODO

            response.content = armar_response_content(None)
            response.status_code = 200

            return response

        else:
            raise KeyError

    except KeyError as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

    except (ValueError, TypeError, IntegrityError) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (SystemError, RuntimeError) as err:
        if len(err.args) == 2:
            return build_internal_server_error(response, err.args[0], err.args[1])
        else:
            return build_internal_server_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_DESCONOCIDO)


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def eliminar_configuracion_riego_mecanismo_riego_finca_sector(request):
    datos = obtener_datos_json(request)
    response = HttpResponse()
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

        if KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR in datos and KEY_ID_FINCA in datos:
            if datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
            if datos[KEY_ID_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

            finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])

            mecanismo_riego_finca_sector_seleccionado = MecanismoRiegoFincaSector.objects.get(
                idMecanismoRiegoFincaSector=datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR])

            if not mecanismo_riego_finca_sector_seleccionado.mecanismoRiegoFinca.finca == finca:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

            # TODO

            response.content = armar_response_content(None)
            response.status_code = 200

            return response

        else:
            raise KeyError

    except KeyError as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

    except (ValueError, TypeError, IntegrityError) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (SystemError, RuntimeError) as err:
        if len(err.args) == 2:
            return build_internal_server_error(response, err.args[0], err.args[1])
        else:
            return build_internal_server_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_DESCONOCIDO)


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def agregar_criterio_configuracion_riego_mecanismo_riego_finca_sector(request):
    datos = obtener_datos_json(request)
    response = HttpResponse()
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

        if KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR in datos and KEY_ID_FINCA in datos:
            if datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
            if datos[KEY_ID_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

            finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])

            mecanismo_riego_finca_sector_seleccionado = MecanismoRiegoFincaSector.objects.get(
                idMecanismoRiegoFincaSector=datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR])

            if not mecanismo_riego_finca_sector_seleccionado.mecanismoRiegoFinca.finca == finca:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

            # TODO

            response.content = armar_response_content(None)
            response.status_code = 200

            return response

        else:
            raise KeyError

    except KeyError as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

    except (ValueError, TypeError, IntegrityError) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (SystemError, RuntimeError) as err:
        if len(err.args) == 2:
            return build_internal_server_error(response, err.args[0], err.args[1])
        else:
            return build_internal_server_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_DESCONOCIDO)


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def eliminar_criterio_configuracion_riego_mecanismo_riego_finca_sector(request):
    datos = obtener_datos_json(request)
    response = HttpResponse()
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

        if KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR in datos and KEY_ID_FINCA in datos:
            if datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
            if datos[KEY_ID_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

            finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])

            mecanismo_riego_finca_sector_seleccionado = MecanismoRiegoFincaSector.objects.get(
                idMecanismoRiegoFincaSector=datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR])

            if not mecanismo_riego_finca_sector_seleccionado.mecanismoRiegoFinca.finca == finca:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

            # TODO

            response.content = armar_response_content(None)
            response.status_code = 200

            return response

        else:
            raise KeyError

    except KeyError as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

    except (ValueError, TypeError, IntegrityError) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (SystemError, RuntimeError) as err:
        if len(err.args) == 2:
            return build_internal_server_error(response, err.args[0], err.args[1])
        else:
            return build_internal_server_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_DESCONOCIDO)


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def modificar_criterio_configuracion_riego_mecanismo_riego_finca_sector(request):
    datos = obtener_datos_json(request)
    response = HttpResponse()
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

        if KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR in datos and KEY_ID_FINCA in datos:
            if datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
            if datos[KEY_ID_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

            finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])

            mecanismo_riego_finca_sector_seleccionado = MecanismoRiegoFincaSector.objects.get(
                idMecanismoRiegoFincaSector=datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR])

            if not mecanismo_riego_finca_sector_seleccionado.mecanismoRiegoFinca.finca == finca:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

            # TODO

            response.content = armar_response_content(None)
            response.status_code = 200

            return response

        else:
            raise KeyError

    except KeyError as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

    except (ValueError, TypeError, IntegrityError) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (SystemError, RuntimeError) as err:
        if len(err.args) == 2:
            return build_internal_server_error(response, err.args[0], err.args[1])
        else:
            return build_internal_server_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_DESCONOCIDO)
