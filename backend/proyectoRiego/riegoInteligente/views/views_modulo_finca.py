# -*- coding: UTF-8 -*-
from django.contrib.auth.models import User
from django.db import IntegrityError

from ..models import Finca, ProveedorInformacionClimaticaFinca, ProveedorInformacionClimatica, \
    EstadoFinca, HistoricoEstadoFinca, UsuarioFinca, DatosUsuario, Rol, RolUsuarioFinca
from supportClases.dto_modulo_finca import *
from supportClases.security_util_functions import *  # Se importa para que se ejecuten los handlers de sesion
from supportClases.security_decorators import *
from supportClases.views_util_functions import *
from supportClases.views_constants import *
from supportClases.error_handler import *


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def obtener_fincas_por_usuario(request):
    response=HttpResponse()
    try:
        user = request.user
        usuario = user.datosusuario
        lista_dto_finca_rol = []
        for usuarioFinca in usuario.usuarioFincaList.all():
            finca = usuarioFinca.finca
            ultimo_historico = HistoricoEstadoFinca.objects.get(finca=finca, fechaFinEstadoFinca__isnull=True)
            if ultimo_historico.estadoFinca.nombreEstadoFinca == ESTADO_HABILITADO:
                rol_usuario_finca = RolUsuarioFinca.objects.get(usuarioFinca=usuarioFinca,
                                                                fechaBajaUsuarioFinca__isnull=True)
                nombre_rol = rol_usuario_finca.rol.nombreRol
                lista_dto_finca_rol.append(DtoFincaRol(nombreFinca=usuarioFinca.finca.nombre, nombreRol=nombre_rol))
        response.content=armar_response_list_content(lista_dto_finca_rol)
        response.content_type = "application/json"
        response.status_code = 200
        return response
    except (IntegrityError, TypeError, KeyError):
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_PUT])
def crear_finca(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if Finca.objects.filter(nombre=datos[KEY_NOMBRE_FINCA], direccionLegal=datos[KEY_DIRECCION_LEGAL]).__len__()\
                == 0:
            finca = Finca(nombre=datos[KEY_NOMBRE_FINCA], direccionLegal=datos[KEY_DIRECCION_LEGAL],
                          ubicacion=datos[KEY_UBICACION],
                          tamanio=datos[KEY_TAMANIO])
            finca.save()
            response.content=armar_response_content(finca)
            response.status_code=200
            return response
        else:
            raise ValueError(ERROR_FINCA_YA_EXISTENTE,"Ya existe una finca con ese nombre")
    except ValueError as err:
        return build_bad_request_error(response, err.args[0],err.args[1])


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_GET])
def buscar_proveedores_informacion(request):
    response=HttpResponse()
    try:
        proveedores = ProveedorInformacionClimatica.objects.filter(habilitado=True)
        response.content=armar_response_list_content(proveedores)
        print "por aca"
        response.status_code=200
        return response
    except (IntegrityError, TypeError, KeyError):
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def elegir_proveedor_informacion(request):
    response=HttpResponse()
    datos=obtener_datos_json(request)
    try:
        if ProveedorInformacionClimatica.objects.filter(nombreProveedor=datos[KEY_NOMBRE_PROVEEDOR]).__len__() == 1:
            proveedorSeleccionado=ProveedorInformacionClimatica.objects.get(nombreProveedor=datos[KEY_NOMBRE_PROVEEDOR])
            fincaCreada=Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
            proveedorInformacionClimaticaFinca=ProveedorInformacionClimaticaFinca(
                proveedorInformacionClimatica=proveedorSeleccionado,finca=fincaCreada)
            proveedorInformacionClimaticaFinca.fechaAltaProveedorInfoClimaticaFinca=datetime.now()
            proveedorInformacionClimaticaFinca.save()
            estadoFinca=EstadoFinca.objects.get(nombreEstadoFinca=ESTADO_PENDIENTE_APROBACION)
            historicoCreado=HistoricoEstadoFinca(fechaInicioEstadoFinca=datetime.now(),estadoFinca=estadoFinca)
            historicoCreado.finca=fincaCreada
            historicoCreado.save()
            print historicoCreado.fechaInicioEstadoFinca
            fincaCreada.historicoEstadoFincaList.add(historicoCreado)
            user = request.user
            usuario = user.datosusuario
            usuarioFinca=UsuarioFinca(usuario=usuario,finca=fincaCreada)
            usuarioFinca.fechaAltaUsuarioFinca = datetime.now()
            usuarioFinca.save()
            fincaCreada.save()
            response.status_code=200
            response.content=armar_response_content(None)
            return response
        else:
            raise ValueError(ERROR_PROVEEDOR_NO_ENCONTRADO, "No se encontro el proveedor seleccionado")
    except ValueError as err:
            return build_bad_request_error(response, err.args[0], err.args[1])
    except (IntegrityError, TypeError, KeyError):
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_GET])
def obtener_fincas_estado_pendiente(request):
    response=HttpResponse()
    try:
        estado_pendiente=EstadoFinca.objects.get(nombreEstadoFinca=ESTADO_PENDIENTE_APROBACION)
        historicos_pendientes=HistoricoEstadoFinca.objects.filter(estadoFinca=estado_pendiente)
        fincas_pendientes=[]
        for historico in historicos_pendientes:
            fincas_pendientes.append(historico.finca)
        response.content = armar_response_list_content(fincas_pendientes)
        response.content_type = "application/json"
        response.status_code = 200
        return response
    except (IntegrityError, TypeError, KeyError):
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")



