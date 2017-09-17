# -*- coding: UTF-8 -*-
from datetime import datetime

from django.http import HttpResponse
from django.db import IntegrityError,transaction

from riegoInteligente.models import *
from supportClases.views_util_functions import *
from supportClases.error_handler import *


@transaction.atomic()
def crearSector(request):
    response=HttpResponse()
    datos=obtener_datos_json(request)
    if request.method=='PUT':
        try:
            finca_actual=Finca.objects.get(OIDFinca=datos['OIDFinca'])
            if Sector.objects.filter(numeroSector=datos['numeroSector']) or Sector.objects.filter(nombreSector=datos['nombreSector']):
                raise ValueError("Ya existe un sector con ese número o nombre")
            sector_nuevo=Sector(numeroSector=datos['numeroSector'],nombreSector=datos['nombreSector'],descripcionSector=datos['descripcionSector'],superficie=datos['superficie'])
            sector_nuevo.save()
            estado_habilitado=EstadoSector.objects.get(OIDEstadoSector="Habilitado")
            historico_nuevo=HistoricoEstadoSector(estado_sector=estado_habilitado,sector=sector_nuevo,fechaInicioEstadoSector=datetime.now())
            historico_nuevo.save()
        except (ValueError,IntegrityError) as err:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, "Datos incorrectos")