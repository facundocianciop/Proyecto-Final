# -*- coding: UTF-8 -*-
import django
from django.http import HttpResponse,JsonResponse
from django.template import loader
from django.shortcuts import render
from ..models import Sector,Finca,TipoSesion,Sesion
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from django.db import IntegrityError
from datetime import datetime
from json import loads,dumps
from ast import literal_eval

@csrf_exempt
def registrarse(request):
    # usuario = request.POST.get("user")
    # contrasenia = request.POST.get("password")

    print 'Raw Data: "%s"' % request.body

    received_json_data=str(request.body)
    cadenaLimpia=received_json_data[14:]
    print "la cadena limpia es %s" %cadenaLimpia
    datos=loads(cadenaLimpia)

    print 'El string es %s' % datos
    print 'El nombre es %s' % datos['usuario']
    try:
        user = User.objects.create_user(username=datos['usuario'],password=datos['contrasenia'])  # Luego de esto ya está guardado aunque no le haga save
        user.save()#CUANDO LO MODIFICO SI NECESITO EL SAVE
        return HttpResponse(user.password)
    except IntegrityError as e:
        return HttpResponse(False)
        #   print(received_json_data)
        #   try:
        # user = User.objects.create_user(username=usuario,password=contrasenia)  # Luego de esto ya está guardado aunque no le haga save
        #     user.save()#CUANDO LO MODIFICO SI NECESITO EL SAVE
        # return HttpResponse(user.password)

@csrf_exempt
def cambioContrasenia(request):
    # if autenticarse(request):
    #     u=User.objects.get(username='Facundo')#BUSCO AL USUARIO CON ESE NOMBRE DE USUARIO
    received_json_data = str(request.body)
    datos=loads(received_json_data)
    usuario=datos["usuario"]
    contraseniaVieja=datos["contraseniaVieja"]
    contraseniaNueva=datos["contraseniaNueva"]
    user=authenticate(username=usuario,password=contraseniaVieja)


    if user is not None:
        user.set_password(contraseniaNueva)
        user.save()
        return HttpResponse(True)
    else:
        return HttpResponse(False)

    # if (u.check_password('123')):
    #     u.set_password('1234')
    #     u.save()
    #     u = User.objects.get(username='Facundo')  # BUSCO AL USUARIO CON ESE NOMBRE DE USUARIO
    # return HttpResponse(u.check_password('1234'))
#@csrf_exempt

def iniciarSesion(request):
    if request.method=='POST':
        usuario=request.POST.get("usuario")
        contrasenia=request.POST.get("contrasenia")
        print (usuario,contrasenia)
        print django.middleware.csrf.get_token(request)
        # u=User.objects.get(username=usuario,password=contrasenia)
        # print (u.username)
        user=authenticate(username=usuario,password=contrasenia)
        if user is not None:
            autenticado=True
        else:
            autenticado=False
        context={'autenticado':autenticado}
        #response=render (request, 'riego/autenticarse.html', context)
        #response.set_cookie(key="csrf_token",value=get_token(request)) #PODEMOS GENERAR NUESTRAS PROPIAAS COOKIES
        #ACA MISMO PODEMOS SETEAR UNA COOKIE CON EL ID DE LA SESION Q GENERAMOS
        print(request.session.session_key)# ESTO ES IMPORTANTE DJANGO CREA SESIONES ESTA CLAVE DEBERIAMOS USARLA PARA CREAR NUESTRA PROPIA CLASES SESION
        return HttpResponse(autenticado)
    else:
        return HttpResponse(False)
def autenticarse(request):
    #CREO QUE ESTE METODO DEBERIA LLAMARSE CADA VEZ QUE SE EJECUTA ALGUN OTRO AL PRINCIPIO, PARA VER SI EL USUARIO SIGUE CON SESION INICIADA
     # PIENSO Q EL AUTENTICARSE DEBERIA BUSCAR LA ULTIMA SESION ACTIVA(O SEA CON FECHA FIN NULA) Y QUE EL ID DE LA COOKIE Q VIENE EN EL REQUEST SEA IGUAL AL ID DE LA SESION

        return HttpResponse(request)
