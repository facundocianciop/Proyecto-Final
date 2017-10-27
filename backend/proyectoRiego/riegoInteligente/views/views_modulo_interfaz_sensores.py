# -*- coding: UTF-8 -*-
from django.db import IntegrityError, DataError, DatabaseError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned

# noinspection PyUnresolvedReferences
from ..models import *

from supportClases.security_util_functions import *  # Se importa para que se ejecuten los handlers de sesion
from supportClases.security_decorators import *
from supportClases.views_util_functions import *
from supportClases.views_constants import *
from supportClases.error_handler import *

import riegoInteligente.tasks


@transaction.atomic()
@metodos_requeridos([METHOD_POST])
@manejar_errores()
def recibir_medicion(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
            if datos == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if (KEY_ID_COMPONENTE_SENSOR in datos) and (KEY_LISTA_MEDICIONES in datos):
                if datos[KEY_ID_COMPONENTE_SENSOR] == '':
                    raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
                if datos[KEY_LISTA_MEDICIONES] == '':
                    raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
                if ComponenteSensor.objects.filter(idComponenteSensor=datos[KEY_ID_COMPONENTE_SENSOR]).__len__() == 0:
                    raise ValueError(ERROR_COMPONENTE_SENSOR_NO_EXISTENTE, "No existe componente sensor con ese id")
                componente_sensor = ComponenteSensor.objects.get(idComponenteSensor=datos[KEY_ID_COMPONENTE_SENSOR])
                estado_habilitado = EstadoComponenteSensor.objects.get(nombreEstado=ESTADO_HABILITADO)
                if componente_sensor.historico_estado_componente_sensor_list.filter(
                    estadoComponenteSensor=estado_habilitado, fechaFinEstadoComponenteSensor__isnull=True).__len__()\
                        == 0:
                    raise ValueError(ERROR_COMPONENTE_SENSOR_NO_HABILITADO,
                                     "El componente sensor no se encuentra habilitado")
                if componente_sensor.componenteSensorSectorList.filter(habilitado=True).__len__() == 0:
                    raise ValueError(ERROR_COMPONENTE_SENSOR_NO_ASIGNADO_A_SECTOR,
                                     "El componente no esta asignado a un sector")
                componente_sensor_sector = componente_sensor.componenteSensorSectorList.get(habilitado=True)
                medicion_cabecera = MedicionCabecera(fechaYHora=datetime.now(pytz.utc),
                                                     componenteSensorSector=componente_sensor_sector)
                medicion_cabecera.save()
                lista_medicion = datos[KEY_LISTA_MEDICIONES]
                i = 1
                for medicion in lista_medicion:
                    id_tipo_medicion = medicion[KEY_ID_TIPO_MEDICION]
                    if TipoMedicion.objects.filter(idTipoMedicion=id_tipo_medicion).__len__() == 0:
                        raise ValueError(ERROR_TIPO_MEDICION_NO_EXISTENTE,
                                         "No se encuentra tipo de medicion con ese id")
                    if TipoMedicion.objects.filter(idTipoMedicion=id_tipo_medicion, habilitado=True).__len__() == 0:
                        raise ValueError(ERROR_TIPO_MEDICION_NO_HABILITADA, "El tipo de medicion no esta habilitado")
                    tipo_medicion = TipoMedicion.objects.get(idTipoMedicion=id_tipo_medicion)
                    valor_medicion = medicion[KEY_VALOR_MEDICION_SENSOR]
                    medicion_detalle = MedicionDetalle(nroRenglon=i, valor=valor_medicion, tipoMedicion=tipo_medicion,
                                                       medicionCabecera=medicion_cabecera)
                    medicion_detalle.save()
                    i += 1

                riegoInteligente.tasks.accion_recepcion_medicion_sensor.delay(
                    oid_sector=componente_sensor_sector.sector.OIDSector,
                    oid_medicion_cabecera=medicion_cabecera.OIDMedicionCabecera
                )

                response.content = armar_response_content(None)
                response.status_code = 200
                return response
            else:
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])
    except (IntegrityError, TypeError, KeyError) as err:
        print err.args
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")
