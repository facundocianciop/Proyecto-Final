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
def crear_sensor(request):
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
def deshabilitar_sensor(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if Sensor.objects.filter(idSensor=datos[KEY_ID_SENSOR]).__len__() == 0:
            raise ValueError(ERROR_SENSOR_NO_EXISTENTE, "No existe el sensor con ese id")
        sensor = Sensor.objects.get(idSensor=datos[KEY_ID_SENSOR])
        sensor.habilitado = False
        sensor.save()
        response.content = armar_response_content(None)
        response.status_code = 200
        return response
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])
    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
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


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def crear_componente_sensor(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if Sensor.objects.filter(idSensor=datos[KEY_ID_SENSOR]).__len__() == 0:
            raise ValueError(ERROR_SENSOR_NO_EXISTENTE, "No existe el sensor con ese id")
        sensor = Sensor.objects.get(idSensor=KEY_ID_SENSOR)
        if Finca.objects.filter(idFinca=datos[KEY_ID_FINCA]).__len__() != 1:
            raise ValueError(ERROR_FINCA_NO_ENCONTRADA, "No existe la finca ingresada")
        finca = Finca.objects.get(idFinca=KEY_ID_FINCA)
        if Sensor.finca != finca:
            raise ValueError(ERROR_SENSOR_NO_PERTENECE_A_FINCA, "Ese sensor no pertence a la finca ingresada")

        componente = ComponenteSensor(numeroComponente=datos[KEY_NUMERO_COMPONENTE_SENSOR])

        response.content = armar_response_content(None)
        response.status_code = 200
        return response
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])
    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def buscar_sensores_no_asignados(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if Finca.objects.filter(idFinca=datos[KEY_ID_FINCA]).__len__() != 1:
            raise ValueError(ERROR_FINCA_NO_ENCONTRADA, "No existe la finca ingresada")
        finca = Finca.objects.get(idFinca=KEY_ID_FINCA)
        lista_sensores = Sensor.objects.filter(finca=finca)
        lista_sensores_no_asignados = []
        for sensor in lista_sensores:
            if AsignacionSensorComponente.objects.filter(sensor=sensor, fechaBaja__isnull=True).__len__() == 0:
                lista_sensores_no_asignados.append(sensor)

        response.content = armar_response_list_content(lista_sensores_no_asignados)
        response.status_code = 200
        return response
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])
    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def mostrar_componentes_sensor_finca_habilitados(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if Finca.objects.filter(idFinca=datos[KEY_ID_FINCA]).__len__() != 1:
            raise ValueError(ERROR_FINCA_NO_ENCONTRADA, "No existe la finca ingresada")
        finca = Finca.objects.get(idFinca=KEY_ID_FINCA)
        estado_habilitado = EstadoComponenteSensor.objects.get(nombreEstado=ESTADO_HABILITADO)
        lista_componentes_sensores = ComponenteSensor.objects.filter(finca=finca)
        lista_componentes_sensores_habilitados = []
        for componente in lista_componentes_sensores:
            if HistoricoEstadoComponenteSensor.objects.filter(fechaFinEstadoComponenteSensor__isnull=True,
                                                              componenteSensor=componente,
                                                              estadoComponenteSensor=estado_habilitado).__len__() == 0:
                lista_componentes_sensores_habilitados.append(componente)

        response.content = armar_response_content(lista_componentes_sensores)
        response.status_code = 200
        return response
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])
    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def mostrar_componentes_sensor_finca(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if Finca.objects.filter(idFinca=datos[KEY_ID_FINCA]).__len__() != 1:
            raise ValueError(ERROR_FINCA_NO_ENCONTRADA, "No existe la finca ingresada")
        finca = Finca.objects.get(idFinca=KEY_ID_FINCA)
        estado_habilitado = EstadoComponenteSensor.objects.get(nombreEstado=ESTADO_HABILITADO)
        lista_componentes_sensores = ComponenteSensor.objects.filter(finca=finca)
        lista_componentes_sensores_habilitados = []
        for componente in lista_componentes_sensores:
            if HistoricoEstadoComponenteSensor.objects.filter(fechaFinEstadoComponenteSensor__isnull=True,
                                                              componenteSensor=componente,
                                                              estadoComponenteSensor=estado_habilitado).__len__() == 0:
                lista_componentes_sensores_habilitados.append(componente)

        response.content = armar_response_content(lista_componentes_sensores)
        response.status_code = 200
        return response
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])
    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")