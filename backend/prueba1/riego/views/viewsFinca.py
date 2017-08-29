# -*- coding: UTF-8 -*-
from django.http import HttpResponse,JsonResponse
from django.template import loader
from django.shortcuts import render
from riego.models import Sector,Finca,TipoSesion,Sesion
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from django.db import IntegrityError
from datetime import datetime
from json import loads,dumps


def index(request):
    fincas=Finca.objects.all()
    cantidadFincas=fincas.count()
    textoSalida=""
    s={}
    for finca in fincas:

        textoSalida+= "El nombre de la finca  es %s \n'"%finca.nombre
    fincasJson=[finca.as_json()for finca in fincas]#HAY Q DEFINIR EN CADA CLASE LA FUNCION as_json(), que retorna un diccionario del objeto
   # return HttpResponse(dumps(finca.as_json()), content_type="application/json") PARA UN SOLO OBJETO
    return HttpResponse(dumps(fincasJson), content_type="application/json")#PARA MAS DE UNO,
def sector(request):
    s= Sector.objects.get(numeroSector=1)
    #json= serialize('json', Sector.objects.all(), cls=DjangoJSONEncoder) CON ESTO RETORNA TODOS LOS OBJETOS SECTOR
    json=serialize('json',[s])#ASI ES PARA UN SOLO OBJETO
    return JsonResponse(json,safe=False)