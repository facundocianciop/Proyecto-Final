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
def mostrarMecanismosRiegoFinca(request):
    response=HttpResponse()
    datos=armarJson(request)
    if request.method=='POST':
        try:
            finca_actual=Finca.objects.get(OIDFinca=datos['OIDFinca'])
            estado_mecanismo_habilitado=EstadoMecanismoRiegoFinca.objects.get(nombreEstadoMecanismoRiegoFinca="Habilitado")
            mecanismo_riego_finca_list=MecanismoRiegoFinca(finca=finca_actual)
            mecanismos_habilitados_list=[]
            for mecanismo in mecanismo_riego_finca_list:
               if (HistoricoMecanismoRiegoFinca.objects.filter(mecanismo_riego_finca=mecanismo,fechaFinEstadoMecanismoRiegoFinca__isnull=True,
                                                            estado_mecanismo_riego_finca=estado_mecanismo_habilitado)).__len__()==1:
                   mecanismos_habilitados_list.append(mecanismo)
            mecanismos_habilitados_list_json=[mecanismo_habilitado.as_json() for mecanismo_habilitado in mecanismos_habilitados_list]
            response.content=dumps(mecanismos_habilitados_list_json)
            response.status_code=200
            return response
        except (IntegrityError,ValueError) as err:
            print err.args
            response.content=err.args
            response.status_code=401
            return response
@csrf_exempt
@transaction.atomic()
def mostrarMecanismosNuevos(request):
    response=HttpResponse()
    datos=armarJson(request)
    if request.method=='POST':
        try:
            finca_actual = Finca.objects.get(OIDFinca=datos['OIDFinca'])
            mecanismo_riego_finca_list=MecanismoRiegoFinca(finca=finca_actual)
            tipo_mecanismo_existente_list=[]
            for mecanismo_riego in mecanismo_riego_finca_list:
                tipo_mecanismo_existente_list.append(mecanismo_riego_finca_list.tipoMecanismoRiego)
            tipo_mecanismo_riego_list=TipoMecanismoRiego(habilitado=True)
            tipo_mecanismo_riego_nuevo_list=[]
            for tipo_mecanismo in tipo_mecanismo_riego_list:
                if tipo_mecanismo_existente_list.__contains__(tipo_mecanismo)==False:
                    tipo_mecanismo_riego_nuevo_list.append(tipo_mecanismo)
            tipo_mecanismo_nuevo_list_json=[tipo_mecanismo_nuevo.asjson() for tipo_mecanismo_nuevo in tipo_mecanismo_riego_nuevo_list]
            response.content=dumps(tipo_mecanismo_nuevo_list_json,content_type="application/json")
            response.status_code=200
            return response
        except IntegrityError as err:
            print err.args
            response.status_code=401
            return response

""""
@csrf_exempt
@transaction.atomic()
def agregarMecanismoRiegoFinca(request):
    response=HttpResponse()
    datos=armarJson(request)
    if request.method=='PUT':
"""

