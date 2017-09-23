# -*- coding: UTF-8 -*-
from django.http import HttpResponse,JsonResponse
from django.db import IntegrityError,transaction
from .supportClases.security_decorators import *

from ..models import *
from supportClases.views_util_functions import *


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def mostrarMecanismosRiegoFinca(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        finca_actual = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
        estado_mecanismo_habilitado = EstadoMecanismoRiegoFinca.objects.get(nombreEstadoMecanismoRiegoFinca=
                                                                            ESTADO_HABILITADO)
        mecanismo_riego_finca_list = MecanismoRiegoFinca.objects.filter(finca=finca_actual)
        mecanismos_habilitados_list = []
        for mecanismo in mecanismo_riego_finca_list:
            if (HistoricoMecanismoRiegoFinca.objects.filter(mecanismo_riego_finca=mecanismo,
                                                            fechaFinEstadoMecanismoRiegoFinca__isnull=True,
                                                            estado_mecanismo_riego_finca=estado_mecanismo_habilitado))\
                    .__len__() == 1:
                mecanismos_habilitados_list.append(mecanismo)
        response.content = armar_response_list_content(mecanismos_habilitados_list)
        response.status_code = 200
        return response
    except (IntegrityError,ValueError) as err:
        print err.args
        response.status_code=401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def mostrar_mecanismos_nuevos(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        finca_actual = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
        mecanismo_riego_finca_list = MecanismoRiegoFinca.objects.filter(finca=finca_actual)
        tipo_mecanismo_existente_list=[]
        for mecanismo_riego in mecanismo_riego_finca_list:
            tipo_mecanismo_existente_list.append(mecanismo_riego.tipoMecanismoRiego)
        tipo_mecanismo_riego_list = TipoMecanismoRiego.objects.filter(habilitado=True)
        tipo_mecanismo_riego_nuevo_list = []
        for tipo_mecanismo in tipo_mecanismo_riego_list:
            if tipo_mecanismo_existente_list.__contains__(tipo_mecanismo)==False:
                tipo_mecanismo_riego_nuevo_list.append(tipo_mecanismo)
        response.content = armar_response_list_content(tipo_mecanismo_riego_nuevo_list)
        response.status_code=200
        return response
    except (IntegrityError, TypeError, KeyError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_PUT])
def agregar_mecanismo_riego_finca(request):
    response=HttpResponse()
    datos = obtener_datos_json(request)
    try:
        tipo_mecanismo = TipoMecanismoRiego.objects.get(nombreMecanismo=datos[KEY_NOMBRE_TIPO_MECANISMO])
        estado_habilitado = EstadoMecanismoRiegoFinca.objects.get(nombreEstadoMecanismoRiegoFinca=ESTADO_HABILITADO)
        historico_nuevo = HistoricoMecanismoRiegoFinca(fechaInicioEstadoMecanismoRiegoFinca=datetime.now(),
                                                     estado_mecanismo_riego_finca=estado_habilitado)

        finca_actual = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])

        mecanismo_riego_finca = MecanismoRiegoFinca(finca=finca_actual, tipoMecanismoRiego=tipo_mecanismo,
                                                  fechaInstalacion=datetime.now())
        mecanismo_riego_finca.save()
        historico_nuevo.mecanismo_riego_finca = mecanismo_riego_finca
        mecanismo_riego_finca.historicoMecanismoRiegoFincaList.add(historico_nuevo, bulk=False)
        historico_nuevo.save()
        mecanismo_riego_finca.save()
        response.content = armar_response_content(None)
        response.status_code = 200
        return response
    except (IntegrityError, TypeError, KeyError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def deshabilitar_mecanismo_riego_finca(request):
    response=HttpResponse()
    datos = obtener_datos_json(request)
    try:
        mecanismo_riego_finca = MecanismoRiegoFinca.objects.get(idMecanismoRiegoFinca=
                                                                datos[KEY_ID_MECANISMO_RIEGO_FINCA])
        ultimo_historico_mecanismo_finca = HistoricoMecanismoRiegoFinca.objects.get(
            mecanismo_riego_finca=mecanismo_riego_finca, fechaFinEstadoMecanismoRiegoFinca__isnull=True )
        ultimo_historico_mecanismo_finca.fechaFinEstadoMecanismoRiegoFinca = datetime.now()
        ultimo_historico_mecanismo_finca.save()
        estado_mecanismo_finca_deshabilitado = EstadoMecanismoRiegoFinca.objects.get(nombreEstadoMecanismoRiegoFinca=
                                                                                     ESTADO_DESHABILITADO)
        nuevo_historico_mecanismo_finca = HistoricoMecanismoRiegoFinca(estado_mecanismo_riego_finca=
                                                                       estado_mecanismo_finca_deshabilitado,
                                                                       fechaInicioEstadoMecanismoRiegoFinca=
                                                                       datetime.now(),
                                                                       mecanismo_riego_finca=mecanismo_riego_finca)
        nuevo_historico_mecanismo_finca.save()
        mecanismo_riego_finca.save()
        estado_mecanismo_sector_deshabilitado = EstadoMecanismoRiegoFincaSector.objects.get(
            nombreEstadoMecanismoRiegoFincaSector=ESTADO_DESHABILITADO)
        estado_mecanismo_sector_habilitado = EstadoMecanismoRiegoFincaSector.objects.get(
            nombreEstadoMecanismoRiegoFincaSector=ESTADO_HABILITADO)
        mecanismo_riego_sector_lista = mecanismo_riego_finca.mecanismoRiegoSectorList.all()
        for mecanismo_sector in mecanismo_riego_sector_lista:
            if HistoricoMecanismoRiegoFincaSector.objects.filter(estado_mecanismo_riego_finca_sector=
                                                                 estado_mecanismo_sector_habilitado,
                                                                 fechaFinEstadoMecanismoRiegoFincaSector__isnull=True).__len__() == 1:
                ultimo_historico_mecanismo_sector = HistoricoMecanismoRiegoFincaSector.objects.get(estado_mecanismo_riego_finca_sector=
                                                                 estado_mecanismo_sector_habilitado,
                                                                 fechaFinEstadoMecanismoRiegoFincaSector__isnull=True)
                ultimo_historico_mecanismo_sector.fechaFinEstadoMecanismoRiegoFincaSector = datetime.now()
                ultimo_historico_mecanismo_sector.save()
                nuevo_historico_mecanismo_sector = HistoricoMecanismoRiegoFincaSector(
                    estado_mecanismo_riego_finca_sector=estado_mecanismo_sector_deshabilitado,
                    fechaInicioEstadoMecanismoRiegoFincaSector=datetime.now(),
                    mecanismo_riego_finca_sector=mecanismo_sector)
                nuevo_historico_mecanismo_sector.save()
        mecanismo_riego_finca.save()
        response.content = armar_response_content(None)
        response.status_code = 200
        return response
    except (IntegrityError, TypeError, KeyError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")