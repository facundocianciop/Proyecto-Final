# -*- coding: UTF-8 -*-
from datetime import datetime

from django.http import HttpResponse,JsonResponse
from django.core.serializers import serialize
from django.contrib.auth.models import User
from django.db import IntegrityError,transaction

from ..models import Sector,Finca,ProveedorInformacionClimaticaFinca,ProveedorInformacionClimatica,\
    EstadoFinca,HistoricoEstadoFinca,UsuarioFinca,DatosUsuario,Rol,RolUsuarioFinca

from supportClases.security_util_functions import *  # Se importa para que se ejecuten los handlers de sesion
from supportClases.security_decorators import *
from supportClases.views_util_functions import *
from supportClases.views_constants import *
from supportClases.error_handler import *


class DTOFincaRol():
    def __init__(self,nombreFinca,nombreRol):
        self.nombreFinca=nombreFinca
        self.nombreRol=nombreRol
    def as_json(self):
        return dict(
            nombreFinca=self.nombreFinca,
            # idFinca=self.idFinca,
            nombreRol=self.nombreRol)


class DTOUsuarioFinca:
    def __init__(self,OIDUsuarioFinca,usuario,nombreUsuario,apellidoUsuario,email,imagenUsuario,rol):
        self.OID_usuario_finca=OIDUsuarioFinca
        self.usuario=usuario
        self.nombre_usuario=nombreUsuario
        self.apellido_usuario=apellidoUsuario
        self.email=email
        self.imagen_usuario=imagenUsuario
        self.rol=rol
    def as_json(self):
        return dict(
            OIDUsuarioFinca=self.OID_usuario_finca,
            nombreUsuario=self.nombre_usuario,
            apellidoUsuario=self.apellido_usuario,
            email=self.email,
            imagenUsuario=self.imagen_usuario,
            rol=self.rol
        )


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def obtenerFincasPorUsuario(request):
    response=HttpResponse()
    datos = obtener_datos_json(request)
    try:
        usuario=request.user
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
    except ValueError as err:
        print err.args
        response.content=err.args
        response.status_code=401
        return response


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_PUT])
def crearFinca(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if Finca.objects.filter(nombre=datos['nombre'], direccionLegal=datos['direccionLegal']).__len__() == 0:
            finca = Finca(nombre=datos['nombre'], direccionLegal=datos['direccionLegal'], ubicacion=datos['ubicacion'],
                          tamanio=datos['tamanio'])
            finca.save()
            response=HttpResponse(dumps(finca,cls=DjangoJSONEncoder))
            response.status_code=200
            return response
        else:
            raise ValueError("Ya existe una finca con ese nombre")
    except (ValueError,IntegrityError) as err:
        print err.args
        response.content=err.args


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_GET])
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
@login_requerido
@metodos_requeridos([METHOD_POST])
def elegirProveedorInformacion(request):
    response=HttpResponse()
    datos=obtener_datos_json(request)
    if ProveedorInformacionClimatica.objects.filter(nombreProveedor=datos['nombreProveedor']).__len__()==1:
        try:
            proveedorSeleccionado=ProveedorInformacionClimatica.objects.get(nombreProveedor=datos['nombreProveedor'])
            fincaCreada=Finca.objects.get(idFinca=datos["idFinca"])
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

            usuarioActual=obtener_datos_json(request)
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


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_GET])
def obtenerFincasEstadoPendiente(request):
    response=HttpResponse()
    estado_pendiente=EstadoFinca.objects.get(nombreEstadoFinca="Pendiente de aprobacion")
    historicos_pendientes=HistoricoEstadoFinca.objects.filter(estadoFinca=estado_pendiente)
    fincas_pendientes=[]
    for historico in historicos_pendientes:
        fincas_pendientes.append(historico.finca)
    fincas_json=[finca.as_json() for finca in fincas_pendientes]
    response = HttpResponse(dumps(fincas_json), content_type="application/json")
    response.status_code = 200
    return response



