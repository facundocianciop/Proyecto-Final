# -*- coding: UTF-8 -*-
from django.http import HttpResponse,JsonResponse
from django.template import loader
from django.shortcuts import render
from ..models import Sector,Finca,ProveedorInformacionClimaticaFinca,ProveedorInformacionClimatica,TipoSesion,Sesion,EstadoFinca,HistoricoEstadoFinca,UsuarioFinca,Usuario,Rol,RolUsuarioFinca
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


class DTOFincaRol():
    def __init__(self,nombreFinca,nombreRol):
        self.nombreFinca=nombreFinca
        self.nombreRol=nombreRol
    def as_json(self):
        return dict(
            nombreFinca=self.nombreFinca,
            # idFinca=self.idFinca,
            nombreRol=self.nombreRol)



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

@csrf_exempt
@transaction.atomic()
def obtenerFincasPorUsuario(request):
    response=HttpResponse()
    if request.method=="POST":
        datos=armarJson(request)
        usuario=Usuario.objects.get(OIDUsuario=datos['OIDUsuario'])
        print "HOLA"
        lista_DTOFincaRol=[]
        for usuarioFinca in usuario.usuarioFincaList.all():
            finca=usuarioFinca.finca
            ultimo_historico=HistoricoEstadoFinca.objects.get(finca=finca,fechaFinEstadoFinca__isnull=True)
            if ultimo_historico.estadoFinca.nombreEstadoFinca=="Habilitada":
                rol_usuario_finca=RolUsuarioFinca.objects.get(usuarioFinca=usuarioFinca,fechaBajaUsuarioFinca__isnull=True)
                nombre_rol=rol_usuario_finca.rol.nombreRol
                lista_DTOFincaRol.append(DTOFincaRol(nombreFinca=usuarioFinca.finca.nombre,nombreRol=nombre_rol))
        lista_DTOFincaRol_json= [DTO_finca_rol.as_json() for DTO_finca_rol in lista_DTOFincaRol]
        response.status_code=200
        response.content=dumps(lista_DTOFincaRol_json)
        response.content_type="application/json"
        return response
    else:
        return HttpResponse(False)


@csrf_exempt
@transaction.atomic()
def crearFinca(request):
    response = HttpResponse()
    if request.method == "POST":
        datos = armarJson(request)
        if Finca.objects.filter(nombre=datos['nombre'], direccionLegal=datos['direccionLegal']).__len__() == 0:
            finca = Finca(nombre=datos['nombre'], direccionLegal=datos['direccionLegal'], ubicacion=datos['ubicacion'],
                          tamanio=datos['tamanio'])
            finca.save()
            response=HttpResponse(dumps(finca.as_json()),content_type="application/json")
            response.status_code=200
            return response
        else:
            response.status_code=400
            return response
    else:
        return HttpResponse(False)

@csrf_exempt
@transaction.atomic()
def buscarProveedoresInformacion(request):
    response=HttpResponse()
    if request.method=="GET":

        proveedores=ProveedorInformacionClimatica.objects.filter(habilitado=True)
        proveedoresJson=[proveedor.as_json() for proveedor in proveedores]
        #proveedoresJson[proveedoresJson.__len__()-1]=finca.OIDFinca
        response= HttpResponse(dumps(proveedoresJson),content_type="application/json")
        response.status_code=200
        return response
    else:
        return HttpResponse(False)
