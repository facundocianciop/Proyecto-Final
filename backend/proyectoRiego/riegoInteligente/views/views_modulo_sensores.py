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
@manejar_errores()
@permisos_rol_requeridos([PERMISO_PUEDEGESTIONARSENSORES])
def crear_sensor(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if (KEY_ID_TIPO_MEDICION and KEY_ID_FINCA and KEY_MODELO_SENSOR) in datos:
            if datos[KEY_ID_FINCA] == '' or datos[KEY_ID_TIPO_MEDICION] == '' or datos[KEY_MODELO_SENSOR] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if TipoMedicion.objects.filter(idTipoMedicion=datos[KEY_ID_TIPO_MEDICION]).__len__() != 1:
                raise ValueError(ERROR_TIPO_MEDICION_NO_EXISTENTE, "No existe ese tipo de medicion")
            if TipoMedicion.objects.filter(idTipoMedicion=datos[KEY_ID_TIPO_MEDICION], habilitado=True).__len__() != 1:
                raise ValueError(ERROR_TIPO_MEDICION_NO_HABILITADA, "El tipo de medicion seleccionado no esta habilitado")
            tipo_medicion = TipoMedicion.objects.get(idTipoMedicion=datos[KEY_ID_TIPO_MEDICION], habilitado=True)
            if Finca.objects.filter(idFinca=datos[KEY_ID_FINCA]).__len__() != 1:
                raise ValueError(ERROR_FINCA_NO_ENCONTRADA, "No existe la finca ingresada")
            finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
            sensor = Sensor(modelo=datos[KEY_MODELO_SENSOR], fechaAltaSensor=datetime.now(pytz.utc),
                            tipoMedicion=tipo_medicion, finca=finca, habilitado=True)
            sensor.save()
            response.content = armar_response_content(None)
            response.status_code = 200
            return response
        else:
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
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
@manejar_errores()
def buscar_sensores_componente(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if KEY_ID_COMPONENTE_SENSOR in datos:
            if datos[KEY_ID_COMPONENTE_SENSOR] == '' :
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if ComponenteSensor.objects.filter(idComponenteSensor=datos[KEY_ID_COMPONENTE_SENSOR]).__len__() != 1:
                raise ValueError(ERROR_COMPONENTE_SENSOR_NO_EXISTENTE
                                 , "No existe ese componente sensor")
            componente_sensor = ComponenteSensor.objects.get(idComponenteSensor=datos[KEY_ID_COMPONENTE_SENSOR])
            if componente_sensor.asignaciones_list.filter(fechaBaja__isnull=True).__len__() == 0:
                response.content = armar_response_content(None)
                response.status_code = 200
                return response
            asignaciones = componente_sensor.asignaciones_list.filter(fechaBaja__isnull=True)
            lista_sensores = []
            for asignacion in asignaciones:
                lista_sensores.append(asignacion.sensor)
            response.content = armar_response_list_content(lista_sensores)
            response.status_code = 200
            return response
        else:
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
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
@manejar_errores()
@permisos_rol_requeridos([PERMISO_PUEDEGESTIONARSENSORES])
def deshabilitar_sensor(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if (KEY_ID_SENSOR) in datos:
            if datos[KEY_ID_SENSOR] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if Sensor.objects.filter(idSensor=datos[KEY_ID_SENSOR]).__len__() == 0:
                raise ValueError(ERROR_SENSOR_NO_EXISTENTE, "No existe el sensor con ese id")
            sensor = Sensor.objects.get(idSensor=datos[KEY_ID_SENSOR])
            sensor.habilitado = False
            sensor.fechaBajaSensor = datetime.now(pytz.utc)
            sensor.save()
            response.content = armar_response_content(None)
            response.status_code = 200
            return response
        else:
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
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
@manejar_errores()
@permisos_rol_requeridos([PERMISO_PUEDEGESTIONARSENSORES])
def modificar_sensor(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if (KEY_ID_TIPO_MEDICION and KEY_MODELO_SENSOR and KEY_ID_SENSOR) in datos:
            if datos[KEY_ID_TIPO_MEDICION] == '' or datos[KEY_MODELO_SENSOR] == '' or datos[KEY_ID_SENSOR] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if TipoMedicion.objects.filter(idTipoMedicion=datos[KEY_ID_TIPO_MEDICION]).__len__() != 1:
                raise ValueError(ERROR_TIPO_MEDICION_NO_EXISTENTE, "No existe ese tipo de medicion")
            if TipoMedicion.objects.filter(idTipoMedicion=datos[KEY_ID_TIPO_MEDICION], habilitado=True).__len__() != 1:
                raise ValueError(ERROR_TIPO_MEDICION_NO_HABILITADA, "El tipo de medicion seleccionado no esta habilitado")
            if Sensor.objects.filter(idSensor=datos[KEY_ID_SENSOR]).__len__() == 0:
                raise ValueError(ERROR_SENSOR_NO_EXISTENTE, "No existe sensor con ese id")
            if Sensor.objects.filter(idSensor=datos[KEY_ID_SENSOR], habilitado=True).__len__() == 0:
                raise ValueError(ERROR_SENSOR_NO_HABILITADO, "El sensor esta deshabilitado")
            tipo_medicion = TipoMedicion.objects.get(idTipoMedicion=datos[KEY_ID_TIPO_MEDICION], habilitado=True)
            sensor = Sensor.objects.get(idSensor=datos[KEY_ID_SENSOR])
            sensor.modelo = datos[KEY_MODELO_SENSOR]
            if sensor.tipoMedicion != tipo_medicion:
                sensor.tipoMedicion = tipo_medicion
            sensor.save()
            response.content = armar_response_content(None)
            response.status_code = 200
            return response
        else:
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
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
@manejar_errores()
def mostrar_sensores_finca(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if (KEY_ID_FINCA) in datos:
            if datos[KEY_ID_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if Finca.objects.filter(idFinca=datos[KEY_ID_FINCA]).__len__() != 1:
                raise ValueError(ERROR_FINCA_NO_ENCONTRADA, "No existe la finca ingresada")
            finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
            sensores_lista = finca.sensor_set.filter(habilitado=True)
            response.content = armar_response_list_content(sensores_lista)
            response.status_code = 200
            return response
        else:
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
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
@manejar_errores()
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
@manejar_errores()
@permisos_rol_requeridos([PERMISO_PUEDEGESTIONARSENSORES, PERMISO_PUEDEASIGNARCOMPONENTESENSOR])
def crear_componente_sensor(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if (KEY_ID_FINCA in datos) and (KEY_MODELO_COMPONENTE in datos) and (KEY_DESCRIPCION_COMPONENTE in datos) \
                and (KEY_CANTIDAD_MAXIMA_SENSORES in datos):
            if datos[KEY_ID_FINCA] == '' or datos[KEY_MODELO_COMPONENTE] == '' \
                    or datos[KEY_DESCRIPCION_COMPONENTE] == '' or datos[KEY_CANTIDAD_MAXIMA_SENSORES] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if Finca.objects.filter(idFinca=datos[KEY_ID_FINCA]).__len__() != 1:
                raise ValueError(ERROR_FINCA_NO_ENCONTRADA, "No existe la finca ingresada")
            finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
            componente = ComponenteSensor(descripcion=datos[KEY_DESCRIPCION_COMPONENTE], finca=finca,
                                          modelo=datos[KEY_MODELO_COMPONENTE],
                                          cantidadMaximaSensores=datos[KEY_CANTIDAD_MAXIMA_SENSORES])
            estado_habilitado = EstadoComponenteSensor.objects.get(nombreEstado=ESTADO_HABILITADO)
            historico_nuevo = HistoricoEstadoComponenteSensor(componenteSensor=componente,
                                                              estadoComponenteSensor=estado_habilitado,
                                                              fechaInicioEstadoComponenteSensor=datetime.now(pytz.utc))
            componente.save()
            historico_nuevo.save()
            response.content = armar_response_content(None)
            response.status_code = 200
            return response
        else:
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
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
@manejar_errores()
@permisos_rol_requeridos([PERMISO_PUEDEGESTIONARSENSORES])
def modificar_componente_sensor(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if (KEY_ID_FINCA in datos) and (KEY_ID_COMPONENTE_SENSOR in datos) and (KEY_MODELO_COMPONENTE in datos) and\
                (KEY_DESCRIPCION_COMPONENTE in datos) and (KEY_CANTIDAD_MAXIMA_SENSORES in datos):
            if datos[KEY_ID_FINCA] == '' or datos[KEY_ID_COMPONENTE_SENSOR] == '' or datos[KEY_MODELO_COMPONENTE] == '' \
                    or datos[KEY_CANTIDAD_MAXIMA_SENSORES] == '' or datos[KEY_DESCRIPCION_COMPONENTE] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if Finca.objects.filter(idFinca=datos[KEY_ID_FINCA]).__len__() != 1:
                raise ValueError(ERROR_FINCA_NO_ENCONTRADA, "No existe la finca ingresada")
            finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
            if ComponenteSensor.objects.filter(idComponenteSensor=datos[KEY_ID_COMPONENTE_SENSOR],
                                               finca=finca).__len__() == 0:
                raise ValueError(ERROR_COMPONENTE_SENSOR_NO_PERTENECE_A_FINCA,
                                 "El componente no pertenece a la finca ingresada")
            if ComponenteSensor.objects.filter(idComponenteSensor=datos[KEY_ID_COMPONENTE_SENSOR]).__len__() == 0:
                raise ValueError(ERROR_COMPONENTE_SENSOR_NO_EXISTENTE, "No existe componente sensor con ese id")
            componente = ComponenteSensor.objects.get(idComponenteSensor=datos[KEY_ID_COMPONENTE_SENSOR])
            componente.modelo = datos[KEY_MODELO_COMPONENTE]
            componente.descripcion = datos[KEY_DESCRIPCION_COMPONENTE]
            componente.cantidadMaximaSensores = datos[KEY_CANTIDAD_MAXIMA_SENSORES]
            componente.save()
            response.content = armar_response_content(None)
            response.status_code = 200
            return response
        else:
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
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
@manejar_errores()
@permisos_rol_requeridos([PERMISO_PUEDEGESTIONARSENSORES, PERMISO_PUEDEASIGNARCOMPONENTESENSOR])
def habilitar_componente_sensor(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if (KEY_ID_FINCA in datos) and (KEY_ID_COMPONENTE_SENSOR in datos):
            if datos[KEY_ID_FINCA] == '' or datos[KEY_ID_COMPONENTE_SENSOR] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if Finca.objects.filter(idFinca=datos[KEY_ID_FINCA]).__len__() != 1:
                raise ValueError(ERROR_FINCA_NO_ENCONTRADA, "No existe la finca ingresada")
            finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
            if ComponenteSensor.objects.filter(idComponenteSensor=datos[KEY_ID_COMPONENTE_SENSOR],
                                               finca=finca).__len__() == 0:
                raise ValueError(ERROR_COMPONENTE_SENSOR_NO_PERTENECE_A_FINCA,
                                 "El componente no pertenece a la finca ingresada")
            if ComponenteSensor.objects.filter(idComponenteSensor=datos[KEY_ID_COMPONENTE_SENSOR]).__len__() == 0:
                raise ValueError(ERROR_COMPONENTE_SENSOR_NO_EXISTENTE, "No existe componente sensor con ese id")
            componente = ComponenteSensor.objects.get(idComponenteSensor=datos[KEY_ID_COMPONENTE_SENSOR])
            ultimo_historico = componente.historico_estado_componente_sensor_list.get(fechaFinEstadoComponenteSensor__isnull=True)
            if ultimo_historico.estadoComponenteSensor.nombreEstado == ESTADO_HABILITADO:
                raise ValueError(ERROR_COMPONENTE_SENSOR_YA_HABILITADO, "El componente sensor ya esta habilitado")
            ultimo_historico.fechaFinEstadoComponenteSensor = datetime.now(pytz.utc)
            ultimo_historico.save()
            estado_habilitado = EstadoComponenteSensor.objects.get(nombreEstado=ESTADO_HABILITADO)
            nuevo_historico = HistoricoEstadoComponenteSensor(estadoComponenteSensor=estado_habilitado,
                                                              componenteSensor=componente,
                                                              fechaInicioEstadoComponenteSensor=datetime.now(pytz.utc))
            nuevo_historico.save()
            componente.save()
            response.content = armar_response_content(None)
            response.status_code = 200
            return response
        else:
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
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
@manejar_errores()
def buscar_componente_sensor_por_id(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if KEY_ID_COMPONENTE_SENSOR in datos:
            if datos[KEY_ID_COMPONENTE_SENSOR] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if ComponenteSensor.objects.filter(idComponenteSensor=datos[KEY_ID_COMPONENTE_SENSOR]).__len__() != 1:
                raise ValueError(ERROR_COMPONENTE_SENSOR_NO_EXISTENTE, "No existe el componenten sensor ingresado")
            componente_sensor = ComponenteSensor.objects.get(idComponenteSensor=datos[KEY_ID_COMPONENTE_SENSOR])
            response.content = armar_response_content(componente_sensor)
            response.status_code = 200
            return response
        else:
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
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
@manejar_errores()
@permisos_rol_requeridos([PERMISO_PUEDEGESTIONARSENSORES, PERMISO_PUEDEASIGNARCOMPONENTESENSOR])
def deshabilitar_componente_sensor(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if (KEY_ID_FINCA in datos) and (KEY_ID_COMPONENTE_SENSOR in datos):
            if datos[KEY_ID_FINCA] == '' or datos[KEY_ID_COMPONENTE_SENSOR] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if Finca.objects.filter(idFinca=datos[KEY_ID_FINCA]).__len__() != 1:
                raise ValueError(ERROR_FINCA_NO_ENCONTRADA, "No existe la finca ingresada")
            finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
            if ComponenteSensor.objects.filter(idComponenteSensor=datos[KEY_ID_COMPONENTE_SENSOR],
                                               finca=finca).__len__() == 0:
                raise ValueError(ERROR_COMPONENTE_SENSOR_NO_PERTENECE_A_FINCA,
                                 "El componente no pertenece a la finca ingresada")
            if ComponenteSensor.objects.filter(idComponenteSensor=datos[KEY_ID_COMPONENTE_SENSOR]).__len__() == 0:
                raise ValueError(ERROR_COMPONENTE_SENSOR_NO_EXISTENTE, "No existe componente sensor con ese id")
            componente = ComponenteSensor.objects.get(idComponenteSensor=datos[KEY_ID_COMPONENTE_SENSOR])
            ultimo_historico = componente.historico_estado_componente_sensor_list.get(
                fechaFinEstadoComponenteSensor__isnull=True)
            ultimo_historico.fechaFinEstadoComponenteSensor = datetime.now(pytz.utc)
            ultimo_historico.save()
            estado_deshabilitado = EstadoComponenteSensor.objects.get(nombreEstado=ESTADO_DESHABILITADO)
            historico_nuevo = HistoricoEstadoComponenteSensor(componenteSensor=componente,
                                                              estadoComponenteSensor=estado_deshabilitado,
                                                              fechaInicioEstadoComponenteSensor=datetime.now(pytz.utc))
            asignaciones_actuales = AsignacionSensorComponente.objects.filter(componenteSensor=componente,
                                                                              fechaBaja__isnull=True)
            for asignacion in asignaciones_actuales:
                asignacion.fechaBaja = datetime.now(pytz.utc)
                asignacion.save()
                componente.cantidadSensoresAsignados-=1
            if componente.componenteSensorSectorList.filter(habilitado=True).__len__() != 0:
                componente_sensor_sector =componente.componenteSensorSectorList.get(habilitado=True)
                ultimo_historico_componente_sensor_sector = componente_sensor_sector.historicoEstadoComponenteSensorSector.get(fechaBajaComponenteSensorSector__isnull=True)
                estado_componente_sensor_sector_deshabilitado = EstadoComponenteSensorSector.objects.get(nombreEstadoComponenteSensorSector=ESTADO_DESHABILITADO)
                ultimo_historico_componente_sensor_sector.fechaBajaComponenteSensorSector = datetime.now(pytz.utc)
                ultimo_historico_componente_sensor_sector.save()
                nuevo_historico_componente_sensor_sector = HistoricoEstadoComponenteSensorSector(estadoComponenteSensorSector=estado_componente_sensor_sector_deshabilitado,
                                                                                                 fechaAltaComponenteSensorSector=datetime.now(pytz.utc),
                                                                                                 componenteSensorSector=componente_sensor_sector)
                nuevo_historico_componente_sensor_sector.save()
                componente_sensor_sector.habilitado = False
                componente_sensor_sector.save()
            componente.save()
            historico_nuevo.save()
            response.content = armar_response_content(None)
            response.status_code = 200
            return response
        else:
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
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
@manejar_errores()
@permisos_rol_requeridos([PERMISO_PUEDEGESTIONARSENSORES, PERMISO_PUEDEASIGNARCOMPONENTESENSOR])
def asignar_sensor_a_componente_sensor(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if (KEY_ID_SENSOR and KEY_ID_COMPONENTE_SENSOR and KEY_ID_FINCA) in datos:
            if  datos[KEY_ID_SENSOR] == '' or datos[KEY_ID_COMPONENTE_SENSOR] == '' \
                    or datos[KEY_ID_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if Finca.objects.filter(idFinca=datos[KEY_ID_FINCA]).__len__() != 1:
                raise ValueError(ERROR_FINCA_NO_ENCONTRADA, "No existe la finca ingresada")
            finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
            if ComponenteSensor.objects.filter(idComponenteSensor=datos[KEY_ID_COMPONENTE_SENSOR], finca=finca).__len__() == 0:
                raise ValueError(ERROR_COMPONENTE_SENSOR_NO_PERTENECE_A_FINCA, "El componente no pertenece a la finca ingresada")
            componente = ComponenteSensor.objects.get(idComponenteSensor=datos[KEY_ID_COMPONENTE_SENSOR])
            estado_habilitado = EstadoComponenteSensor.objects.get(nombreEstado=ESTADO_HABILITADO)
            if componente.historico_estado_componente_sensor_list.filter(fechaFinEstadoComponenteSensor__isnull=True,
                                                                         estadoComponenteSensor=estado_habilitado).__len__() == 0:
                raise ValueError(ERROR_COMPONENTE_SENSOR_NO_HABILITADO, "El componente no esta habilitado")
            if Sensor.objects.filter(idSensor=datos[KEY_ID_SENSOR], finca=finca).__len__() == 0:
                raise ValueError(ERROR_SENSOR_NO_PERTENECE_A_FINCA, "El sensor no pertenece a la finca ingresada")
            if Sensor.objects.filter(idSensor=datos[KEY_ID_SENSOR]).__len__() == 0:
                raise ValueError(ERROR_SENSOR_NO_EXISTENTE, "No existe el sensor con ese id")
            if Sensor.objects.filter(idSensor=datos[KEY_ID_SENSOR], habilitado=True).__len__() == 0:
                raise ValueError(ERROR_SENSOR_NO_HABILITADO, "El sensor esta deshabilitado")
            if ComponenteSensor.objects.filter(idComponenteSensor=datos[KEY_ID_COMPONENTE_SENSOR]).__len__() == 0:
                raise ValueError(ERROR_COMPONENTE_SENSOR_NO_EXISTENTE, "No existe componente sensor con ese id")
            sensor = Sensor.objects.get(idSensor=datos[KEY_ID_SENSOR])
            if AsignacionSensorComponente.objects.filter(sensor=sensor, fechaBaja__isnull=True).__len__() != 0:
                raise ValueError(ERROR_SENSOR_YA_ASIGNADO, "El sensor ya esta asignado a otro componente")
            if componente.cantidadSensoresAsignados == componente.cantidadMaximaSensores:
                raise ValueError(ERROR_COMPONENTE_NO_ACEPTA_MAS_SENSORES, "El componente supero su limite de sensores")
            asignacion_nueva = AsignacionSensorComponente(sensor=sensor, componenteSensor=componente,
                                                          fechaAsignacion=datetime.now(pytz.utc))
            asignacion_nueva.save()
            componente.cantidadSensoresAsignados +=1
            componente.save()
            response.content = armar_response_content(None)
            response.status_code = 200
            return response
        else:
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
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
@manejar_errores()
@permisos_rol_requeridos([PERMISO_PUEDEGESTIONARSENSORES, PERMISO_PUEDEASIGNARCOMPONENTESENSOR])
def desasignar_sensor_de_componente_sensor(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if (KEY_ID_SENSOR and KEY_ID_COMPONENTE_SENSOR and KEY_ID_FINCA) in datos:
            if  datos[KEY_ID_SENSOR] == '' or datos[KEY_ID_COMPONENTE_SENSOR] == '' \
                    or datos[KEY_ID_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if Finca.objects.filter(idFinca=datos[KEY_ID_FINCA]).__len__() != 1:
                raise ValueError(ERROR_FINCA_NO_ENCONTRADA, "No existe la finca ingresada")
            finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
            if ComponenteSensor.objects.filter(idComponenteSensor=datos[KEY_ID_COMPONENTE_SENSOR], finca=finca).__len__() == 0:
                raise ValueError(ERROR_COMPONENTE_SENSOR_NO_PERTENECE_A_FINCA, "El componente no pertenece a la finca ingresada")
            if Sensor.objects.filter(idSensor=datos[KEY_ID_SENSOR], finca=finca).__len__() == 0:
                raise ValueError(ERROR_SENSOR_NO_PERTENECE_A_FINCA, "El sensor no pertenece a la finca ingresada")
            if Sensor.objects.filter(idSensor=datos[KEY_ID_SENSOR]).__len__() == 0:
                raise ValueError(ERROR_SENSOR_NO_EXISTENTE, "No existe el sensor con ese id")
            if Sensor.objects.filter(idSensor=datos[KEY_ID_SENSOR], habilitado=True).__len__() == 0:
                raise ValueError(ERROR_SENSOR_NO_HABILITADO, "El sensor esta deshabilitado")
            if ComponenteSensor.objects.filter(idComponenteSensor=datos[KEY_ID_COMPONENTE_SENSOR]).__len__() == 0:
                raise ValueError(ERROR_COMPONENTE_SENSOR_NO_EXISTENTE, "No existe componente sensor con ese id")
            componente = ComponenteSensor.objects.get(idComponenteSensor=datos[KEY_ID_COMPONENTE_SENSOR])
            sensor = Sensor.objects.get(idSensor=datos[KEY_ID_SENSOR])
            if AsignacionSensorComponente.objects.filter(sensor=sensor, componenteSensor=componente,
                                                         fechaBaja__isnull=True).__len__() == 0:
                raise ValueError(ERROR_SENSOR_NO_ASIGNADO_A_COMPONENTE, "El sensor no esta asignado a este componente")
            else:
                asignacion_actual = AsignacionSensorComponente.objects.get(sensor=sensor, componenteSensor=componente,
                                                         fechaBaja__isnull=True)
                asignacion_actual.fechaBaja = datetime.now(pytz.utc)
                asignacion_actual.save()
                componente.cantidadSensoresAsignados -=1
                componente.save()
                response.content = armar_response_content(None)
                response.status_code = 200
                return response
        else:
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
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
@manejar_errores()
def buscar_sensores_no_asignados(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if (KEY_ID_FINCA) in datos:
            if datos[KEY_ID_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if Finca.objects.filter(idFinca=datos[KEY_ID_FINCA]).__len__() != 1:
                raise ValueError(ERROR_FINCA_NO_ENCONTRADA, "No existe la finca ingresada")
            finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
            lista_sensores = Sensor.objects.filter(finca=finca, habilitado=True)
            lista_sensores_no_asignados = []
            for sensor in lista_sensores:
                if AsignacionSensorComponente.objects.filter(sensor=sensor, fechaBaja__isnull=True).__len__() == 0:
                    lista_sensores_no_asignados.append(sensor)

            response.content = armar_response_list_content(lista_sensores_no_asignados)
            response.status_code = 200
            return response
        else:
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
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
@manejar_errores()
def mostrar_componentes_sensor_finca_habilitados(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if (KEY_ID_FINCA) in datos:
            if datos[KEY_ID_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if Finca.objects.filter(idFinca=datos[KEY_ID_FINCA]).__len__() != 1:
                raise ValueError(ERROR_FINCA_NO_ENCONTRADA, "No existe la finca ingresada")
            finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
            estado_habilitado = EstadoComponenteSensor.objects.get(nombreEstado=ESTADO_HABILITADO)
            lista_componentes_sensores = ComponenteSensor.objects.filter(finca=finca)
            lista_componentes_sensores_habilitados = []
            for componente in lista_componentes_sensores:
                if HistoricoEstadoComponenteSensor.objects.filter(fechaFinEstadoComponenteSensor__isnull=True,
                                                                  componenteSensor=componente,
                                                                  estadoComponenteSensor=estado_habilitado).__len__() == 1:
                    lista_componentes_sensores_habilitados.append(componente)

            response.content = armar_response_list_content(lista_componentes_sensores_habilitados)
            response.status_code = 200
            return response
        else:
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
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
@manejar_errores()
def mostrar_componentes_sensor_finca(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if (KEY_ID_FINCA) in datos:
            if datos[KEY_ID_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if Finca.objects.filter(idFinca=datos[KEY_ID_FINCA]).__len__() != 1:
                raise ValueError(ERROR_FINCA_NO_ENCONTRADA, "No existe la finca ingresada")
            if Finca.objects.filter(idFinca=datos[KEY_ID_FINCA]).__len__() != 1:
                raise ValueError(ERROR_FINCA_NO_ENCONTRADA, "No existe la finca ingresada")
            finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
            lista_componentes_sensores = ComponenteSensor.objects.filter(finca=finca)
            response.content = armar_response_list_content(lista_componentes_sensores)
            response.status_code = 200
            return response
        else:
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
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
@manejar_errores()
def mostrar_componentes_sensor_finca_no_asignados(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if (KEY_ID_FINCA) in datos:
            if datos[KEY_ID_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if Finca.objects.filter(idFinca=datos[KEY_ID_FINCA]).__len__() != 1:
                raise ValueError(ERROR_FINCA_NO_ENCONTRADA, "No existe la finca ingresada")
            if Finca.objects.filter(idFinca=datos[KEY_ID_FINCA]).__len__() != 1:
                raise ValueError(ERROR_FINCA_NO_ENCONTRADA, "No existe la finca ingresada")
            finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
            estado_habilitado = EstadoComponenteSensor.objects.get(nombreEstado=ESTADO_HABILITADO)
            lista_componentes_sensores = ComponenteSensor.objects.filter(finca=finca)
            lista_componentes_sensores_no_asignados = []
            for componente in lista_componentes_sensores:
                if HistoricoEstadoComponenteSensor.objects.filter(fechaFinEstadoComponenteSensor__isnull=True,
                                                                  componenteSensor=componente,
                                                                  estadoComponenteSensor=estado_habilitado).__len__() == 1:
                    if componente.componenteSensorSectorList.filter(habilitado=True).__len__() == 0:
                        lista_componentes_sensores_no_asignados.append(componente)
            response.content = armar_response_list_content(lista_componentes_sensores_no_asignados)
            response.status_code = 200
            return response
        else:
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])
    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")