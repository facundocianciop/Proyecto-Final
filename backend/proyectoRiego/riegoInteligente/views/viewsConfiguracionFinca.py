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



