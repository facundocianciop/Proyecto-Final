# -*- coding: UTF-8 -*-
from django.http import HttpResponse,JsonResponse
from django.template import loader
from django.shortcuts import render
from ..models import Sector,Finca,ProveedorInformacionClimaticaFinca,ProveedorInformacionClimatica,TipoSesion,Sesion,EstadoFinca,HistoricoEstadoFinca,UsuarioFinca,Usuario
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from django.db import IntegrityError
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
def crearFinca(request):
    response=HttpResponse()
    if request.method=="POST":
        datos=armarJson(request)
        if Finca.objects.filter(nombre=datos['nombre'],direccionLegal=datos['direccionLegal']).__len__()==0:
            finca=Finca(nombre=datos['nombre'],direccionLegal=datos['direccionLegal'],ubicacion=datos['ubicacion'],tamanio=datos['tamanio'])
            finca.save()
            #global fincaCreada=finca.OIDFinca
            print "HOLA"
            proveedores=ProveedorInformacionClimatica.objects.filter(habilitado=True)
            proveedoresJson=[proveedor.as_json() for proveedor in proveedores]
            response= HttpResponse(dumps(proveedoresJson),content_type="application/json")
            response.status_code=200
            return response
        else:
            response.status_code=404
            return response
    else:
        return HttpResponse(False)
@csrf_exempt
def elegirProveedorInformacion(request):
    response=HttpResponse()
    if request.method=="POST":
        datos=armarJson(request)
        if ProveedorInformacionClimatica.objects.filter(nombreProveedor=datos['nombreProveedor']).__len__()==1:
            proveedorSeleccionado=ProveedorInformacionClimatica.objects.get(nombreProveedor=datos['nombreProveedor'])
            fincaCreada=Finca.objects.get(OIDFinca=datos["OIDfincaCreada"])
            proveedorInformacionClimaticaFinca=ProveedorInformacionClimaticaFinca(proveedorInformacionClimatica=proveedorSeleccionado,finca=fincaCreada)
            estadoFinca=EstadoFinca.objects.get(nombreEstadoFinca="Pendiente")
            historicoCreado=HistoricoEstadoFinca(fechaInicioEstadoFinca=datetime.now(),estado_finca=estadoFinca)
            historicoCreado.save()
            fincaCreada.historicoEstadoFincaList.add(historicoCreado)
            #usuarioActual=DEBERIA BUSCAR EL USUARIO PERTENECIENTE A LA COOKIE QUE TIENE LA SESION
           # usuarioFinca=UsuarioFinca(usuario=usuarioActual,finca=fincaCreada)
            #usuarioFinca.fechaAltaUsuarioFinca=datetime.now()
            fincaCreada.save()
            proveedorInformacionClimaticaFinca.save()
           # usuarioFinca.save()
            return HttpResponse(True)


