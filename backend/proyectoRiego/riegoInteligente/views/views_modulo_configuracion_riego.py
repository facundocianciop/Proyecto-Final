# -*- coding: UTF-8 -*-

from django.db import transaction
# noinspection PyUnresolvedReferences
from django.db import IntegrityError, DataError, DatabaseError
# noinspection PyUnresolvedReferences
from django.core.exceptions import ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned

from ..models import CriterioRiegoPorHora, CriterioRiegoPorMedicion, CriterioRiegoVolumenAgua, CriterioRiego,\
    TipoMedicion

from supportClases.configuracion_riego_util_functions import *
from supportClases.security_decorators import *
from supportClases.views_util_functions import *
from supportClases.views_constants import *
from supportClases.error_handler import *
from supportClases.configuracion_riego_parameters import *


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
@manejar_errores()
@permisos_rol_requeridos([PERMISO_PUEDEINICIARODETENERRIEGOMANUALMENTE, PERMISO_PUEDEGENERARINFORMERIEGOENEJECUCION])
def obtener_riego_en_ejecucion_mecanismo_riego_finca_sector(request):
    """
    Devuelve instancia de riego en ejecucion para un Mecanismo Riego Finca Sector
    :param request: idMecanismoRiegoFincaSector, idFinca
    :return: datos ejecucion riego
    """
    datos = obtener_datos_json(request)
    response = HttpResponse()

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


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
@manejar_errores()
@permisos_rol_requeridos([PERMISO_PUEDEGESTIONAREVENTOPERSONALIZADO])
def buscar_configuracion_riego_id(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if KEY_ID_CONFIGURACION_RIEGO in datos:
            if datos[KEY_ID_CONFIGURACION_RIEGO] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if ConfiguracionRiego.objects.filter(id_configuracion_riego=datos[KEY_ID_CONFIGURACION_RIEGO]).__len__() \
                    == 0:
                raise ValueError(ERROR_CONFIGURACION_RIEGO_NO_EXISTE, "No se encuentra una configuracion de riego "
                                                                      "con ese id.")
            configuracion_riego = ConfiguracionRiego.objects.get(
                id_configuracion_riego=datos[KEY_ID_CONFIGURACION_RIEGO])
            response.content = armar_response_content(configuracion_riego)
            response.status_code = 200
            return response
        else:
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
    except ValueError as err:
        return build_bad_request_error(response, err.args[0], err.args[1])
    except (IntegrityError, TypeError, KeyError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
@manejar_errores()
@permisos_rol_requeridos([PERMISO_PUEDEGESTIONAREVENTOPERSONALIZADO])
def buscar_criterio_id(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if KEY_ID_CRITERIO_RIEGO in datos:
            if datos[KEY_ID_CRITERIO_RIEGO] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if CriterioRiego.objects.filter(id_criterio_riego=datos[KEY_ID_CRITERIO_RIEGO]).__len__() == 0:
                raise ValueError(ERROR_CRITERIO_NO_EXISTE, "No se encuentra un criterio de riego"
                                                           "con ese id.")
            criterio_riego = CriterioRiego.objects.get(id_criterio_riego=datos[KEY_ID_CRITERIO_RIEGO])
            response.content = armar_response_content(criterio_riego)
            response.status_code = 200
            return response
        else:
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
    except ValueError as err:
        return build_bad_request_error(response, err.args[0], err.args[1])
    except (IntegrityError, TypeError, KeyError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


# noinspection PyUnboundLocalVariable
@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
@manejar_errores()
@permisos_rol_requeridos([PERMISO_PUEDEINICIARODETENERRIEGOMANUALMENTE])
def iniciar_riego_manualente(request):
    """
    Inicia el riego para un Mecanismo Riego Finca Sector, si habia un riego pausado lo reinicia, 
    si existe uno ejecucion no hace cambios y devuelve la informacion del riego en ejecucion
    :param request: idMecanismoRiegoFincaSector, idFinca
    :return:
    """
    datos = obtener_datos_json(request)
    response = HttpResponse()

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
            mecanismo_riego_finca_sector=mecanismo_riego_finca_sector_seleccionado) \
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


# noinspection PyUnboundLocalVariable
@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
@manejar_errores()
@permisos_rol_requeridos([PERMISO_PUEDEINICIARODETENERRIEGOMANUALMENTE])
def pausar_riego_manualente(request):
    """
    Detiene el riego para un Mecanismo Riego Finca Sector
    :param request: idMecanismoRiegoFincaSector, idFinca
    :return:
    """
    datos = obtener_datos_json(request)
    response = HttpResponse()

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
            mecanismo_riego_finca_sector=mecanismo_riego_finca_sector_seleccionado) \
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


# noinspection PyUnboundLocalVariable
@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
@manejar_errores()
@permisos_rol_requeridos([PERMISO_PUEDEINICIARODETENERRIEGOMANUALMENTE])
def cancelar_riego_manualente(request):
    """
    Cancela el riego para un Mecanismo Riego Finca Sector
    :param request: idMecanismoRiegoFincaSector, idFinca
    :return:
    """
    datos = obtener_datos_json(request)
    response = HttpResponse()

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
            mecanismo_riego_finca_sector=mecanismo_riego_finca_sector_seleccionado) \
            .order_by('-fecha_hora_inicio').first()

        if ejecucion_riego_actual is not None:
            if (ejecucion_riego_actual.estado_ejecucion_riego == estado_ejecucion_riego_en_ejecucion or
                    ejecucion_riego_actual.estado_ejecucion_riego == estado_ejecucion_riego_pausado):

                cancelar_riego(ejecucion_riego_actual)

                response.content = armar_response_content(ejecucion_riego_actual, DETALLE_RIEGO_CANCELADO)
                response.status_code = 200

                return response

        response.content = armar_response_content(None, DETALLE_RIEGO_NO_ACTIVO)
        response.status_code = 200

        return response
    else:
        raise KeyError


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
@manejar_errores()
@permisos_rol_requeridos([PERMISO_PUEDECREARCONFIGURACIONRIEGO, PERMISO_PUEDEMODIFICARCONFIGURACIONRIEGO])
def obtener_configuraciones_riego_mecanismo_riego_finca_sector(request):
    """
    Obtener las configuraciones de riego de un mecanismo finca sector habilitadas o deshabilitadas (no eliminadas)
    :param request: idFinca, idMecanismoRiegoFincaSector
    :return:
    """
    datos = obtener_datos_json(request)
    response = HttpResponse()

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
                    or ultimo_estado_historico.estado_configuracion_riego == estado_configuracion_riego_deshabilitado:
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


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
@manejar_errores()
@permisos_rol_requeridos([PERMISO_PUEDECREARCONFIGURACIONRIEGO, PERMISO_PUEDEMODIFICARCONFIGURACIONRIEGO])
def obtener_criterios_iniciales_configuracion_riego_mecanismo_riego_finca_sector(request):
    """
    Obtener los criterios iniciales de una configuracion de riego (solo las 
    configuraciones programadas tienen criterios, las automaticas no)
    :param request: idFinca, idMecanismoRiegoFincaSector, idConfiguracionRiego
    :return:
    """
    datos = obtener_datos_json(request)
    response = HttpResponse()

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

        if KEY_ID_CONFIGURACION_RIEGO not in datos:
            raise KeyError

        if datos[KEY_ID_CONFIGURACION_RIEGO] == "":
            raise ValueError

        configuracion_riego = ConfiguracionRiego.objects.get(
            id_configuracion_riego=datos[KEY_ID_CONFIGURACION_RIEGO])

        if not configuracion_riego.mecanismoRiegoFincaSector == mecanismo_riego_finca_sector_seleccionado:
            raise ValueError

        criterios_riego_iniciales = CriterioRiego.objects.filter(
            configuracionRiegoInicial=configuracion_riego, fecha_eliminacion_criterio=None).select_subclasses()

        response.content = armar_response_list_content(criterios_riego_iniciales)
        response.status_code = 200

        return response
    else:
        raise KeyError


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
@manejar_errores()
@permisos_rol_requeridos([PERMISO_PUEDECREARCONFIGURACIONRIEGO, PERMISO_PUEDEMODIFICARCONFIGURACIONRIEGO])
def obtener_criterios_finales_configuracion_riego_mecanismo_riego_finca_sector(request):
    """
    Obtener los criterios finales de una configuracion de riego (solo las 
    configuraciones programadas tienen criterios, las automaticas no)
    :param request: idFinca, idMecanismoRiegoFincaSector, idConfiguracionRiego
    :return:
    """
    datos = obtener_datos_json(request)
    response = HttpResponse()

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

        if KEY_ID_CONFIGURACION_RIEGO not in datos:
            raise KeyError

        if datos[KEY_ID_CONFIGURACION_RIEGO] == "":
            raise ValueError

        configuracion_riego = ConfiguracionRiego.objects.get(
            id_configuracion_riego=datos[KEY_ID_CONFIGURACION_RIEGO])

        if not configuracion_riego.mecanismoRiegoFincaSector == mecanismo_riego_finca_sector_seleccionado:
            raise ValueError

        criterios_riego_finales = CriterioRiego.objects.filter(
            configuracionRiegoFinal=configuracion_riego, fecha_eliminacion_criterio=None).select_subclasses()

        response.content = armar_response_list_content(criterios_riego_finales)
        response.status_code = 200

        return response
    else:
        raise KeyError


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
@manejar_errores()
@permisos_rol_requeridos([PERMISO_PUEDECREARCONFIGURACIONRIEGO])
def crear_configuracion_riego_automatico_mecanismo_riego_finca_sector(request):
    """
    Crear una configuracion de riego automatica
    :param request: idFinca, idMecanismoRiegoFincaSector, nombreConfiguracionRiego, descripcionConfiguracionRiego,
    duracionMaximaConfiguracionRiego
    :return:
    """
    datos = obtener_datos_json(request)
    response = HttpResponse()

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

        # Comprobar que se mandan todos los datos necesarios
        if KEY_NOMBRE_CONFIGURACION_RIEGO not in datos or datos[KEY_NOMBRE_CONFIGURACION_RIEGO] == "":
            raise KeyError

        if KEY_DESCRIPCION_CONFIGURACION_RIEGO not in datos:
            raise KeyError

        if KEY_DURACION_MAXIMA_CONFIGURACION_RIEGO not in datos:
            raise KeyError

        # Se obtienen objetos necesarios para crear configuracion
        tipo_configuracion_riego_automatico = TipoConfiguracionRiego.objects.get(
            nombre=TIPO_CONFIGURACION_RIEGO_AUTOMATICO)

        estado_configuracion_riego_habilitado = EstadoConfiguracionRiego.objects.get(
            nombreEstadoConfiguracionRiego=ESTADO_HABILITADO)
        estado_configuracion_riego_deshabilitado = EstadoConfiguracionRiego.objects.get(
            nombreEstadoConfiguracionRiego=ESTADO_DESHABILITADO)

        # Se obtienen todos las configuraciones de riego del sector seleccionado
        configuraciones_riego_mecanismo_sector = ConfiguracionRiego.objects.filter(
            mecanismoRiegoFincaSector=mecanismo_riego_finca_sector_seleccionado)

        # Se obtienen todas las configuraciones de riego del sector activas (habilitadas o deshabilitadas)
        configuraciones_riego_activas = []
        for configuracion_riego in configuraciones_riego_mecanismo_sector:
            ultimo_estado_historico = HistoricoEstadoConfiguracionRiego.objects.get(
                configuracion_riego=configuracion_riego, fechaFinEstadoConfiguracionRiego=None)
            if ultimo_estado_historico.estado_configuracion_riego == estado_configuracion_riego_habilitado \
                    or ultimo_estado_historico.estado_configuracion_riego == estado_configuracion_riego_deshabilitado:
                configuraciones_riego_activas.extend([configuracion_riego])

        # Eliminar otras configuraciones de riego automaticas
        for configuracion_riego in configuraciones_riego_activas:
            if configuracion_riego.tipoConfiguracionRiego == tipo_configuracion_riego_automatico:
                eliminar_configuracion_riego(configuracion_riego)

        nueva_configuracion_riego = crear_configuracion_riego(
            nombre=datos[KEY_NOMBRE_CONFIGURACION_RIEGO],
            descripcion=datos[KEY_DESCRIPCION_CONFIGURACION_RIEGO],
            duracion_maxima=float(datos[KEY_DURACION_MAXIMA_CONFIGURACION_RIEGO]),
            nombre_tipo_configuracion_riego=TIPO_CONFIGURACION_RIEGO_AUTOMATICO,
            id_mecanismo_riego_finca_sector=datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR]
        )

        response.content = armar_response_content(nueva_configuracion_riego)
        response.status_code = 200

        return response
    else:
        raise KeyError


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
@manejar_errores()
@permisos_rol_requeridos([PERMISO_PUEDECREARCONFIGURACIONRIEGO])
def crear_configuracion_riego_manual_mecanismo_riego_finca_sector(request):
    """
    Crear una configuracion de riego programada
    :param request: idFinca, idMecanismoRiegoFincaSector, nombreConfiguracionRiego, descripcionConfiguracionRiego,
    duracionMaximaConfiguracionRiego
    :return:
    """
    datos = obtener_datos_json(request)
    response = HttpResponse()

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

        # Comprobar que se mandan todos los datos necesarios
        if KEY_NOMBRE_CONFIGURACION_RIEGO not in datos or datos[KEY_NOMBRE_CONFIGURACION_RIEGO] == "":
            raise KeyError

        if KEY_DESCRIPCION_CONFIGURACION_RIEGO not in datos:
            raise KeyError

        if KEY_DURACION_MAXIMA_CONFIGURACION_RIEGO not in datos:
            raise KeyError

        nueva_configuracion_riego = crear_configuracion_riego(
            nombre=datos[KEY_NOMBRE_CONFIGURACION_RIEGO],
            descripcion=datos[KEY_DESCRIPCION_CONFIGURACION_RIEGO],
            duracion_maxima=float(datos[KEY_DURACION_MAXIMA_CONFIGURACION_RIEGO]),
            nombre_tipo_configuracion_riego=TIPO_CONFIGURACION_RIEGO_PROGRAMADO,
            id_mecanismo_riego_finca_sector=datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR]
        )

        response.content = armar_response_content(nueva_configuracion_riego)
        response.status_code = 200

        return response
    else:
        raise KeyError


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
@manejar_errores()
@permisos_rol_requeridos([PERMISO_PUEDEMODIFICARCONFIGURACIONRIEGO])
def cambiar_estado_configuracion_riego_mecanismo_riego_finca_sector(request):
    """
    Cambia el estado de una configuracion riego de habilitado a deshabilitado o viceversa
    :param request: idFinca, idMecanismoRiegoFincaSector, idConfiguracionRiego
    :return:
    """
    datos = obtener_datos_json(request)
    response = HttpResponse()

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

        # Se comprueba que se hayan mandando los datos necesarios
        if KEY_ID_CONFIGURACION_RIEGO not in datos:
            raise KeyError

        if datos[KEY_ID_CONFIGURACION_RIEGO] == "":
            raise ValueError

        configuracion_riego_elegida = ConfiguracionRiego.objects.get(
            id_configuracion_riego=datos[KEY_ID_CONFIGURACION_RIEGO])

        # Comprobar que la configuracion elegida se corresponde con el mecanismo finca sector seleccionado
        if not configuracion_riego_elegida.mecanismoRiegoFincaSector == mecanismo_riego_finca_sector_seleccionado:
            raise ValueError

        # Comprobar que no se este ejecutando el riego para esta configuracion
        if configuracion_tiene_riego_activo(configuracion_riego_elegida):
            raise ValueError(ERROR_MODIFICACION_CONFIGURACION_RIEGO, DETALLE_ERROR_CONFIGURACION_RIEGO_EN_EJECUCION)

        # Se obtienen objetos necesarios para cambiar estado a la configuracion
        estado_configuracion_riego_habilitado = EstadoConfiguracionRiego.objects.get(
            nombreEstadoConfiguracionRiego=ESTADO_HABILITADO)
        estado_configuracion_riego_deshabilitado = EstadoConfiguracionRiego.objects.get(
            nombreEstadoConfiguracionRiego=ESTADO_DESHABILITADO)

        # Se obtiene el ultimo historico y se le setea fecha final
        ultimo_estado_historico = HistoricoEstadoConfiguracionRiego.objects.get(
            configuracion_riego=configuracion_riego_elegida, fechaFinEstadoConfiguracionRiego=None)

        ultimo_estado_historico.fechaFinEstadoConfiguracionRiego = datetime.now(pytz.utc)
        ultimo_estado_historico.save()

        if ultimo_estado_historico.estado_configuracion_riego == estado_configuracion_riego_habilitado:

            estado_historico_deshabilitado = HistoricoEstadoConfiguracionRiego(
                fechaInicioEstadoConfiguracionRiego=datetime.now(pytz.utc),
                estado_configuracion_riego=estado_configuracion_riego_deshabilitado)
            estado_historico_deshabilitado.configuracion_riego = configuracion_riego_elegida
            estado_historico_deshabilitado.save()

            configuracion_riego_elegida.save()

            response.content = armar_response_content(configuracion_riego_elegida)
            response.status_code = 200

            return response

        elif ultimo_estado_historico.estado_configuracion_riego == estado_configuracion_riego_deshabilitado:

            estado_historico_habilitado = HistoricoEstadoConfiguracionRiego(
                fechaInicioEstadoConfiguracionRiego=datetime.now(pytz.utc),
                estado_configuracion_riego=estado_configuracion_riego_habilitado)
            estado_historico_habilitado.configuracion_riego = configuracion_riego_elegida
            estado_historico_habilitado.save()

            configuracion_riego_elegida.save()

            response.content = armar_response_content(configuracion_riego_elegida)
            response.status_code = 200

            return response

        else:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_MODIFICACION_CONFIGURACION_RIEGO)
    else:
        raise KeyError


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
@manejar_errores()
@permisos_rol_requeridos([PERMISO_PUEDEMODIFICARCONFIGURACIONRIEGO])
def modificar_configuracion_riego_mecanismo_riego_finca_sector(request):
    """
    Se modifica el nombre, descripcion y duracion maxima de una configuracion riego
    :param request: idFinca, idMecanismoRiegoFincaSector, idConfiguracionRiego, nombreConfiguracionRiego,
    descripcionConfiguracionRiego, duracionMaximaConfiguracionRiego
    :return:
    """
    datos = obtener_datos_json(request)
    response = HttpResponse()

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

        # Se comprueba que se hayan mandando los datos necesarios
        if KEY_ID_CONFIGURACION_RIEGO not in datos:
            raise KeyError

        if datos[KEY_ID_CONFIGURACION_RIEGO] == "":
            raise ValueError

        if KEY_NOMBRE_CONFIGURACION_RIEGO not in datos or datos[KEY_NOMBRE_CONFIGURACION_RIEGO] == "":
            raise KeyError

        if KEY_DESCRIPCION_CONFIGURACION_RIEGO not in datos:
            raise KeyError

        if KEY_DURACION_MAXIMA_CONFIGURACION_RIEGO not in datos:
            raise KeyError

        # Se obtienen los objetos necesarios para modificar la configuracion
        estado_configuracion_riego_habilitado = EstadoConfiguracionRiego.objects.get(
            nombreEstadoConfiguracionRiego=ESTADO_HABILITADO)
        estado_configuracion_riego_deshabilitado = EstadoConfiguracionRiego.objects.get(
            nombreEstadoConfiguracionRiego=ESTADO_DESHABILITADO)

        # Se obtiene la configuracion elegida
        configuracion_riego_elegida = ConfiguracionRiego.objects.get(
            id_configuracion_riego=datos[KEY_ID_CONFIGURACION_RIEGO])

        # Comprobar que la configuracion elegida se corresponde con el mecanismo finca sector seleccionado
        if not configuracion_riego_elegida.mecanismoRiegoFincaSector == mecanismo_riego_finca_sector_seleccionado:
            raise ValueError

        # Se comprueba que la configuracion elegida no haya sido eliminada
        ultimo_estado_historico = HistoricoEstadoConfiguracionRiego.objects.get(
            configuracion_riego=configuracion_riego_elegida, fechaFinEstadoConfiguracionRiego=None)

        if ultimo_estado_historico.estado_configuracion_riego == estado_configuracion_riego_habilitado \
                or ultimo_estado_historico.estado_configuracion_riego == estado_configuracion_riego_deshabilitado:

            configuracion_riego_elegida.nombre = datos[KEY_NOMBRE_CONFIGURACION_RIEGO]
            configuracion_riego_elegida.descripcion = datos[KEY_DESCRIPCION_CONFIGURACION_RIEGO]
            configuracion_riego_elegida.duracionMaxima = datos[KEY_DURACION_MAXIMA_CONFIGURACION_RIEGO]

            configuracion_riego_elegida.save()

            response.content = armar_response_content(configuracion_riego_elegida)
            response.status_code = 200

            return response

        else:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_MODIFICACION_CONFIGURACION_RIEGO)
    else:
        raise KeyError


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
@manejar_errores()
@permisos_rol_requeridos([PERMISO_PUEDEMODIFICARCONFIGURACIONRIEGO])
def eliminar_configuracion_riego_mecanismo_riego_finca_sector(request):
    """
    Se elimina una configuracion riego
    :param request: idFinca, idMecanismoRiegoFincaSector, idConfiguracionRiego
    :return:
    """
    datos = obtener_datos_json(request)
    response = HttpResponse()

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

        # Se comprueba que se hayan mandando los datos necesarios
        if KEY_ID_CONFIGURACION_RIEGO not in datos:
            raise KeyError

        if datos[KEY_ID_CONFIGURACION_RIEGO] == "":
            raise ValueError

        configuracion_riego_elegida = ConfiguracionRiego.objects.get(
            id_configuracion_riego=datos[KEY_ID_CONFIGURACION_RIEGO])

        # Comprobar que no se este ejecutando el riego para esta configuracion
        if configuracion_tiene_riego_activo(configuracion_riego_elegida):
            raise ValueError(ERROR_MODIFICACION_CONFIGURACION_RIEGO, DETALLE_ERROR_CONFIGURACION_RIEGO_EN_EJECUCION)

        # Comprobar que la configuracion elegida se corresponde con el mecanismo finca sector seleccionado
        if not configuracion_riego_elegida.mecanismoRiegoFincaSector == mecanismo_riego_finca_sector_seleccionado:
            raise ValueError()

        if eliminar_configuracion_riego(configuracion_riego_elegida):
            response.content = armar_response_content(configuracion_riego_elegida)
            response.status_code = 200

            return response

        else:
            raise ValueError
    else:
        raise KeyError


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
@manejar_errores()
@permisos_rol_requeridos([PERMISO_PUEDECREARCONFIGURACIONRIEGO, PERMISO_PUEDEMODIFICARCONFIGURACIONRIEGO])
def agregar_criterio_inicial_configuracion_riego_mecanismo_riego_finca_sector(request):
    """
    Agregar un criterio inicial a una configuracion de riego (solo las 
    configuraciones programadas tienen criterios, las automaticas no)
    :param request: idFinca, idMecanismoRiegoFincaSector, idConfiguracionRiego, tipoCriterioRiego, nombreCriterioRiego,
    descripcionCriterioRiego, (criterio medicion)idTipoMedicion, (criterio medicion) valorMedicionCriterioRiego,
    (criterio hora)horaInicioCriterioRiego, (criterio hora)diaInicioCriterioRiego
    :return:
    """
    datos = obtener_datos_json(request)
    response = HttpResponse()

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

        # Se comprueba que se hayan mandando los datos necesarios
        if KEY_ID_CONFIGURACION_RIEGO not in datos:
            raise KeyError

        if datos[KEY_ID_CONFIGURACION_RIEGO] == "":
            raise ValueError

        if KEY_NOMBRE_CRITERIO_RIEGO not in datos:
            raise KeyError

        if datos[KEY_NOMBRE_CRITERIO_RIEGO] == "":
            raise ValueError

        if KEY_DESCRIPCION_CRITERIO_RIEGO not in datos:
            raise KeyError

        if KEY_TIPO_CRITERIO_RIEGO not in datos:
            raise KeyError

        if datos[KEY_TIPO_CRITERIO_RIEGO] == TIPO_CRITERIO_RIEGO_MEDICION:

            if KEY_VALOR_MEDICION_CRITERIO_RIEGO not in datos:
                raise KeyError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_CRITERIO_RIEGO_VALOR_MEDICION_INEXISTENTE)

            if datos[KEY_VALOR_MEDICION_CRITERIO_RIEGO] == "":
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_CRITERIO_RIEGO_VALOR_MEDICION_INEXISTENTE)

            if KEY_OPERADOR_MEDICION_CRITERIO_RIEGO not in datos:
                raise KeyError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_CRITERIO_RIEGO_OPERADOR_MEDICION_INEXISTENTE)

            if datos[KEY_OPERADOR_MEDICION_CRITERIO_RIEGO] == "":
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_CRITERIO_RIEGO_OPERADOR_MEDICION_INEXISTENTE)

            if KEY_ID_TIPO_MEDICION not in datos:
                raise KeyError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_CRITERIO_RIEGO_TIPO_MEDICION_INEXISTENTE)

            if datos[KEY_ID_TIPO_MEDICION] == "":
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_CRITERIO_RIEGO_TIPO_MEDICION_INEXISTENTE)

        elif datos[KEY_TIPO_CRITERIO_RIEGO] == TIPO_CRITERIO_RIEGO_VOLUMEN_AGUA:

            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_TIPO_CRITERIO_RIEGO_INICIAL_INCORRECTO)

        elif datos[KEY_TIPO_CRITERIO_RIEGO] == TIPO_CRITERIO_RIEGO_HORA:

            if KEY_HORA_INICIO_CRITERIO_RIEGO not in datos:
                raise KeyError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_CRITERIO_RIEGO_HORA_INICIO_INEXISTENTE)

            if datos[KEY_HORA_INICIO_CRITERIO_RIEGO] == "":
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_CRITERIO_RIEGO_HORA_INICIO_INEXISTENTE)

            if KEY_DIA_INICIO_CRITERIO_RIEGO not in datos:
                raise KeyError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_CRITERIO_RIEGO_DIA_INICIO_INEXISTENTE)

            if datos[KEY_DIA_INICIO_CRITERIO_RIEGO] == "":
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_CRITERIO_RIEGO_DIA_INICIO_INEXISTENTE)

        else:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_TIPO_CRITERIO_RIEGO_INCORRECTO)

        # Se obtienen los objetos necesarios para modificar la configuracion
        estado_configuracion_riego_habilitado = EstadoConfiguracionRiego.objects.get(
            nombreEstadoConfiguracionRiego=ESTADO_HABILITADO)
        estado_configuracion_riego_deshabilitado = EstadoConfiguracionRiego.objects.get(
            nombreEstadoConfiguracionRiego=ESTADO_DESHABILITADO)

        # Se obtiene la configuracion elegida
        configuracion_riego_elegida = ConfiguracionRiego.objects.get(
            id_configuracion_riego=datos[KEY_ID_CONFIGURACION_RIEGO])

        # Comprobar que la configuracion elegida se corresponde con el mecanismo finca sector seleccionado
        if not configuracion_riego_elegida.mecanismoRiegoFincaSector == mecanismo_riego_finca_sector_seleccionado:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CONFIGURACION_RIEGO_INCORRECTA)

        # Comprobar que la configuracion riego no tiene maximo de criterios iniciales
        cant_criterios_riego_iniciales = CriterioRiego.objects.filter(
            configuracionRiegoInicial=configuracion_riego_elegida, fecha_eliminacion_criterio=None).count()
        if cant_criterios_riego_iniciales >= CANTIDAD_MAXIMA_CRITERIO_RIEGO_INICIAL_CONFIGURACION_RIEGO:
            raise ValueError(ERROR_DATOS_INCORRECTOS,
                             DETALLE_ERROR_CONFIGURACION_RIEGO_CANTIDAD_MAX_CRITERIO_INICIAL)

        # Comprobar que la configuracion elegida sea programada
        tipo_configuracion_riego_programada = TipoConfiguracionRiego.objects.get(
            nombre=TIPO_CONFIGURACION_RIEGO_PROGRAMADO)
        if not configuracion_riego_elegida.tipoConfiguracionRiego == tipo_configuracion_riego_programada:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CONFIGURACION_RIEGO_AUTOMATICA_CRITERIO)

        # Se comprueba que la configuracion elegida no haya sido eliminada
        ultimo_estado_historico = HistoricoEstadoConfiguracionRiego.objects.get(
            configuracion_riego=configuracion_riego_elegida, fechaFinEstadoConfiguracionRiego=None)

        if ultimo_estado_historico.estado_configuracion_riego == estado_configuracion_riego_habilitado \
                or ultimo_estado_historico.estado_configuracion_riego == estado_configuracion_riego_deshabilitado:

            # Se verifica el tipo de criterio riego y se crea el tipo de criterio correspondiente
            if datos[KEY_TIPO_CRITERIO_RIEGO] == TIPO_CRITERIO_RIEGO_MEDICION:

                # Se obtiene el tipo de medicion
                tipo_medicion_elegido = TipoMedicion.objects.get(idTipoMedicion=datos[KEY_ID_TIPO_MEDICION])

                criterio_riego_medicion = CriterioRiegoPorMedicion(
                    nombre=datos[KEY_NOMBRE_CRITERIO_RIEGO],
                    descripcion=datos[KEY_DESCRIPCION_CRITERIO_RIEGO],
                    fecha_creacion_criterio=datetime.now(pytz.utc),
                    valor=datos[KEY_VALOR_MEDICION_CRITERIO_RIEGO],
                    operador=datos[KEY_OPERADOR_MEDICION_CRITERIO_RIEGO],
                    tipo_medicion=tipo_medicion_elegido,
                    configuracionRiegoInicial=configuracion_riego_elegida
                )
                criterio_riego_medicion.save()

                response.content = armar_response_content(criterio_riego_medicion, DETALLE_CRITERIO_RIEGO_CREADO)
                response.status_code = 200
                return response

            elif datos[KEY_TIPO_CRITERIO_RIEGO] == TIPO_CRITERIO_RIEGO_VOLUMEN_AGUA:

                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_TIPO_CRITERIO_RIEGO_INICIAL_INCORRECTO)

            elif datos[KEY_TIPO_CRITERIO_RIEGO] == TIPO_CRITERIO_RIEGO_HORA:

                criterio_riego_hora = CriterioRiegoPorHora(
                    nombre=datos[KEY_NOMBRE_CRITERIO_RIEGO],
                    descripcion=datos[KEY_DESCRIPCION_CRITERIO_RIEGO],
                    fecha_creacion_criterio=datetime.now(pytz.utc),
                    hora=parsear_datos_hora_a_utc(datos[KEY_HORA_INICIO_CRITERIO_RIEGO]),
                    numeroDia=datos[KEY_DIA_INICIO_CRITERIO_RIEGO],
                    configuracionRiegoInicial=configuracion_riego_elegida
                )
                criterio_riego_hora.save()

                response.content = armar_response_content(criterio_riego_hora, DETALLE_CRITERIO_RIEGO_CREADO)
                response.status_code = 200
                return response

            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_TIPO_CRITERIO_RIEGO_INCORRECTO)
        else:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_MODIFICACION_CONFIGURACION_RIEGO)
    else:
        raise KeyError


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
@manejar_errores()
@permisos_rol_requeridos([PERMISO_PUEDECREARCONFIGURACIONRIEGO, PERMISO_PUEDEMODIFICARCONFIGURACIONRIEGO])
def agregar_criterio_final_configuracion_riego_mecanismo_riego_finca_sector(request):
    """
    Agregar un criterio final a una configuracion de riego (solo las 
    configuraciones programadas tienen criterios, las automaticas no)
    :param request: idFinca, idMecanismoRiegoFincaSector, idConfiguracionRiego, tipoCriterioRiego, nombreCriterioRiego,
    descripcionCriterioRiego, (criterio medicion)idTipoMedicion, (criterio medicion) valorMedicionCriterioRiego,
    (criterio volumen) volumenAguaCriterioRiego, (criterio hora)horaInicioCriterioRiego,
    (criterio hora)diaInicioCriterioRiego
    :return:
    """
    datos = obtener_datos_json(request)
    response = HttpResponse()

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

        # Se comprueba que se hayan mandando los datos necesarios
        if KEY_ID_CONFIGURACION_RIEGO not in datos:
            raise KeyError

        if datos[KEY_ID_CONFIGURACION_RIEGO] == "":
            raise ValueError

        if KEY_ID_CONFIGURACION_RIEGO not in datos:
            raise KeyError

        if datos[KEY_ID_CONFIGURACION_RIEGO] == "":
            raise ValueError

        if KEY_NOMBRE_CRITERIO_RIEGO not in datos:
            raise KeyError

        if datos[KEY_NOMBRE_CRITERIO_RIEGO] == "":
            raise ValueError

        if KEY_DESCRIPCION_CRITERIO_RIEGO not in datos:
            raise KeyError

        if KEY_TIPO_CRITERIO_RIEGO not in datos:
            raise KeyError

        if datos[KEY_TIPO_CRITERIO_RIEGO] == TIPO_CRITERIO_RIEGO_MEDICION:

            if KEY_VALOR_MEDICION_CRITERIO_RIEGO not in datos:
                raise KeyError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_CRITERIO_RIEGO_VALOR_MEDICION_INEXISTENTE)

            if datos[KEY_VALOR_MEDICION_CRITERIO_RIEGO] == "":
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_CRITERIO_RIEGO_VALOR_MEDICION_INEXISTENTE)

            if KEY_OPERADOR_MEDICION_CRITERIO_RIEGO not in datos:
                raise KeyError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_CRITERIO_RIEGO_OPERADOR_MEDICION_INEXISTENTE)

            if datos[KEY_OPERADOR_MEDICION_CRITERIO_RIEGO] == "":
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_CRITERIO_RIEGO_OPERADOR_MEDICION_INEXISTENTE)

            if KEY_ID_TIPO_MEDICION not in datos:
                raise KeyError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_CRITERIO_RIEGO_TIPO_MEDICION_INEXISTENTE)

            if datos[KEY_ID_TIPO_MEDICION] == "":
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_CRITERIO_RIEGO_TIPO_MEDICION_INEXISTENTE)

        elif datos[KEY_TIPO_CRITERIO_RIEGO] == TIPO_CRITERIO_RIEGO_VOLUMEN_AGUA:

            if KEY_VOLUMEN_AGUA_CRITERIO_RIEGO not in datos:
                raise KeyError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_CRITERIO_RIEGO_VOLUMEN_INEXISTENTE)

            if datos[KEY_VOLUMEN_AGUA_CRITERIO_RIEGO] == "":
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_CRITERIO_RIEGO_VOLUMEN_INEXISTENTE)

        elif datos[KEY_TIPO_CRITERIO_RIEGO] == TIPO_CRITERIO_RIEGO_HORA:

            if KEY_HORA_INICIO_CRITERIO_RIEGO not in datos:
                raise KeyError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_CRITERIO_RIEGO_HORA_INICIO_INEXISTENTE)

            if datos[KEY_HORA_INICIO_CRITERIO_RIEGO] == "":
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_CRITERIO_RIEGO_HORA_INICIO_INEXISTENTE)

            if KEY_DIA_INICIO_CRITERIO_RIEGO not in datos:
                raise KeyError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_CRITERIO_RIEGO_DIA_INICIO_INEXISTENTE)

            if datos[KEY_DIA_INICIO_CRITERIO_RIEGO] == "":
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_CRITERIO_RIEGO_DIA_INICIO_INEXISTENTE)

        else:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_TIPO_CRITERIO_RIEGO_INCORRECTO)

        # Se obtienen los objetos necesarios para modificar la configuracion
        estado_configuracion_riego_habilitado = EstadoConfiguracionRiego.objects.get(
            nombreEstadoConfiguracionRiego=ESTADO_HABILITADO)
        estado_configuracion_riego_deshabilitado = EstadoConfiguracionRiego.objects.get(
            nombreEstadoConfiguracionRiego=ESTADO_DESHABILITADO)

        # Se obtiene la configuracion elegida
        configuracion_riego_elegida = ConfiguracionRiego.objects.get(
            id_configuracion_riego=datos[KEY_ID_CONFIGURACION_RIEGO])

        # Comprobar que la configuracion elegida se corresponde con el mecanismo finca sector seleccionado
        if not configuracion_riego_elegida.mecanismoRiegoFincaSector == mecanismo_riego_finca_sector_seleccionado:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CONFIGURACION_RIEGO_INCORRECTA)

        # Comprobar que la configuracion riego no tiene maximo de criterios finales
        cant_criterios_riego_finales = CriterioRiego.objects.filter(
            configuracionRiegoFinal=configuracion_riego_elegida, fecha_eliminacion_criterio=None).count()

        if cant_criterios_riego_finales >= CANTIDAD_MAXIMA_CRITERIO_RIEGO_FINAL_CONFIGURACION_RIEGO:
            raise ValueError(ERROR_DATOS_INCORRECTOS,
                             DETALLE_ERROR_CONFIGURACION_RIEGO_CANTIDAD_MAX_CRITERIO_FINAL)

        # Comprobar que la configuracion elegida sea programada
        tipo_configuracion_riego_programada = TipoConfiguracionRiego.objects.get(
            nombre=TIPO_CONFIGURACION_RIEGO_PROGRAMADO)
        if not configuracion_riego_elegida.tipoConfiguracionRiego == tipo_configuracion_riego_programada:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CONFIGURACION_RIEGO_AUTOMATICA_CRITERIO)

        # Se comprueba que la configuracion elegida no haya sido eliminada
        ultimo_estado_historico = HistoricoEstadoConfiguracionRiego.objects.get(
            configuracion_riego=configuracion_riego_elegida, fechaFinEstadoConfiguracionRiego=None)

        if ultimo_estado_historico.estado_configuracion_riego == estado_configuracion_riego_habilitado \
                or ultimo_estado_historico.estado_configuracion_riego == estado_configuracion_riego_deshabilitado:

            # Se verifica el tipo de criterio riego y se crea el tipo de criterio correspondiente
            if datos[KEY_TIPO_CRITERIO_RIEGO] == TIPO_CRITERIO_RIEGO_MEDICION:

                # Se obtiene el tipo de medicion
                tipo_medicion_elegido = TipoMedicion.objects.get(idTipoMedicion=datos[KEY_ID_TIPO_MEDICION])

                criterio_riego_medicion = CriterioRiegoPorMedicion(
                    nombre=datos[KEY_NOMBRE_CRITERIO_RIEGO],
                    descripcion=datos[KEY_DESCRIPCION_CRITERIO_RIEGO],
                    fecha_creacion_criterio=datetime.now(pytz.utc),
                    valor=datos[KEY_VALOR_MEDICION_CRITERIO_RIEGO],
                    operador=datos[KEY_OPERADOR_MEDICION_CRITERIO_RIEGO],
                    tipo_medicion=tipo_medicion_elegido,
                    configuracionRiegoFinal=configuracion_riego_elegida
                )
                criterio_riego_medicion.save()

                response.content = armar_response_content(criterio_riego_medicion, DETALLE_CRITERIO_RIEGO_CREADO)
                response.status_code = 200
                return response

            elif datos[KEY_TIPO_CRITERIO_RIEGO] == TIPO_CRITERIO_RIEGO_VOLUMEN_AGUA:

                criterio_riego_volumen_agua = CriterioRiegoVolumenAgua(
                    nombre=datos[KEY_NOMBRE_CRITERIO_RIEGO],
                    descripcion=datos[KEY_DESCRIPCION_CRITERIO_RIEGO],
                    fecha_creacion_criterio=datetime.now(pytz.utc),
                    volumen=datos[KEY_VOLUMEN_AGUA_CRITERIO_RIEGO],
                    configuracionRiegoFinal=configuracion_riego_elegida
                )
                criterio_riego_volumen_agua.save()

                response.content = armar_response_content(criterio_riego_volumen_agua,
                                                          DETALLE_CRITERIO_RIEGO_CREADO)
                response.status_code = 200
                return response

            elif datos[KEY_TIPO_CRITERIO_RIEGO] == TIPO_CRITERIO_RIEGO_HORA:

                criterio_riego_hora = CriterioRiegoPorHora(
                    nombre=datos[KEY_NOMBRE_CRITERIO_RIEGO],
                    descripcion=datos[KEY_DESCRIPCION_CRITERIO_RIEGO],
                    fecha_creacion_criterio=datetime.now(pytz.utc),
                    hora=parsear_datos_hora_a_utc(datos[KEY_HORA_INICIO_CRITERIO_RIEGO]),
                    numeroDia=datos[KEY_DIA_INICIO_CRITERIO_RIEGO],
                    configuracionRiegoFinal=configuracion_riego_elegida
                )
                criterio_riego_hora.save()

                response.content = armar_response_content(criterio_riego_hora, DETALLE_CRITERIO_RIEGO_CREADO)
                response.status_code = 200
                return response

            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_TIPO_CRITERIO_RIEGO_INCORRECTO)
        else:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_MODIFICACION_CONFIGURACION_RIEGO)
    else:
        raise KeyError


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
@manejar_errores()
@permisos_rol_requeridos([PERMISO_PUEDECREARCONFIGURACIONRIEGO, PERMISO_PUEDEMODIFICARCONFIGURACIONRIEGO])
def eliminar_criterio_configuracion_riego_mecanismo_riego_finca_sector(request):
    """
    Eliminar un criterio (inicial o final) de una configuracion de riego (solo las 
    configuraciones programadas tienen criterios, las automaticas no)
    :param request: idFinca, idMecanismoRiegoFincaSector, idConfiguracionRiego, idCriterioRiego
    :return:
    """
    datos = obtener_datos_json(request)
    response = HttpResponse()

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

        # Se comprueba que se hayan mandando los datos necesarios
        if KEY_ID_CONFIGURACION_RIEGO not in datos:
            raise KeyError

        if datos[KEY_ID_CONFIGURACION_RIEGO] == "":
            raise ValueError

        if KEY_ID_CRITERIO_RIEGO not in datos:
            raise KeyError

        if datos[KEY_ID_CRITERIO_RIEGO] == "":
            raise ValueError

        # Se obtienen los objetos necesarios para modificar la configuracion
        estado_configuracion_riego_habilitado = EstadoConfiguracionRiego.objects.get(
            nombreEstadoConfiguracionRiego=ESTADO_HABILITADO)
        estado_configuracion_riego_deshabilitado = EstadoConfiguracionRiego.objects.get(
            nombreEstadoConfiguracionRiego=ESTADO_DESHABILITADO)

        # Se obtiene la configuracion elegida
        configuracion_riego_elegida = ConfiguracionRiego.objects.get(
            id_configuracion_riego=datos[KEY_ID_CONFIGURACION_RIEGO])

        # Comprobar que la configuracion elegida se corresponde con el mecanismo finca sector seleccionado
        if not configuracion_riego_elegida.mecanismoRiegoFincaSector == mecanismo_riego_finca_sector_seleccionado:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CONFIGURACION_RIEGO_INCORRECTA)

        # Comprobar que la configuracion elegida sea programada
        tipo_configuracion_riego_programada = TipoConfiguracionRiego.objects.\
            get(nombre=TIPO_CONFIGURACION_RIEGO_PROGRAMADO)
        if not configuracion_riego_elegida.tipoConfiguracionRiego == tipo_configuracion_riego_programada:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CONFIGURACION_RIEGO_AUTOMATICA_CRITERIO)

        # Comprobar que no se este ejecutando el riego para esta configuracion
        if configuracion_tiene_riego_activo(configuracion_riego_elegida):
            raise ValueError(ERROR_MODIFICACION_CONFIGURACION_RIEGO, DETALLE_ERROR_CONFIGURACION_RIEGO_EN_EJECUCION)

        # Se comprueba que la configuracion elegida no haya sido eliminada
        ultimo_estado_historico = HistoricoEstadoConfiguracionRiego.objects.get(
            configuracion_riego=configuracion_riego_elegida, fechaFinEstadoConfiguracionRiego=None)

        if ultimo_estado_historico.estado_configuracion_riego == estado_configuracion_riego_habilitado \
                or ultimo_estado_historico.estado_configuracion_riego == estado_configuracion_riego_deshabilitado:

            # Comprobar que la configuracion elegida se corresponda con el criterio
            try:
                criterio_riego_elegido = CriterioRiego.objects.get_subclass(
                    id_criterio_riego=datos[KEY_ID_CRITERIO_RIEGO], fecha_eliminacion_criterio=None)
            except ObjectDoesNotExist:
                raise ObjectDoesNotExist(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CRITERIO_RIEGO_INEXISTENTE)

            if criterio_riego_elegido.configuracionRiegoInicial != configuracion_riego_elegida \
                    and criterio_riego_elegido.configuracionRiegoFinal != configuracion_riego_elegida:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_RELACION_CONFIGURACION_RIEGO_CRITERIO)

            criterio_riego_elegido.fecha_eliminacion_criterio = datetime.now(pytz.utc)
            criterio_riego_elegido.save()

            response.content = armar_response_content(criterio_riego_elegido,
                                                      DETALLE_CRITERIO_RIEGO_ELIMINADO)
            response.status_code = 200
            return response

        else:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_MODIFICACION_CONFIGURACION_RIEGO)
    else:
        raise KeyError


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
@manejar_errores()
@permisos_rol_requeridos([PERMISO_PUEDECREARCONFIGURACIONRIEGO, PERMISO_PUEDEMODIFICARCONFIGURACIONRIEGO])
def modificar_criterio_configuracion_riego_mecanismo_riego_finca_sector(request):
    """
    Modificar un criterio (inicial o final) de una configuracion de riego (solo las 
    configuraciones programadas tienen criterios, las automaticas no)
    :param request: idFinca, idMecanismoRiegoFincaSector, idConfiguracionRiego, tipoCriterioRiego, idCriterioRiego,
    nombreCriterioRiego, descripcionCriterioRiego, (criterio medicion)idTipoMedicion,
    (criterio medicion)valorMedicionCriterioRiego, (criterio volumen)volumenAguaCriterioRiego,
    (criterio hora)horaInicioCriterioRiego, (criterio hora)diaInicioCriterioRiego
    :return:
    """
    datos = obtener_datos_json(request)
    response = HttpResponse()

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

        # Se comprueba que se hayan mandando los datos necesarios
        if KEY_ID_CONFIGURACION_RIEGO not in datos:
            raise KeyError

        if datos[KEY_ID_CONFIGURACION_RIEGO] == "":
            raise ValueError

        if KEY_ID_CRITERIO_RIEGO not in datos:
            raise KeyError

        if datos[KEY_ID_CRITERIO_RIEGO] == "":
            raise ValueError

        if KEY_NOMBRE_CRITERIO_RIEGO not in datos:
            raise KeyError

        if datos[KEY_NOMBRE_CRITERIO_RIEGO] == "":
            raise ValueError

        if KEY_DESCRIPCION_CRITERIO_RIEGO not in datos:
            raise KeyError

        if KEY_TIPO_CRITERIO_RIEGO not in datos:
            raise KeyError

        if datos[KEY_TIPO_CRITERIO_RIEGO] == TIPO_CRITERIO_RIEGO_MEDICION:

            if KEY_VALOR_MEDICION_CRITERIO_RIEGO not in datos:
                raise KeyError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_CRITERIO_RIEGO_VALOR_MEDICION_INEXISTENTE)

            if datos[KEY_VALOR_MEDICION_CRITERIO_RIEGO] == "":
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_CRITERIO_RIEGO_VALOR_MEDICION_INEXISTENTE)

            if KEY_OPERADOR_MEDICION_CRITERIO_RIEGO not in datos:
                raise KeyError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_CRITERIO_RIEGO_OPERADOR_MEDICION_INEXISTENTE)

            if datos[KEY_OPERADOR_MEDICION_CRITERIO_RIEGO] == "":
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_CRITERIO_RIEGO_OPERADOR_MEDICION_INEXISTENTE)

            if KEY_ID_TIPO_MEDICION not in datos:
                raise KeyError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_CRITERIO_RIEGO_TIPO_MEDICION_INEXISTENTE)

            if datos[KEY_ID_TIPO_MEDICION] == "":
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_CRITERIO_RIEGO_TIPO_MEDICION_INEXISTENTE)

        elif datos[KEY_TIPO_CRITERIO_RIEGO] == TIPO_CRITERIO_RIEGO_VOLUMEN_AGUA:

            if KEY_VOLUMEN_AGUA_CRITERIO_RIEGO not in datos:
                raise KeyError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_CRITERIO_RIEGO_VOLUMEN_INEXISTENTE)

            if datos[KEY_VOLUMEN_AGUA_CRITERIO_RIEGO] == "":
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_CRITERIO_RIEGO_VOLUMEN_INEXISTENTE)

        elif datos[KEY_TIPO_CRITERIO_RIEGO] == TIPO_CRITERIO_RIEGO_HORA:

            if KEY_HORA_INICIO_CRITERIO_RIEGO not in datos:
                raise KeyError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_CRITERIO_RIEGO_HORA_INICIO_INEXISTENTE)

            if datos[KEY_HORA_INICIO_CRITERIO_RIEGO] == "":
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_CRITERIO_RIEGO_HORA_INICIO_INEXISTENTE)

            if KEY_DIA_INICIO_CRITERIO_RIEGO not in datos:
                raise KeyError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_CRITERIO_RIEGO_DIA_INICIO_INEXISTENTE)

            if datos[KEY_DIA_INICIO_CRITERIO_RIEGO] == "":
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_CRITERIO_RIEGO_DIA_INICIO_INEXISTENTE)

        else:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_TIPO_CRITERIO_RIEGO_INCORRECTO)

        # Se obtienen los objetos necesarios para modificar la configuracion
        estado_configuracion_riego_habilitado = EstadoConfiguracionRiego.objects.get(
            nombreEstadoConfiguracionRiego=ESTADO_HABILITADO)
        estado_configuracion_riego_deshabilitado = EstadoConfiguracionRiego.objects.get(
            nombreEstadoConfiguracionRiego=ESTADO_DESHABILITADO)

        # Se obtiene la configuracion elegida
        configuracion_riego_elegida = ConfiguracionRiego.objects.get(
            id_configuracion_riego=datos[KEY_ID_CONFIGURACION_RIEGO])

        # Comprobar que la configuracion elegida se corresponde con el mecanismo finca sector seleccionado
        if not configuracion_riego_elegida.mecanismoRiegoFincaSector == mecanismo_riego_finca_sector_seleccionado:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CONFIGURACION_RIEGO_INCORRECTA)

        # Comprobar que la configuracion elegida sea programada
        tipo_configuracion_riego_programada = TipoConfiguracionRiego.objects.get(
            nombre=TIPO_CONFIGURACION_RIEGO_PROGRAMADO)
        if not configuracion_riego_elegida.tipoConfiguracionRiego == tipo_configuracion_riego_programada:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CONFIGURACION_RIEGO_AUTOMATICA_CRITERIO)

        # Se comprueba que la configuracion elegida no haya sido eliminada
        ultimo_estado_historico = HistoricoEstadoConfiguracionRiego.objects.get(
            configuracion_riego=configuracion_riego_elegida, fechaFinEstadoConfiguracionRiego=None)

        # Comprobar que no se este ejecutando el riego para esta configuracion
        if configuracion_tiene_riego_activo(configuracion_riego_elegida):
            raise ValueError(ERROR_MODIFICACION_CONFIGURACION_RIEGO, DETALLE_ERROR_CONFIGURACION_RIEGO_EN_EJECUCION)

        if ultimo_estado_historico.estado_configuracion_riego == estado_configuracion_riego_habilitado \
                or ultimo_estado_historico.estado_configuracion_riego == estado_configuracion_riego_deshabilitado:

            # Comprobar que la configuracion elegida se corresponda con el criterio
            try:
                criterio_riego_elegido = CriterioRiego.objects.get_subclass(
                    id_criterio_riego=datos[KEY_ID_CRITERIO_RIEGO], fecha_eliminacion_criterio=None)
            except ObjectDoesNotExist:
                raise ObjectDoesNotExist(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CRITERIO_RIEGO_INEXISTENTE)

            if criterio_riego_elegido.configuracionRiegoInicial != configuracion_riego_elegida \
                    and criterio_riego_elegido.configuracionRiegoFinal != configuracion_riego_elegida:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_RELACION_CONFIGURACION_RIEGO_CRITERIO)

            # Se verifica el tipo de criterio riego y se crea el tipo de criterio correspondiente
            if datos[KEY_TIPO_CRITERIO_RIEGO] == TIPO_CRITERIO_RIEGO_MEDICION:

                # Comprobar que el criterio elegido se corresponde con el tipo
                if not isinstance(criterio_riego_elegido, CriterioRiegoPorMedicion):
                    raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_TIPO_CRITERIO_RIEGO_INCORRECTO_MEDICION)

                criterio_riego_medicion_elegido = CriterioRiegoPorMedicion.objects.get(
                    id_criterio_riego=datos[KEY_ID_CRITERIO_RIEGO])

                # Se obtiene el tipo de medicion
                tipo_medicion_elegido = TipoMedicion.objects.get(idTipoMedicion=datos[KEY_ID_TIPO_MEDICION])

                criterio_riego_medicion_elegido.nombre = datos[KEY_NOMBRE_CRITERIO_RIEGO]
                criterio_riego_medicion_elegido.descripcion = datos[KEY_DESCRIPCION_CRITERIO_RIEGO]
                criterio_riego_medicion_elegido.valor = datos[KEY_VALOR_MEDICION_CRITERIO_RIEGO]
                criterio_riego_medicion_elegido.operador = datos[KEY_OPERADOR_MEDICION_CRITERIO_RIEGO]
                criterio_riego_medicion_elegido.tipo_medicion = tipo_medicion_elegido

                criterio_riego_medicion_elegido.save()

                response.content = armar_response_content(criterio_riego_medicion_elegido,
                                                          DETALLE_CRITERIO_RIEGO_MODIFICADO)
                response.status_code = 200
                return response

            elif datos[KEY_TIPO_CRITERIO_RIEGO] == TIPO_CRITERIO_RIEGO_VOLUMEN_AGUA:

                # Comprobar que el criterio elegido se corresponde con el tipo
                if not isinstance(criterio_riego_elegido, CriterioRiegoVolumenAgua):
                    raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_TIPO_CRITERIO_RIEGO_INCORRECTO_VOLUMEN)

                criterio_riego_volumen_agua_elegido = CriterioRiegoVolumenAgua.objects.get(
                    id_criterio_riego=datos[KEY_ID_CRITERIO_RIEGO])

                criterio_riego_volumen_agua_elegido.nombre = datos[KEY_NOMBRE_CRITERIO_RIEGO]
                criterio_riego_volumen_agua_elegido.descripcion = datos[KEY_DESCRIPCION_CRITERIO_RIEGO]
                criterio_riego_volumen_agua_elegido.volumen = datos[KEY_VOLUMEN_AGUA_CRITERIO_RIEGO]

                criterio_riego_volumen_agua_elegido.save()

                response.content = armar_response_content(criterio_riego_volumen_agua_elegido,
                                                          DETALLE_CRITERIO_RIEGO_MODIFICADO)
                response.status_code = 200
                return response

            elif datos[KEY_TIPO_CRITERIO_RIEGO] == TIPO_CRITERIO_RIEGO_HORA:

                # Comprobar que el criterio elegido se corresponde con el tipo
                if not isinstance(criterio_riego_elegido, CriterioRiegoPorHora):
                    raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_TIPO_CRITERIO_RIEGO_INCORRECTO_HORA)

                criterio_riego_hora_elegido = CriterioRiegoPorHora.objects.get(
                    id_criterio_riego=datos[KEY_ID_CRITERIO_RIEGO])

                criterio_riego_hora_elegido.nombre = datos[KEY_NOMBRE_CRITERIO_RIEGO]
                criterio_riego_hora_elegido.descripcion = datos[KEY_DESCRIPCION_CRITERIO_RIEGO]
                criterio_riego_hora_elegido.hora = parsear_datos_hora_a_utc(datos[KEY_HORA_INICIO_CRITERIO_RIEGO])
                criterio_riego_hora_elegido.numeroDia = datos[KEY_DIA_INICIO_CRITERIO_RIEGO]

                criterio_riego_hora_elegido.save()

                response.content = armar_response_content(criterio_riego_hora_elegido,
                                                          DETALLE_CRITERIO_RIEGO_MODIFICADO)
                response.status_code = 200
                return response

            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_TIPO_CRITERIO_RIEGO_INCORRECTO)
        else:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_MODIFICACION_CONFIGURACION_RIEGO)
    else:
        raise KeyError