@transaction.atomic()
@csrf_exempt
def elegirProveedorInformacion(request):
    response=HttpResponse()
    print "HOLA"
    if request.method=="POST":
        datos=armarJson(request)
        if ProveedorInformacionClimatica.objects.filter(nombreProveedor=datos['nombreProveedor']).__len__()==1:
            try:
                proveedorSeleccionado=ProveedorInformacionClimatica.objects.get(nombreProveedor=datos['nombreProveedor'])
                fincaCreada=Finca.objects.get(OIDFinca=datos["OIDFinca"])
                print "Encontre la finca"
                proveedorInformacionClimaticaFinca=ProveedorInformacionClimaticaFinca(proveedorInformacionClimatica=proveedorSeleccionado,finca=fincaCreada)
                proveedorInformacionClimaticaFinca.fechaAltaProveedorInfoClimaticaFinca=datetime.now()
                proveedorInformacionClimaticaFinca.save()
                print "Cree el proveedorInfoClima"
                estadoFinca=EstadoFinca.objects.get(nombreEstadoFinca="Pendiente de Aprobacion")
                print "encontre el estado"

                historicoCreado=HistoricoEstadoFinca(fechaInicioEstadoFinca=datetime.now(),estadoFinca=estadoFinca)
                historicoCreado.finca=fincaCreada
                historicoCreado.save()
                print historicoCreado.fechaInicioEstadoFinca
                fincaCreada.historicoEstadoFincaList.add(historicoCreado)

                print fincaCreada.historicoEstadoFincaList

                usuarioActual=Usuario.objects.get(OIDUsuario=datos['OIDUsuario'])
                print "Encontre al usuario" #DEBERIA BUSCAR EL USUARIO PERTENECIENTE A LA COOKIE QUE TIENE LA SESION
                usuarioFinca=UsuarioFinca(usuario=usuarioActual,finca=fincaCreada)
                usuarioFinca.fechaAltaUsuarioFinca = datetime.now()
                usuarioFinca.save()
                print "joya"

                print "por guardar finca"
                fincaCreada.save()
                # print "Se guardo bien la finca"
                #
                # rolEncargado=Rol.objects.get(nombreRol="Encargado")
                # rol_usuario_finca=RolUsuarioFinca()
                # rol_usuario_finca.fechaAltaUsuarioFinca=datetime.now()
                # rol_usuario_finca.rol=rolEncargado
                # rol_usuario_finca.save()
                # usuarioFinca.rolUsuarioFincaList.add( rol_usuario_finca)
                #
                # usuarioFinca.save()
                response.status_code=200
                return response
            except IntegrityError as e:
                response.status_code=401
                print "error de integridad"
                return response
@csrf_exempt
@transaction.atomic()
def obtenerFincasEstadoPendiente(request):
    response=HttpResponse()
    if request.method=="GET":
        estado_pendiente=EstadoFinca.objects.get(nombreEstadoFinca="Pendiente de aprobacion")
        historicos_pendientes=HistoricoEstadoFinca.objects.filter(estadoFinca=estado_pendiente)
        fincas_pendientes=[]
        for historico in historicos_pendientes:
            fincas_pendientes.append(historico.finca)
        fincas_json=[finca.as_json() for finca in fincas_pendientes]
        response = HttpResponse(dumps(fincas_json), content_type="application/json")
        response.status_code = 200
        return response
    else:
        return HttpResponse(False)

@csrf_exempt
@transaction.atomic()
def aprobarFinca(request):
    response=HttpResponse()
    datos = armarJson(request)
    if request.method=="POST":
        if Finca.objects.filter(OIDFinca=datos['OIDFinca']).__len__() == 1:
            try:
                finca_por_aprobar=Finca.objects.get(OIDFinca=datos['OIDFinca'])

                estado_habilitado=EstadoFinca.objects.get(nombreEstadoFinca="Habilitada")
                historico_viejo=HistoricoEstadoFinca.objects.get(estadoFinca="Pendiente de Aprobacion",finca=finca_por_aprobar)
                historico_viejo.fechaFinEstadoFinca=datetime.now()
                historico_viejo.save()
                historico_nuevo=HistoricoEstadoFinca(estadoFinca=estado_habilitado,finca=finca_por_aprobar,fechaInicioEstadoFinca=datetime.now())
                finca_por_aprobar.historicoEstadoFincaList.add(historico_nuevo,bulk=False)
                finca_por_aprobar.save()
                usuario_finca=UsuarioFinca.objects.get(finca=finca_por_aprobar)
                rolEncargado = Rol.objects.get(nombreRol="Encargado")
                rol_usuario_finca = RolUsuarioFinca()
                rol_usuario_finca.fechaAltaUsuarioFinca = datetime.now()
                rol_usuario_finca.rol = rolEncargado
                rol_usuario_finca.save()
                usuario_finca.rolUsuarioFincaList.add(rol_usuario_finca)

                # usuario_finca.save()
                # with mail.get_connection() as connection:
                #     mail.EmailMessage('SmartFarming: Estado de Aprobación de su finca','Su finca ha sido aprobada, y usted ya dispone del rol de Encargado',from1='facundocianciop',
                #                       to1='facundocianciop',connection=connection).send()
                    #FALTA MANDAR EL MAIL, CONFIGURAR LA CONTRASEÑA Y EL PUERTO
                response.status_code=200
                return response
            except IntegrityError as e:
                response.status_code = 401
                print "error de integridad"
                return response


