# -*- coding: UTF-8 -*-
from django.http import HttpResponse,JsonResponse
from django.db import IntegrityError,transaction
from .supportClases.security_decorators import *

from ..models import *
from supportClases.views_util_functions import *
from supportClases.dto_configuracion_finca import *


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def crear_sector(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if TipoMedicion.objects.filter(idTipoMedicion=datos[KEY_ID_TIPO_MEDICION]).__len__() != 1:
            raise ValueError(ERROR_TIPO_MEDICION_NO_EXISTENTE, "No existe ese tipo de medicion")
        if TipoMedicion.objects.filter(idTipoMedicion=datos[KEY_ID_TIPO_MEDICION], habilitado=True).__len__() != 1:
            raise ValueError(ERROR_TIPO_MEDICION_NO_HABILITADA, "El tipo de medicion seleccionado no esta habilitado")
        tipo_medicion = TipoMedicion.objects.get(idTipoMedicion=datos[KEY_ID_TIPO_MEDICION], habilitado=True)
        if Finca.objects.filter(idFinca=datos[KEY_ID_FINCA]).__len__() != 1:
            raise ValueError(ERROR_FINCA_NO_ENCONTRADA, "No existe la finca ingresada")
        finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
        sensor = Sensor(modelo=datos[KEY_MODELO_SENSOR], fechaAltaSensor=datetime.now(),
                        tipoMedicion=tipo_medicion)
        sensor.save()


        response.content = armar_response_content(None)
        response.status_code = 200
        return response
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])
    except (IntegrityError,ValueError) as err:
        print err.args
        response.status_code=401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")



@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def mostrar_sensores_finca(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if Finca.objects.filter(idFinca=datos[KEY_ID_FINCA]).__len__() != 1:
            raise ValueError(ERROR_FINCA_NO_ENCONTRADA, "No existe la finca ingresada")
        finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
        sensores_lista = finca.sensor_set.filter(habilitado=True)
        response.content = armar_response_list_content(sensores_lista)
        response.status_code = 200
        return response
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])
    except (IntegrityError,ValueError) as err:
        print err.args
        response.status_code=401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_GET])
def mostrar_tipo_medicion(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        tipo_medicion_lista = TipoMedicion.objects.filter(habilitado=True)
        response.content = armar_response_list_content(tipo_medicion_lista)
        response.status_code = 200
        return response
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])
    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


