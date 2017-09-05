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

def armarJson(request):
    received_json_data = str(request.body)
    datos = loads(received_json_data)
    return datos

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
                #fincaCreada.historicoEstadoFincaList.add(historicoCreado)

                print "TODO BIEN"

                usuarioActual=Usuario.objects.get(OIDUsuario=datos['OIDUsuario'])
                print "Encontre al usuario" #DEBERIA BUSCAR EL USUARIO PERTENECIENTE A LA COOKIE QUE TIENE LA SESION
                usuarioFinca=UsuarioFinca(usuario=usuarioActual,finca=fincaCreada)
                print "joya"
                usuarioFinca.fechaAltaUsuarioFinca=datetime.now()
                fincaCreada.save()
                "Se guardo bien la finca"
                proveedorInformacionClimaticaFinca.save()
                "Se guardo el proveedor bien"
                rolEncargado=Rol.objects.get(nombreRol="Encargado")
                rolUsuarioFinca=RolUsuarioFinca(fechaAltaRolUsuarioFinca=datetime.now(),rol=rolEncargado)
                rolUsuarioFinca.save()
                usuarioFinca.rolUsuarioFincaList.add(rolUsuarioFinca)
                usuarioFinca.save()
                response.status_code=200
                return response
            except IntegrityError as e:
                response.status_code=404
                print "error de integridad"
                return response


