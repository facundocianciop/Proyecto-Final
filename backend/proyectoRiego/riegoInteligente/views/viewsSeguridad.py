# -*- coding: UTF-8 -*-
import django
from django.http import HttpResponse, JsonResponse, response
from ..models import TipoSesion,Sesion,EstadoUsuario,HistoricoEstadoUsuario,Usuario
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from django.db import IntegrityError
from datetime import datetime
from django.db import transaction
from supportClases.utilFunctions import *
from supportClases.authentication import autorizar
from json import loads,dumps
import uuid


@csrf_exempt
@transaction.atomic()
def registrarse(request):
    # usuario = request.POST.get("user")
    # contrasenia = request.POST.get("password")
    datos=armarJson(request)
    response=HttpResponse()
    if request.method == 'PUT':
        try:
            print(datos['usuario'],datos['contrasenia'],datos['email'])
            if User.objects.filter(username=datos['usuario']).__len__()==1:
                raise ValueError ("Ya existe un usuario con ese nombre, por favor ingrese otro")
            user = User.objects.create_user(username=datos['usuario'],password=datos['contrasenia'])
            #Luego de esto ya está guardado aunque no le haga save
            user.usuario.email=datos['email']
            estado=EstadoUsuario.objects.get(nombreEstadoUsuario="Activado")
            historico=HistoricoEstadoUsuario(fechaInicioEstadoUsuario=datetime.now(),estadoUsuario=estado)
            print(historico.fechaInicioEstadoUsuario)
            print estado.nombreEstadoUsuario
            historico.save()
            user.usuario.historicoEstadoUsuarioList.add(historico)
            user.save()#CUANDO LO MODIFICO SI NECESITO EL SAVEs
            usuario_json = user.usuario.as_json()
            response.content = dumps(usuario_json)
            response.status_code=200
            return response
        except (IntegrityError,ValueError) as err:
            print err.args
            response.content=err.args
            response.status_code=401
            return response
            #   print(received_json_data)
            #   try:
            # user = User.objects.create_user(username=usuario,password=contrasenia)  # Luego de esto ya está guardado aunque no le haga save
            #     user.save()#CUANDO LO MODIFICO SI NECESITO EL SAVE
            # return HttpResponse(user.password)
@csrf_exempt
@transaction.atomic()
def mostrarUsuario(request):
    response=HttpResponse()
    if request.method == 'GET':
        usuario_actual=obtenerUsuarioActual(request)
        response.content=dumps(usuario_actual.as_json())
        response.status_code=200
        return response

@csrf_exempt
def obtenerUsuarioActual(request):
    try:
        if Sesion.objects.filter(idSesion=request.COOKIES['idsesion']).__len__==0:
            raise ValueError("No hay sesion actual")
        sesion_actual=Sesion.objects.get(idSesion=request.COOKIES['idsesion'])
        usuario_actual=sesion_actual.usuario
        return usuario_actual
    except ValueError as err:
        print err.args


@csrf_exempt
@transaction.atomic()
def iniciarSesion(request):
    response=HttpResponse()
    datos = armarJson(request)
    if request.method=='POST':
        try:

            usuario = datos["usuario"]
            contrasenia = datos["contrasenia"]

            print (usuario,contrasenia)
            usuario_inicial= authenticate(username=usuario,password=contrasenia)
            print usuario_inicial.username
            if usuario_inicial is not None:
                if Sesion.objects.filter(usuario=usuario_inicial.usuario,fechaYHoraFin__isnull=True):
                    raise ValueError("Ya tiene una sesión iniciada")
                login(request, usuario_inicial)
                sesion = Sesion(fechaYHoraInicio=datetime.now(), horaUltimoAcceso=datetime.now())
                tipoSesion = TipoSesion.objects.get(nombre=datos["tipoDispositivo"])
                sesion.tipoSesion = tipoSesion
                sesion.idSesion=uuid.uuid4()
                sesion.save()
                usuario_inicial.usuario.sesionList.add(sesion)
                usuario_inicial.save()
                response.set_cookie("idsesion", sesion.idSesion, max_age=3600)
                response.set_cookie(key="idsesion",value=sesion.idSesion)  # PODEMOS GENERAR NUESTRAS PROPIAAS COOKIES
                usuario_json=usuario_inicial.usuario.as_json()
                response.content=dumps(usuario_json)
                response.status_code = 200
                return response
            else:
                raise ValueError("El usuario o contraseña ingresado son incorrectos")
        except ValueError as err:
            print err.args
            response.content=err.args
            response.status_code=401
            return response



@csrf_exempt
@transaction.atomic()
def recuperarCuenta(request):
    # usuario = request.POST.get("user")
    # contrasenia = request.POST.get("password")
    datos=armarJson(request)
    response=HttpResponse()

    try:

        usuario = Usuario.objects.get(email=datos['email'])
        sesiones_abiertas=Sesion.objects.get(usuario=usuario,fechaYHoraFin__isnull=True)
        for sesion in sesiones_abiertas:
            sesion.fechaYHoraFin=datetime.now()
        contrasenia_aleatoria=id_generator()
        usuario.user.set_password(contrasenia_aleatoria)
        #with mail.get_connection() as connection:
        # mail.EmailMessage('SmartFarming: Recuperacion de cueta ',body="Su nueva contraseña es %s"%contrasenia_aleatoria,from1='facundocianciop',
        #                       to1='facundocianciop',connection=connection).send()
        # FALTA MANDAR EL MAIL, CONFIGURAR LA CONTRASEÑA Y EL PUERTO
        # ACA PENSE QUE EN CASO DE RECHAZAR LA FINCA QUE EL ADMINISTRADOR ESCRIBIERA UN MENSAJE DICIENDO POR QUÉ LA RECHAZÓ



        response.status_code=200
        return response
    except IntegrityError as e:
        response.status_code=401
        descripcion_error="No se encontró usuario con el mail ingresado"
        response.content=descripcion_error
        return response
        #   print(received_json_data)
        #   try:
        # user = User.objects.create_user(username=usuario,password=contrasenia)  # Luego de esto ya está guardado aunque no le haga save
        #     user.save()#CUANDO LO MODIFICO SI NECESITO EL SAVE
        # return HttpResponse(user.password)



