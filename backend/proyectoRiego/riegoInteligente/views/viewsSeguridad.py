# -*- coding: UTF-8 -*-
import django
from django.http import HttpResponse, JsonResponse, response
from django.template import loader
from django.shortcuts import render
from ..models import Sector,Finca,TipoSesion,Sesion,EstadoUsuario,HistoricoEstadoUsuario
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from django.db import IntegrityError
from datetime import datetime
from json import loads,dumps
from ast import literal_eval
from datetime import datetime
from django.db import transaction
def armarJson(request):
    received_json_data = str(request.body)
    datos = loads(received_json_data)
    return datos

@csrf_exempt
@transaction.atomic()
def registrarse(request):
    # usuario = request.POST.get("user")
    # contrasenia = request.POST.get("password")
    datos=armarJson(request)

    try:
        print(datos['usuario'],datos['contrasenia'],datos['email'])
        user = User.objects.create_user(username=datos['usuario'],password=datos['contrasenia'])
        #Luego de esto ya está guardado aunque no le haga save
        user.usuario.email=datos['email']
        estado=EstadoUsuario.objects.get(nombreEstadoUsuario="Activado")#
        historico=HistoricoEstadoUsuario(fechaInicioEstadoUsuario=datetime.now(),estadoUsuario=estado)
        print(historico.fechaInicioEstadoUsuario)
        print estado.nombreEstadoUsuario
        historico.save()
        user.usuario.historicoEstadoUsuarioList.add(historico)
        user.save()#CUANDO LO MODIFICO SI NECESITO EL SAVEs
        return HttpResponse(request)
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
@csrf_exempt
@transaction.atomic()
def iniciarSesion(request):
    response=HttpResponse()
    if request.method=='POST':
        datos=armarJson(request)
        usuario = datos["usuario"]
        contrasenia = datos["contrasenia"]

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
        try:
            user=authenticate(username=usuario,password=contrasenia)
            if user is not None:
                login(request,user)
                print user.username
                sesion=Sesion(fechaYHoraInicio=datetime.now(),horaUltimoAcceso=datetime.now())
                tipoSesion=TipoSesion.objects.get(nombre="Celular")
                sesion.tipoSesion=tipoSesion
                sesion.save()
                user.usuario.sesionList.add(sesion)

                user.save()
                response.set_cookie("idsesion",sesion.idSesion,max_age=3600)
                response.status_code=200
                autenticado=True

            else:
                autenticado=False
                response.status_code = 404
            return response
        except IntegrityError as e:
            print "Error al guardar"
            print e.message
            response.status_code = 404
            return response
        else:
            return response
@csrf_exempt
def finalizarSesion(request):
    if request.method=='POST':
        try:

            sesion = Sesion.objects.get(idSesion=request.COOKIES.get('idSesion'))
            #BUSCO LA SESION CON ESE ID EN LA BASE DE DATOS
            # Si se encontro la sesion se finaliza y se devuelve que la sesion
            # finalizo correctamente

            sesion.fechaYHoraFin = datetime.now()
            sesion.save()
            return HttpResponse(True)

        except Sesion.DoesNotExist:
            # Si no se encontro la sesion se devuelve nada ya que la sesion es
            # incorrecta o ya finalizo
            print('No se encontro la sesion')
            return HttpResponse(False)
    else:
        print "No entró ni al post"
        return HttpResponse(False)
