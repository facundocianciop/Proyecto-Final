# -*- coding: UTF-8 -*-
from django.http import HttpResponse,JsonResponse
from django.template import loader
from django.shortcuts import render
from ..models import *
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from django.db import IntegrityError,transaction
from datetime import datetime
from json import loads,dumps
from django.core.mail import send_mail
from django.core import mail
from supportClases.utilFunctions import *
from .viewsSeguridad import obtenerUsuarioActual
@csrf_exempt
@transaction.atomic()
def crearSector(request):
    response=HttpResponse()
    datos=armarJson(request)
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
            print err.args
            response.content=armarJsonErrores("error","descripcion")
            response.status_code=401
            return response