@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def aprobarFinca(request):
    response=HttpResponse()
    datos = obtener_datos_json(request)
    if Finca.objects.filter(idFinca=datos['idFinca']).__len__() == 1:
        try:
            finca_por_aprobar=Finca.objects.get(idFinca=datos['idFinca'])

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
            rol_usuario_finca.fechaAltaRolUsuarioFinca = datetime.now()
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


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def noAprobarFinca(request):
    response=HttpResponse()
    datos = obtener_datos_json(request)

    if Finca.objects.filter(idFinca=datos['idFinca']).__len__() == 1:
        try:
            finca_por_aprobar=Finca.objects.get(idFinca=datos['idFinca'])
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


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_GET])
def mostrarFincasEncargado(request):
    response=HttpResponse()
    datos = obtener_datos_json(request)
    try:
        usuario=request.user
        usuario_finca_lista=usuario.usuarioFincaList.all()
        fincas_encargado=[]
        for usuario_finca in usuario_finca_lista:
            rol=RolUsuarioFinca.objects.get(usuarioFinca=usuario_finca,fechaBajaRolUsuarioFinca__isnull=True).rol
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

@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def modificarFinca(request):
    response=HttpResponse()
    datos = obtener_datos_json(request)
    if Finca.objects.filter(idFinca=datos['idFinca']).__len__() == 1:
        try:
            finca_a_modificar=Finca.objects.get(OIDFinca=datos['idFinca'])
            # finca_encontrada=Finca.objects.get(nombre=datos['nombreFinca'])
            # if (finca_encontrada is Finca.objects.get(nombre=datos['nombreFinca'])):
            #     print Finca.objects.get(nombre=datos['nombreFinca']).OIDFinca
            #     print datos['OIDFinca']
            #     print("Ya existe una finca con ese nombre")
            #     raise ValueError("Ya existe una finca con ese nombre")
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
            response=dumps(finca_a_modificar.as_json(),content_type="application/json")
            response.status_code=200
            return response
        except (IntegrityError,ValueError) as err:
            response.status_code = 401
            print (err.args)
            response.content=err.args
            return response


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def buscarStakeholdersFinca(request):
    response=HttpResponse()
    datos=obtener_datos_json(request)
    try:
        finca=Finca.objects.get(idFinca=datos['idFinca'])
        usuarios_finca=UsuarioFinca.objects.filter(finca=finca)
        rol_stakeholder=Rol.objects.get(nombreRol="Stakeholder")
        DTO_usuario_finca_list=[]
        for usuario_finca in usuarios_finca:
            if RolUsuarioFinca.objects.filter(usuarioFinca=usuario_finca,rol=rol_stakeholder,fechaBajaRolUsuarioFinca__isnull=True).__len__()==1:
                DTO_usuario_finca_list.append(DTOUsuarioFinca(OIDUsuarioFinca=usuario_finca.OIDUsuarioFinca,usuario=usuario_finca.usuario.user.username,nombreUsuario=usuario_finca.usuario.user.first_name,
                                                              apellidoUsuario=usuario_finca.usuario.user.last_name,email=usuario_finca.usuario.user.email,
                                                              imagenUsuario=usuario_finca.usuario.imagenUsuario))

                #SI EXISTE SIGNIFICA QUE ES UN USUARIO DE ESA FINCA CON EL ROL STAKEHOLDER Y LO AGREGO A LA LISTA
        DTO_usuario_finca_list_json=[DTO_usuario_finca.as_json() for DTO_usuario_finca in DTO_usuario_finca_list]
        response.content=dumps(DTO_usuario_finca_list_json,content_type="application/json")
        response.status_code=200
        return response
    except (ValueError,IntegrityError) as err:
        print err.args
        response.content=err.args
        response.status_code=401
        return response


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_DELETE])
def eliminarStakeholderFinca(request):
    response=HttpResponse()
    datos=obtener_datos_json(request)
    try:
        usuarios_finca=UsuarioFinca.objects.get(OIDUsuarioFinca=datos['OIDUsuarioFinca'])
        usuarios_finca.fechaBajaUsuarioFinca=datetime.now()
        usuarios_finca.save()
        response.status_code=200
        return response
    except IntegrityError as e:
        print e.args
        response.status_code=401
        return response


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_GET])
def buscarUsuarios(request):
    response=HttpResponse()
    try:
        usuarios_todos=DatosUsuario.objects.all()
        # usuario_logueado=Sesion.objects.get(idSesion=request.COOKIES['idsesion']).usuario ESTO ES PARA QUE CUANDO MUESTRE TODOS LOS USUARIOS NO TE MOSTRES A VOS MISMO
        usuario_logueado=obtener_datos_json(request)

        usuarios=[]
        for usuario in usuarios_todos:
            print usuario.OIDUsuario
            print usuario_logueado.OIDUsuario
            print (usuario == usuario_logueado)
            if (usuario == usuario_logueado)==False:
                usuarios.append(usuario)

        usuarios_json=[usuario.as_json() for usuario in usuarios]
        response.content=dumps(usuarios_json,content_type="application/json")
        response.status_code=200
        return response
    except IntegrityError as err:
        print err.args
        response.status_code=401
        return response


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_PUT])
def agregarUsuarioFinca(request):
    response=HttpResponse()
    datos=obtener_datos_json(request)
    try:
        user=User.objects.get(username=datos['usuario'])
        usuario_ingresado=user.datosusuario
        finca=Finca.objects.get(idFinca=datos['idFinca'])
        rol_ingresado=Rol.objects.get(nombreRol=datos['nombreRol'])
        rol_usuario_finca=RolUsuarioFinca(rol=rol_ingresado,fechaAltaRolUsuarioFinca=datetime.now())

        print "hasta aca bien"
        usuario_finca_nuevo=UsuarioFinca(usuario=usuario_ingresado,finca=finca,fechaAltaUsuarioFinca=datetime.now())
        usuario_finca_nuevo.save()
        rol_usuario_finca.usuarioFinca = usuario_finca_nuevo
        usuario_finca_nuevo.rolUsuarioFincaList.add(rol_usuario_finca,bulk=False)


        response.content_type="application/json"
        response.status_code=200
        return response
    except IntegrityError as err:
        print err.args
        response.status_code=401
        return response


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def modificarRolUsuario(request):
    response=HttpResponse()
    datos=obtener_datos_json(request)
    try:
        user = User.objects.get(username=datos['usuario'])
        usuario_ingresado = user.datosusuario
        finca = Finca.objects.get(idFinca=datos['idFinca'])
        rol_ingresado = Rol.objects.get(nombreRol=datos['nombreRol'])

        usuario_finca=UsuarioFinca.objects.get(usuario=usuario_ingresado,finca=finca)

        rol_usuario_finca_viejo=RolUsuarioFinca.objects.get(usuarioFinca=usuario_finca,fechaBajaRolUsuarioFinca__isnull=True)
        if rol_ingresado == rol_usuario_finca_viejo.rol:
            raise ValueError("El usuario ya dispone de ese rol , por favor intente con otro rol")
        rol_usuario_finca_viejo.fechaBajaRolUsuarioFinca=datetime.now()
        rol_usuario_finca_viejo.save()
        rol_usuario_finca_nuevo=RolUsuarioFinca(usuarioFinca=usuario_finca,fechaAltaRolUsuarioFinca=datetime.now(),rol=rol_ingresado)
        usuario_finca.rolUsuarioFincaList.add(rol_usuario_finca_nuevo,bulk=False)
        usuario_finca.save()
    except (ValueError,IntegrityError) as err:
        print err.args
        response.content=err.args
        response.status_code=401


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def buscarFincaId(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        finca = Finca.objects.get(idFinca=datos['idFinca'])
        response.dumps(finca.as_json())
        return response
    except (ValueError,IntegrityError) as err:
        print err.args
        response.content=err.args
        response.status_code = 401

@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def devolverPermisos(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        finca = Finca.objects.get(idFinca=datos['idFinca'])
        user=request.user
        usuario=user.datosusuario
        usuario_finca=UsuarioFinca.objects.get(usuario=usuario,finca=finca)
        rol_usuario=RolUsuarioFinca.objects.get(usuarioFinca=usuario_finca,fechaBajaRolUsuarioFinca__isnull=True)
        rol=rol_usuario.rol
        permisos=rol.conjuntoPermisos
        response.content=dumps(armar_response_content(permisos,cls=DjangoJSONEncoder))
        response.status_code=200
        return response
    except IntegrityError as err:
        print err.args
        response.content=build_bad_request_error(response,err.args[0],err.args[1])
        response.status_code=401
        return response
