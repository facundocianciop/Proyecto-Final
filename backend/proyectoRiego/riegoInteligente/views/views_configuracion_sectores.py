# -*- coding: UTF-8 -*-
from django.db import IntegrityError,transaction
from .supportClases.security_decorators import *
from ..models import *
from supportClases.views_util_functions import *
from supportClases.error_handler import *


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_PUT])
def crearSector(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        finca_actual = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
        estado_habilitado = EstadoSector.objects.get(nombreEstadoSector=ESTADO_HABILITADO)

        if Sector.objects.filter(numeroSector=datos[KEY_NUMERO_SECTOR], finca= finca_actual).__len__() == 1:
            sector = Sector.objects.get(numeroSector=datos[KEY_NUMERO_SECTOR], finca= finca_actual)
            if sector.historicoEstadoSectorList.filter(fechaFinEstadoSector__isnull=True,
                                                       estado_sector=estado_habilitado).__len__() == 1:
                raise ValueError(ERROR_SECTOR_YA_EXISTENTE,"Ya existe un sector con ese numero")
        if Sector.objects.filter(nombreSector=datos[KEY_NOMBRE_SECTOR], finca=finca_actual).__len__() == 1:
            sector = Sector.objects.get(numeroSector=datos[KEY_NOMBRE_SECTOR], finca=finca_actual)
            if sector.historicoEstadoSectorList.filter(fechaFinEstadoSector__isnull=True,
                                                       estado_sector=estado_habilitado).__len__() ==1:
                raise ValueError(ERROR_SECTOR_YA_EXISTENTE, "Ya existe un sector con ese nombre")
        sector_nuevo = Sector(numeroSector=datos[KEY_NUMERO_SECTOR], nombreSector=datos[KEY_NOMBRE_SECTOR],
                              descripcionSector=datos[KEY_DESCRIPCION_SECTOR], superficie=datos[KEY_SUPERFICIE_SECTOR],
                              finca=finca_actual
                              )
        sector_nuevo.save()
        historico_nuevo = HistoricoEstadoSector(estado_sector=estado_habilitado, sector=sector_nuevo,
                                                fechaInicioEstadoSector=datetime.now())
        historico_nuevo.save()
        finca_actual.save()
        response.content = armar_response_content(None)
        response.status_code = 200
        return response
    except ValueError as err:
        return build_bad_request_error(response, err.args[0], err.args[1])
    except (IntegrityError, TypeError, KeyError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def modificarSector(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:

        sector_seleccionado = Sector.objects.get(idSector=datos[KEY_ID_SECTOR])
        estado_habilitado = EstadoSector.objects.get(nombreEstadoSector=ESTADO_HABILITADO)
        if HistoricoEstadoSector.objects.filter(sector=sector_seleccionado, estado_sector=estado_habilitado,
                                                             fechaFinEstadoSector__isnull=True).__len__() != 1:
            raise ValueError(ERROR_SECTOR_NO_HABILITADO, "El sector seleccionado no esta habilitado")

        sector_seleccionado.nombreSector = datos[KEY_NOMBRE_SECTOR]
        sector_seleccionado.descripcionSector = datos[KEY_DESCRIPCION_SECTOR]
        sector_seleccionado.superficie = datos[KEY_SUPERFICIE_SECTOR]
        sector_seleccionado.save()
        response.content = armar_response_content(None)
        response.status_code = 200
        return response
    except ValueError as err:
        return build_bad_request_error(response,err.args[0], err.args[1])
    except (IntegrityError, TypeError, KeyError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def eliminarSector(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:

        sector_seleccionado = Sector.objects.get(idSector=datos[KEY_ID_SECTOR])
        estado_habilitado = EstadoSector.objects.get(nombreEstadoSector=ESTADO_HABILITADO)
        if HistoricoEstadoSector.objects.filter(sector=sector_seleccionado, estado_sector=estado_habilitado,
                                                             fechaFinEstadoSector__isnull=True).__len__() != 1:
            raise ValueError(ERROR_SECTOR_NO_HABILITADO, "El sector seleccionado no esta habilitado")
        historico_viejo = HistoricoEstadoSector.objects.get(sector=sector_seleccionado, estado_sector=estado_habilitado,
                                                            fechaFinEstadoSector__isnull=True)
        historico_viejo.fechaFinEstadoSector = datetime.now()
        historico_viejo.save()
        estado_deshabilitado = EstadoSector.objects.get(nombreEstadoSector=ESTADO_DESHABILITADO)
        historico_nuevo = HistoricoEstadoSector(fechaInicioEstadoSector=datetime.now(),
                                                estado_sector=estado_deshabilitado)
        sector_seleccionado.historicoEstadoSectorList.add(historico_nuevo, bulk=False)
        sector_seleccionado.save()
        mecanismo_riego_sector_lista = MecanismoRiegoFincaSector.objects.filter(sector= sector_seleccionado)
        estado_mecanismo_riego_sector_habilitado = EstadoMecanismoRiegoFincaSector.objects.get(nombreEstadoMecanismoRiegoFincaSector=ESTADO_HABILITADO)
        for mecanismo_riego_sector in mecanismo_riego_sector_lista:
            if mecanismo_riego_sector.historicoMecanismoRiegoFincaSector.filter(fechaFinEstadoMecanismoRiegoFincaSector__isnull=True, estado_mecanismo_riego_finca_sector=
                                                                                estado_mecanismo_riego_sector_habilitado).__len__() == 1:
                mecanismo_riego_sector_deshabilitar = mecanismo_riego_sector
                ultimo_historico_mecanismo_riego_sector = mecanismo_riego_sector.historicoMecanismoRiegoFincaSector.get(fechaFinEstadoMecanismoRiegoFincaSector__isnull=True, estado_mecanismo_riego_finca_sector=
                estado_mecanismo_riego_sector_habilitado)
                ultimo_historico_mecanismo_riego_sector.fechaFinEstadoMecanismoRiegoFincaSector = datetime.now()
                ultimo_historico_mecanismo_riego_sector.save()
                estado_mecanismo_riego_sector_deshabilitado = EstadoMecanismoRiegoFincaSector.objects.get(nombreEstadoMecanismoRiegoFincaSector=ESTADO_DESHABILITADO)
                nuevo_historico_mecanismo_riego_sector = HistoricoMecanismoRiegoFincaSector(mecanismo_riego_finca_sector=mecanismo_riego_sector_deshabilitar,
                                                                                    fechaInicioEstadoMecanismoRiegoFincaSector= datetime.now(),
                                                                                    estado_mecanismo_riego_finca_sector=estado_mecanismo_riego_sector_deshabilitado)
                nuevo_historico_mecanismo_riego_sector.save()

                response.content = armar_response_content(None)
                response.status_code = 200
                return response
    except ValueError as err:
        return build_bad_request_error(response,err.args[0], err.args[1])
    except (IntegrityError, TypeError, KeyError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")
@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def mostrarSectores(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        finca_actual = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
        estado_habilitado = EstadoSector.objects.get(nombreEstadoSector=ESTADO_HABILITADO)
        lista_sectores = Sector.objects.filter(finca=finca_actual)
        sectores_habilitados = []
        for sector in lista_sectores:
            if HistoricoEstadoSector.objects.filter(sector=sector, fechaFinEstadoSector__isnull=True,
                                                                 estado_sector=estado_habilitado).__len__() ==1:
                sectores_habilitados.append(sector)

        response.content = armar_response_list_content(sectores_habilitados)
        response.status_code = 200
        return response
    except ValueError as err:
        return build_bad_request_error(response,err.args[0], err.args[1])
    except (IntegrityError, TypeError, KeyError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")

@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_PUT])
def asignarMecanismoASector(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        mecanismo_riego_finca_seleccionado = MecanismoRiegoFinca.objects.get(idMecanismoRiegoFinca=
                                                                             datos[KEY_ID_MECANISMO_RIEGO_FINCA])
        historico_mecanismo_riego_finca_actual = mecanismo_riego_finca_seleccionado.historicoMecanismoRiegoFincaList.\
            get(fechaFinEstadoMecanismoRiegoFinca__isnull=True)
        if historico_mecanismo_riego_finca_actual.estado_mecanismo_riego_finca.nombreEstadoMecanismoRiegoFinca \
                != ESTADO_HABILITADO:
            raise ValueError(ERROR_MECANISMO_RIEGO_FINCA_NO_HABILITADO,
                             "El mecanismo seleccionado no se encuentra habilitado para la finca")
        sector_seleccionado = Sector.objects.get(idSector=datos[KEY_ID_SECTOR])
        historico_sector_seleccionado_actual = sector_seleccionado.historicoEstadoSectorList.get\
            (fechaFinEstadoSector__isnull=True)
        if historico_sector_seleccionado_actual.estado_sector.nombreEstadoSector != ESTADO_HABILITADO:
            raise ValueError(ERROR_SECTOR_NO_HABILITADO, "El sector seleccionado no se encuentra habilitado")
        mecanismo_riego_sector = MecanismoRiegoFincaSector(mecanismo_riego_finca=mecanismo_riego_finca_seleccionado,
                                                           sector=sector_seleccionado)
        if KEY_MECANISMO_RIEGO_CAUDAL in datos:
            mecanismo_riego_sector.caudal = datos[KEY_MECANISMO_RIEGO_CAUDAL]
        else:
            mecanismo_riego_sector.caudal = mecanismo_riego_finca_seleccionado.tipoMecanismoRiego.caudalEstandar
        if KEY_MECANISMO_RIEGO_PRESION in datos:
            mecanismo_riego_sector.presion = datos[KEY_MECANISMO_RIEGO_PRESION]
        else:
            mecanismo_riego_sector.presion = mecanismo_riego_finca_seleccionado.tipoMecanismoRiego.presionEstandar
        mecanismo_riego_sector.save()
        estado_mecanismo_riego_finca_sector_habilitado = EstadoMecanismoRiegoFincaSector.objects.get(
            nombreEstadoMecanismoRiegoFincaSector=ESTADO_HABILITADO)
        nuevo_historico = HistoricoMecanismoRiegoFincaSector(fechaInicioEstadoMecanismoRiegoFincaSector=datetime.now(),
                                                             estado_mecanismo_riego_finca_sector=
                                                             estado_mecanismo_riego_finca_sector_habilitado)
        mecanismo_riego_sector.historicoMecanismoRiegoFincaSector.add(nuevo_historico, bulk=False)
        mecanismo_riego_sector.save()
        response.content = armar_response_content(None)
        response.status_code = 200
        return response


    except ValueError as err:
        return build_bad_request_error(response, err.args[0], err.args[1])
    except (IntegrityError, TypeError, KeyError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")