@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def aprobar_finca(request):
    response=HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if Finca.objects.filter(idFinca=datos[KEY_ID_FINCA]).__len__() == 1:
                finca_por_aprobar = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
                ultimo_historico = finca_por_aprobar.historicoEstadoFincaList.get(fechaFinEstadoFinca__isnull=True)
                if ultimo_historico.estadoFinca.nombreEstadoFinca == ESTADO_HABILITADO:
                    raise ValueError(ERROR_FINCA_YA_APROBADA, "Esta finca ya esta aprobada")

                estado_habilitado = EstadoFinca.objects.get(nombreEstadoFinca=ESTADO_HABILITADO)
                estado_pendiente_aprobacion = EstadoFinca.objects.get(nombreEstadoFinca=ESTADO_PENDIENTE_APROBACION)
                historico_viejo=HistoricoEstadoFinca.objects.get(estadoFinca=estado_pendiente_aprobacion,
                                                                 finca=finca_por_aprobar)
                historico_viejo.fechaFinEstadoFinca = datetime.now()
                historico_viejo.save()
                historico_nuevo = HistoricoEstadoFinca(estadoFinca=estado_habilitado,finca=finca_por_aprobar,
                                                       fechaInicioEstadoFinca=datetime.now())
                finca_por_aprobar.historicoEstadoFincaList.add(historico_nuevo, bulk=False)
                finca_por_aprobar.save()
                usuario_finca = UsuarioFinca.objects.get(finca=finca_por_aprobar)
                rol_encargado = Rol.objects.get(nombreRol=ROL_ENCARGADO)
                rol_usuario_finca = RolUsuarioFinca()
                rol_usuario_finca.fechaAltaRolUsuarioFinca = datetime.now()
                rol_usuario_finca.rol = rol_encargado
                rol_usuario_finca.save()
                usuario_finca.rolUsuarioFincaList.add(rol_usuario_finca)

                # usuario_finca.save()
                # with mail.get_connection() as connection:
                #     mail.EmailMessage('SmartFarming: Estado de Aprobación de su finca','Su finca ha sido aprobada, y usted ya dispone del rol de Encargado',from1='facundocianciop',
                #                       to1='facundocianciop',connection=connection).send()
                #FALTA MANDAR EL MAIL, CONFIGURAR LA CONTRASEÑA Y EL PUERTO
                response.content=armar_response_content(None)
                response.status_code=200
                return response
        else:
            raise ValueError(ERROR_FINCA_NO_ENCONTRADA, "No se encontro la finca seleccionada")
    except ValueError as err:
        return build_bad_request_error(response, err.args[0], err.args[1])
    except (IntegrityError, TypeError, KeyError):
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def no_aprobar_finca(request):
    response=HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if Finca.objects.filter(idFinca=datos[KEY_ID_FINCA]).__len__() == 1:

                finca_por_aprobar=Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
                ultimo_historico = finca_por_aprobar.historicoEstadoFincaList.get(fechaFinEstadoFinca__isnull=True)
                if ultimo_historico.estadoFinca.nombreEstadoFinca == ESTADO_NO_APROBADO:
                    raise ValueError(ERROR_FINCA_YA_DESAPROBADA, "Esta finca ya esta desaprobada")
                estado_pendiente_aprobacion = EstadoFinca.objects.get(nombreEstadoFinca=ESTADO_PENDIENTE_APROBACION)
                estado_no_aprobada = EstadoFinca.objects.get(nombreEstadoFinca=ESTADO_NO_APROBADO)
                historico_viejo = HistoricoEstadoFinca.objects.get(estadoFinca=estado_pendiente_aprobacion,
                                                                   finca=finca_por_aprobar)
                historico_viejo.fechaFinEstadoFinca = datetime.now()
                historico_viejo.save()
                historico_nuevo=HistoricoEstadoFinca(estadoFinca=estado_no_aprobada,finca=finca_por_aprobar,
                                                     fechaInicioEstadoFinca=datetime.now())
                finca_por_aprobar.historicoEstadoFincaList.add(historico_nuevo)
                finca_por_aprobar.save()
                usuario_finca = UsuarioFinca.objects.get(finca=finca_por_aprobar)
                # with mail.get_connection() as connection:
                #     mail.EmailMessage('SmartFarming: Estado de Aprobación de su finca',body=datos['mail'],from1='facundocianciop',
                #                       to1='facundocianciop',connection=connection).send()
                #FALTA MANDAR EL MAIL, CONFIGURAR LA CONTRASEÑA Y EL PUERTO
                #ACA PENSE QUE EN CASO DE RECHAZAR LA FINCA QUE EL ADMINISTRADOR ESCRIBIERA UN MENSAJE DICIENDO POR QUÉ LA RECHAZÓ
                response.content = armar_response_content(None)
                response.status_code = 200
                return response
        else:
            raise ValueError(ERROR_FINCA_NO_ENCONTRADA, "No se encontro la finca seleccionada")
    except ValueError as err:
        return build_bad_request_error(response, err.args[0], err.args[1])
    except (IntegrityError, TypeError, KeyError):
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_GET])
def mostrar_fincas_encargado(request):
    response=HttpResponse()
    try:
        user = request.user
        usuario = user.datosusuario
        usuario_finca_lista = usuario.usuarioFincaList.all()
        fincas_encargado = []
        for usuario_finca in usuario_finca_lista:
            rol = RolUsuarioFinca.objects.get(usuarioFinca=usuario_finca, fechaBajaRolUsuarioFinca__isnull=True).rol
            if rol.nombreRol == ROL_ENCARGADO:
                fincas_encargado.append(usuario_finca.finca)
        response.content = armar_response_list_content(fincas_encargado)
        response.content_type = "application/json"
        response.status_code = 200
        return response
    except (IntegrityError, TypeError, KeyError):
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def modificar_finca(request):
    response=HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if Finca.objects.filter(idFinca=datos[KEY_ID_FINCA]).__len__() == 1:
            finca_a_modificar = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
            finca_a_modificar.nombre = datos[KEY_NOMBRE_FINCA]
            finca_a_modificar.ubicacion = datos[KEY_UBICACION]
            finca_a_modificar.tamanio = datos[KEY_TAMANIO]
            finca_a_modificar.direccionLegal = datos[KEY_DIRECCION_LEGAL]
            finca_a_modificar.logoFinca = datos[KEY_LOGO]
            historico_actual = HistoricoEstadoFinca.objects.get(finca=finca_a_modificar,
                                                                fechaFinEstadoFinca__isnull=True)
            if datos[KEY_ESTADO_FINCA] != '':
                if historico_actual.estadoFinca.nombreEstadoFinca != datos[KEY_ESTADO_FINCA]:
                    estado__nuevo=  EstadoFinca.objects.get(nombreEstadoFinca=datos[KEY_ESTADO_FINCA])
                    historico_actual.fechaFinEstadoFinca = datetime.now()
                    historico_actual.save()
                    historico_nuevo = HistoricoEstadoFinca(fechaInicioEstadoFinca=datetime.now(),
                                                           finca=finca_a_modificar, estadoFinca=estado__nuevo)
                    historico_nuevo.save()
            finca_a_modificar.save()
            response.content = armar_response_content(finca_a_modificar)
            response.content_type = "application/json"
            response.status_code = 200
            return response
        else:
            raise ValueError(ERROR_FINCA_NO_ENCONTRADA, "No se encontro la finca seleccionada")
    except ValueError as err:
        return build_bad_request_error(response, err.args[0], err.args[1])
    except (IntegrityError, TypeError, KeyError):
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def buscar_no_encargados(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
        usuarios_finca = UsuarioFinca.objects.filter(finca=finca)
        rol_stakeholder = Rol.objects.get(nombreRol=ROL_STAKEHOLDER)
        DTO_usuario_finca_list = []
        for usuario_finca in usuarios_finca:
            if RolUsuarioFinca.objects.filter(usuarioFinca=usuario_finca, rol=rol_stakeholder,
                                              fechaBajaRolUsuarioFinca__isnull=True).__len__() == 1:
                DTO_usuario_finca_list.append(DtoUsuarioFinca(OIDUsuarioFinca=usuario_finca.OIDUsuarioFinca,
                                                              usuario=usuario_finca.usuario.user.username,
                                                              nombreUsuario=usuario_finca.usuario.user.first_name,
                                                              apellidoUsuario=usuario_finca.usuario.user.last_name,
                                                              email=usuario_finca.usuario.user.email,
                                                              imagenUsuario=usuario_finca.usuario.imagenUsuario))

                #SI EXISTE SIGNIFICA QUE ES UN USUARIO DE ESA FINCA CON EL ROL STAKEHOLDER Y LO AGREGO A LA LISTA
        response.content = armar_response_list_content(DTO_usuario_finca_list)
        response.content_type = "application/json"
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