@transaction.atomic()
@csrf_exempt
def cambiarContrasenia(request):
    response=HttpResponse()
    datos = armarJson(request)
    if request.method=='POST':
        # if autenticarse(request):
        #     u=User.objects.get(username='Facundo')#BUSCO AL USUARIO CON ESE NOMBRE DE USUARIO

        usuario_a_modificar = obtenerUsuarioActual(request)
        print "JOYA"
        username=usuario_a_modificar.user.get_username()
        contrasenia_vieja=datos["contraseniaVieja"]
        contrasenia_nueva=datos["contraseniaNueva"]
        user=authenticate(username=username,password=contrasenia_vieja)

        if user is not None:
            user.set_password(contrasenia_nueva)
            user.save()
            response.status_code=200
        else:
            response.status_code=401
        return response

        # if (u.check_password('123')):
        #     u.set_password('1234')
        #     u.save()
        #     u = User.objects.get(username='Facundo')  # BUSCO AL USUARIO CON ESE NOMBRE DE USUARIO
        # return HttpResponse(u.check_password('1234'))




@csrf_exempt
@transaction.atomic()
def modificarUsuario(request):
    response=HttpResponse()
    if request.method=='POST':
        try:
            datos=armarJson(request)
            usuario_a_modificar=obtenerUsuarioActual(request)
            usuario_a_modificar.user.username=datos['usuario']
            usuario_a_modificar.user.email = datos['mail']
            usuario_a_modificar.email=datos['mail']

            usuario_a_modificar.nombre = datos['nombre']
            usuario_a_modificar.apellido = datos['apellido']
            if datos['dni']!="":
                usuario_a_modificar.dni=int(datos['dni'])
            if datos['cuit'] != "":
                usuario_a_modificar.cuit=int(datos['cuit'])
            if datos['fechaNacimiento'] != "":
                usuario_a_modificar.fechaNacimiento=datos['fechaNacimiento']
            if datos['imagenUsuario'] != "":
                usuario_a_modificar.imagenUsuario=datos['imagenUsuario']
            if datos['contraseniaNueva']!='':
                if (cambiarContrasenia(request)).status_code == 200:
                    usuario_a_modificar.save()
                    response.status_code=200
                    return response
                else:
                    raise ValueError("Contrasenia Ingresada Incorrecta")

            usuario_a_modificar.user.save()
            usuario_a_modificar.save()
            response.content=dumps(usuario_a_modificar.as_json())
            response.status_code = 200
            return response

        except (IntegrityError,ValueError) as err:
            print err.args
            response.status_code=401
            response.content = err.args
            return response

@csrf_exempt
@transaction.atomic()
def eliminarUsuario(request):
    response=HttpResponse()
    if request.method=='DELETE':
        try:
            datos=armarJson(request)
            usuario_a_desactivar=obtenerUsuarioActual(request)
            ultimo_historico=HistoricoEstadoUsuario.objects.get(usuario=usuario_a_desactivar,fechaFinEstadoUsuario__isnull=True)
            ultimo_historico.fechaFinEstadoUsuario=datetime.now()
            ultimo_historico.save()
            estado_desactivado=EstadoUsuario.objects.get(nombreEstadoUsuario="Desactivado")
            nuevo_historico=HistoricoEstadoUsuario(estadoUsuario=estado_desactivado,fechaInicioEstadoUsuario=datetime.now(),usuario=usuario_a_desactivar)
            nuevo_historico.save()
            usuario_a_desactivar.historicoEstadoUsuarioList.add(nuevo_historico)
            print usuario_a_desactivar.historicoEstadoUsuarioList
            sesion_actual=Sesion.objects.get(usuario=usuario_a_desactivar,fechaYHoraFin__isnull=True,idSesion=request.COOKIES['idsesion'])
            sesion_actual.fechaYHoraFin=datetime.now()
            sesion_actual.save()
            usuario_a_desactivar.save()
            response.content=dumps(usuario_a_desactivar.as_json())
            response.status_code=200
            return response
        except IntegrityError as e:
            descripcion_error="Error al tratar de eliminar"
            response.status_code=401
            response.content = descripcion_error
            return response

"""
def autenticarse(request):
    #CREO QUE ESTE METODO DEBERIA LLAMARSE CADA VEZ QUE SE EJECUTA ALGUN OTRO AL PRINCIPIO, PARA VER SI EL USUARIO SIGUE CON SESION INICIADA
     # PIENSO Q EL AUTENTICARSE DEBERIA BUSCAR LA ULTIMA SESION ACTIVA(O SEA CON FECHA FIN NULA) Y QUE EL ID DE LA COOKIE Q VIENE EN EL REQUEST SEA IGUAL AL ID DE LA SESION
        try:
            user=authenticate(username='prueba',password="1234")
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
"""

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
