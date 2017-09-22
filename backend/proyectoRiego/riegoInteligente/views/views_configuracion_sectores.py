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
        if Sector.objects.filter(numeroSector=datos[KEY_NUMERO_SECTOR]) or Sector.objects.filter(nombreSector=datos[KEY_NOMBRE_SECTOR]):
            raise ValueError("Ya existe un sector con ese número o nombre")
        sector_nuevo = Sector(numeroSector=datos[KEY_NUMERO_SECTOR], nombreSector=datos[KEY_NOMBRE_SECTOR],
                              descripcionSector=datos[KEY_DESCRIPCION_SECTOR], superficie=datos[KEY_SUPERFICIE_SECTOR],
                              finca=finca_actual
                              )
        sector_nuevo.save()
        estado_habilitado = EstadoSector.objects.get(nombreEstadoSector=ESTADO_HABILITADO)
        historico_nuevo = HistoricoEstadoSector(estado_sector=estado_habilitado, sector=sector_nuevo,
                                                fechaInicioEstadoSector=datetime.now())
        historico_nuevo.save()
        finca_actual.save()
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
        response.content = 200
        return response
    except ValueError as err:
        return build_bad_request_error(response,err.args[0], err.args[1])
    except (IntegrityError, TypeError, KeyError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")