@csrf_exempt
@transaction.atomic()
def noAprobarFinca(request):
    response=HttpResponse()
    datos = armarJson(request)
    if request.method=="POST":
        if Finca.objects.filter(OIDFinca=datos['OIDFinca']).__len__() == 1:
            try:
                finca_por_aprobar=Finca.objects.get(OIDFinca=datos['OIDFinca'])
                estado_no_aprobada=EstadoFinca.objects.get(nombreEstadoFinca="No aprobada")
                historico_viejo = HistoricoEstadoFinca.objects.get(estadoFinca="Pendiente de Aprobacion",
                                                                   finca=finca_por_aprobar)
                historico_viejo.fechaFinEstadoFinca = datetime.now()
                historico_viejo.save()
                historico_nuevo=HistoricoEstadoFinca(estadoFinca=estado_no_aprobada,finca=finca_por_aprobar,fechaInicioEstadoFinca=datetime.now())
                finca_por_aprobar.historicoEstadoFincaList.add(historico_nuevo)
                finca_por_aprobar.save()
                usuario_finca=UsuarioFinca.objects.get(finca=finca_por_aprobar)
                # with mail.get_connection() as connection:
                #     mail.EmailMessage('SmartFarming: Estado de Aprobación de su finca',body=datos['mail'],from1='facundocianciop',
                #                       to1='facundocianciop',connection=connection).send()
                    #FALTA MANDAR EL MAIL, CONFIGURAR LA CONTRASEÑA Y EL PUERTO
                    #ACA PENSE QUE EN CASO DE RECHAZAR LA FINCA QUE EL ADMINISTRADOR ESCRIBIERA UN MENSAJE DICIENDO POR QUÉ LA RECHAZÓ

                response.status_code=200
                return response(True)
            except IntegrityError as e:
                response.status_code = 401
                print "error de integridad"
                return response

@csrf_exempt
@transaction.atomic()
def modificarFinca(request):
    response=HttpResponse()
    datos = armarJson(request)
    if request.method=="POST":
        if Finca.objects.filter(OIDFinca=datos['OIDFinca']).__len__() == 1:
            try:
                finca_a_modificar=Finca.objects.get(OIDFinca=datos['OIDFinca'])
                finca_encontrada=Finca.objects.get(nombre=datos['nombreFinca'])
                if (finca_encontrada is Finca.objects.get(nombre=datos['nombreFinca'])):
                    print Finca.objects.get(nombre=datos['nombreFinca']).OIDFinca
                    print datos['OIDFinca']
                    print("Ya existe una finca con ese nombre")
                    raise ValueError("Ya existe una finca con ese nombre")
                finca_a_modificar.nombre=datos['nombreFinca']
                finca_a_modificar.ubicacion=datos['ubicacion']
                finca_a_modificar.tamanio=datos['tamanio']
                finca_a_modificar.direccionLegal=datos['direccionLegal']
                finca_a_modificar.logoFinca=datos['logo']
                historico_actual=HistoricoEstadoFinca.objects.get(finca=finca_a_modificar,fechaFinEstadoFinca__isnull=True)
                if historico_actual.estadoFinca.nombreEstadoFinca!=datos['nombreEstado']:
                    print "El estado es distinto al anterior"
                    estado__nuevo=EstadoFinca.objects.get(nombreEstadoFinca=datos['nombreEstado'])
                    historico_actual.fechaFinEstadoFinca=datetime.now()
                    historico_actual.save()
                    historico_nuevo=HistoricoEstadoFinca(fechaInicioEstadoFinca=datetime.now(),finca=finca_a_modificar,estadoFinca=estado__nuevo)
                    historico_nuevo.save()
                finca_a_modificar.save()
                response.status_code=200
                return response
            except (IntegrityError,ValueError) as err:
                response.status_code = 401
                print (err.args)
                response.content=err.args
                return response

@csrf_exempt
@transaction.atomic()
def mostrarFincas(request):
    response=HttpResponse()
    datos = armarJson(request)
    if request.method=="POST":


            try:
                usuario = Usuario.objects.get(OIDUsuario=datos['OIDUsuario'])
                usuario_finca_lista=usuario.usuarioFincaList.all()
                fincas_encargado=[]
                for usuario_finca in usuario_finca_lista:
                    rol=RolUsuarioFinca.objects.get(usuarioFinca=usuario_finca,fechaBajaUsuarioFinca__isnull=True).rol
                    if rol.nombreRol=="Encargado":
                        fincas_encargado.append(usuario_finca.finca)
                fincas_json=[finca.as_json() for finca in fincas_encargado]
                response.content=dumps(fincas_json)
                response.content_type="application/json"
                response.status_code=200
                return response

            except (IntegrityError,ValueError) as err:
                response.status_code = 401
                print (err.args)
                response.content=err.args
                return response




