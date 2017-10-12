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
@metodos_requeridos([METHOD_GET])
def obtener_fincas_por_usuario(request):
    response = HttpResponse()
    try:
        user = request.user
        usuario = user.datosusuario
        lista_dto_finca_rol = []
        for usuarioFinca in usuario.usuarioFincaList.all():
            finca = usuarioFinca.finca
            ultimo_historico = HistoricoEstadoFinca.objects.get(finca=finca, fechaFinEstadoFinca__isnull=True)
            if ultimo_historico.estadoFinca.nombreEstadoFinca == ESTADO_HABILITADO:
                rol_usuario_finca = RolUsuarioFinca.objects.get(usuarioFinca=usuarioFinca,
                                                                fechaBajaRolUsuarioFinca__isnull=True)
                nombre_rol = rol_usuario_finca.rol.nombreRol
                lista_dto_finca_rol.append(DtoFincaRol(nombreFinca=usuarioFinca.finca.nombre, nombreRol=nombre_rol,
                                                       idFinca= finca.idFinca))
        response.content = armar_response_list_content(lista_dto_finca_rol)
        response.status_code = 200
        return response
    except (IntegrityError, TypeError, KeyError) as err:
        print err.args
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")

#permite que la llamada rest sea atómica
@transaction.atomic()
#para poder realizar este método es necesario haber inicado sesión
@login_requerido
#este método sólo acepta una petición del tipo PUT
@metodos_requeridos([METHOD_PUT])
def crear_finca(request):
    #se crea un objeto HttpResponse
    response = HttpResponse()
    #se llama a un método que convierte los datos de la petición en un json
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            #si los datos de la petición llegan vacíos retorna un error datos incompletos
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if (KEY_NOMBRE_FINCA in datos) and (KEY_DIRECCION_LEGAL in datos) and (KEY_UBICACION in datos) and \
                (KEY_TAMANIO in datos) and (KEY_NOMBRE_PROVEEDOR in datos) and (KEY_FRECUENCIA in datos):
                #si alguno de los parámetros no está presente en la petición retorna un erro de datos incompletos
            if datos[KEY_NOMBRE_FINCA] == '' or datos[KEY_DIRECCION_LEGAL] == '' or datos[KEY_UBICACION] == '' \
                    or datos[KEY_TAMANIO] == '' or datos[KEY_NOMBRE_PROVEEDOR] == '' or datos[KEY_FRECUENCIA] == '':
                # si alguno de los datos está vacío retorna un error de datos incompletos
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if Finca.objects.filter(nombre=datos[KEY_NOMBRE_FINCA],
                                    direccionLegal=datos[KEY_DIRECCION_LEGAL]).__len__() != 0:
                #en caso de que exista una finca con ese nombre y con esa dirección legal se retorna un error
                raise ValueError(ERROR_FINCA_YA_EXISTENTE, "Ya existe una finca con ese nombre")
            if ProveedorInformacionClimatica.objects.filter(nombreProveedor=datos[KEY_NOMBRE_PROVEEDOR]).__len__() == 0:
                #en caso de que no exista un proveedor con ese nombre y con esa dirección legal se retorna un error
                raise ValueError(ERROR_PROVEEDOR_NO_ENCONTRADO, "No se encontro el proveedor seleccionado")
            proveedorSeleccionado = ProveedorInformacionClimatica.objects.get(
                nombreProveedor=datos[KEY_NOMBRE_PROVEEDOR])
                #se obtiene al proveedor deseado
            if int(datos[KEY_FRECUENCIA]) > proveedorSeleccionado.frecuenciaMaxPosible:
                #si la frecuencia de actualización es mayor a la permitida por el proveedor se retorna un error
                raise ValueError(ERROR_FRECUENCIA_MAXIMA_SUPERADA,
                                 "No se puede colocar esa frecuencia, ya que es mayor a la permitida por el proveedor")
            #se realiza la creación de la finca con los atributos ingresados
            finca_creada = Finca(nombre=datos[KEY_NOMBRE_FINCA], direccionLegal=datos[KEY_DIRECCION_LEGAL],
                              ubicacion=datos[KEY_UBICACION],
                              tamanio=datos[KEY_TAMANIO])
            #se crea la instancia de proveedorInformacionClimaticaFinca relacionada al proveedor, la finca creada y
            # la frecuencia ingresada
            proveedorInformacionClimaticaFinca = ProveedorInformacionClimaticaFinca(frecuencia=datos[KEY_FRECUENCIA],
                proveedorInformacionClimatica=proveedorSeleccionado, finca=finca_creada)
            #se setea la fecha de alta con la fecha actual
            proveedorInformacionClimaticaFinca.fechaAltaProveedorInfoClimaticaFinca = datetime.now()
            #se guarda el objeto en la base de datos
            proveedorInformacionClimaticaFinca.save()
            #se busca la instancia de estado finca "pendienteaprobacion"
            estadoFinca = EstadoFinca.objects.get(nombreEstadoFinca=ESTADO_PENDIENTE_APROBACION)
            #se realiza la creación de un histórico con fecha actual y relacionado al estado encontrado
            historicoCreado = HistoricoEstadoFinca(fechaInicioEstadoFinca=datetime.now(), estadoFinca=estadoFinca)
            #se setea la finca al histórico creado
            historicoCreado.finca = finca_creada
            #se guarda el histórico en la base de datos
            historicoCreado.save()
            #se agrega el historico a la lista de históricos de la finca
            finca_creada.historicoEstadoFincaList.add(historicoCreado)
            #se obtiene el usuario de la petición actual
            user = request.user
            #se obtienen los datos del usuario
            usuario = user.datosusuario
            #se crea una instancia de UsuarioFinca, relacionada a los datos de usuario encontrado y a la finca creada
            usuario_finca = UsuarioFinca(usuario=usuario, finca=finca_creada)
            #se setea la fecha de alta
            usuario_finca.fechaAltaUsuarioFinca = datetime.now()
            #se guarda la instancia usuario_finca creada
            usuario_finca.save()
            # se guarda la instancia finca creada
            finca_creada.save()
            #se llama al método armar_response_content con parámetro None, de manera de que se arma una respuesta sin
            #contenido, indicando que como resultado True
            response.content=armar_response_content(None)
            #se coloca a la respuesta el código 200, que significa que la llamada fue exitosa
            response.status_code = 200
            return response
        else:
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
    except ValueError as err:
        print err.args
        #en caso de haber ocurrido algún error retornar una respuesta con el nombre del error y su descripción
        return build_bad_request_error(response, err.args[0],err.args[1])


#permite que la llamada rest sea atómica
@transaction.atomic()
#para poder realizar este método es necesario haber inicado sesión
@login_requerido
#este método sólo acepta una petición del tipo GET
@metodos_requeridos([METHOD_GET])
def buscar_proveedores_informacion(request):
    # se crea un objeto HttpResponse
    response=HttpResponse()
    try:
        #se buscan los proveedores que se encuentren habilitados
        proveedores = ProveedorInformacionClimatica.objects.filter(habilitado=True)
        #se arma una respuesta que convierte a los proveedores en un archivo json,guardándose en el content del response
        response.content=armar_response_list_content(proveedores)
        #se coloca a la respuesta el código 200, que significa que la llamada fue exitosa
        response.status_code=200
        return response
    except (IntegrityError, TypeError, KeyError):
        #en caso de ocurrir un error no esperado se construye una respuesta indicando que ocurrió un error
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")





@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_GET])
def obtener_fincas_estado_pendiente(request):
    response = HttpResponse()
    try:
        user = request.user
        usuario = user.datosusuario
        estado_pendiente = EstadoFinca.objects.get(nombreEstadoFinca=ESTADO_PENDIENTE_APROBACION)
        historicos_pendientes = HistoricoEstadoFinca.objects.filter(estadoFinca=estado_pendiente,
                                                                    fechaFinEstadoFinca__isnull=True)
        fincas_pendientes= []
        for historico in historicos_pendientes:
            if UsuarioFinca.objects.filter(finca=historico.finca, usuario=usuario).__len__() == 1:
                 fincas_pendientes.append(historico.finca)
        response.content = armar_response_list_content(fincas_pendientes)
        response.status_code = 200
        return response
    except (IntegrityError, TypeError, KeyError):
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")



@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def aprobar_finca(request, idFinca):
    response=HttpResponse()
    datos = obtener_datos_json(request)
    if request.user.is_staff == False:
        raise ValueError(ERROR_NO_TIENE_PERMISOS, "El usuario no tiene permisos para acceder a esta pagina")
    try:
        # if datos == '':
        #     raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        # if (KEY_ID_FINCA) in datos:
        #     if datos[KEY_ID_FINCA] == '':
        #         raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if Finca.objects.filter(idFinca=idFinca).__len__() == 1:
                    finca_por_aprobar = Finca.objects.get(idFinca=idFinca)
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
    except (IntegrityError, TypeError, KeyError)as err:
        print err.args
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def no_aprobar_finca(request, idFinca):
    response = HttpResponse()
    if request.user.is_staff == False:
        raise ValueError(ERROR_NO_TIENE_PERMISOS, "El usuario no tiene permisos para acceder a esta pagina")
    try:
            if Finca.objects.filter(idFinca=idFinca).__len__() == 1:
                    finca_por_aprobar = Finca.objects.get(idFinca=idFinca)
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
                    historico_nuevo.save()
                    finca_por_aprobar.save()
                    #finca_por_aprobar.historicoEstadoFincaList.add(historico_nuevo)

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
        print err.args
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
        usuario_finca_lista = UsuarioFinca.objects.filter(usuario=usuario, fechaBajaUsuarioFinca__isnull=True)
        fincas_encargado = []
        for usuario_finca in usuario_finca_lista:
            if RolUsuarioFinca.objects.filter(usuarioFinca=usuario_finca, fechaBajaRolUsuarioFinca__isnull=True).__len__() != 0:
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
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if (KEY_NOMBRE_FINCA and KEY_DIRECCION_LEGAL and KEY_UBICACION and KEY_TAMANIO and KEY_ESTADO_FINCA) in datos:
            if datos[KEY_NOMBRE_FINCA] == '' or datos[KEY_DIRECCION_LEGAL] == '' or datos[KEY_UBICACION] == '' \
                    or datos[KEY_TAMANIO] == '' or datos[KEY_ESTADO_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if Finca.objects.filter(idFinca=datos[KEY_ID_FINCA]).__len__() == 1:
                finca_a_modificar = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
                finca_a_modificar.nombre = datos[KEY_NOMBRE_FINCA]
                finca_a_modificar.ubicacion = datos[KEY_UBICACION]
                finca_a_modificar.tamanio = datos[KEY_TAMANIO]
                finca_a_modificar.direccionLegal = datos[KEY_DIRECCION_LEGAL]
                finca_a_modificar.logoFinca = datos[KEY_LOGO]
                historico_actual = HistoricoEstadoFinca.objects.get(finca=finca_a_modificar,
                                                                    fechaFinEstadoFinca__isnull=True)

                if historico_actual.estadoFinca.nombreEstadoFinca != datos[KEY_ESTADO_FINCA]:
                    estado__nuevo=  EstadoFinca.objects.get(nombreEstadoFinca=datos[KEY_ESTADO_FINCA])
                    historico_actual.fechaFinEstadoFinca = datetime.now()
                    historico_actual.save()
                    historico_nuevo = HistoricoEstadoFinca(fechaInicioEstadoFinca=datetime.now(),
                                                           finca=finca_a_modificar, estadoFinca=estado__nuevo)
                    historico_nuevo.save()
                finca_a_modificar.save()
                response.content = armar_response_content(finca_a_modificar)
                response.status_code = 200
                return response
            else:
                raise ValueError(ERROR_FINCA_NO_ENCONTRADA, "No se encontro la finca seleccionada")
        else:
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")

    except ValueError as err:
        return build_bad_request_error(response, err.args[0], err.args[1])
    except (IntegrityError, TypeError, KeyError):
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_GET])
def buscar_roles(request):
    response = HttpResponse()
    try:
        roles = Rol.objects.filter(fechaBajaRol__isnull=True)
        response.content = armar_response_list_content(roles)
        response.status_code = 200
        return response
    except ValueError as err:
        return build_bad_request_error(response, err.args[0], err.args[1])
    except (IntegrityError, TypeError, KeyError) as err:
        print err.args
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def eliminar_finca(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if (KEY_ID_FINCA) in datos:
            if datos[KEY_ID_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            if Finca.objects.filter(idFinca=datos[KEY_ID_FINCA]).__len__() == 1:
                finca_a_eliminar = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
                user = request.user
                usuario = user.datosusuario
                usuario_finca = UsuarioFinca.objects.get(usuario=usuario, finca=finca_a_eliminar,
                                                         fechaBajaUsuarioFinca__isnull=True)
                rol_usuario_finca = RolUsuarioFinca.objects.get(usuarioFinca=usuario_finca,
                                                                fechaBajaRolUsuarioFinca__isnull=True)
                if rol_usuario_finca.rol.nombreRol != 'encargado':
                    raise ValueError(ERROR_USUARIO_NO_ENCARGADO, "Este usuario no tiene los privilegios para eliminar "
                                                                 "esta finca")

                historico_actual = HistoricoEstadoFinca.objects.get(finca=finca_a_eliminar,
                                                                    fechaFinEstadoFinca__isnull=True)

                estado__nuevo = EstadoFinca.objects.get(nombreEstadoFinca=ESTADO_DESHABILITADO)
                historico_actual.fechaFinEstadoFinca = datetime.now()
                historico_actual.save()
                historico_nuevo = HistoricoEstadoFinca(fechaInicioEstadoFinca=datetime.now(),
                                                       finca=finca_a_eliminar, estadoFinca=estado__nuevo)
                historico_nuevo.save()
                finca_a_eliminar.save()
                usuario_finca_list = finca_a_eliminar.usuariofinca_set.all()
                for usuario_finca_a_eliminar in usuario_finca_list:
                    usuario_finca_a_eliminar.fechaBajaUsuarioFinca = datetime.now()
                    ultimo_historico = RolUsuarioFinca.objects.get(usuarioFinca= usuario_finca_a_eliminar,
                                                                   fechaBajaRolUsuarioFinca__isnull= True)
                    ultimo_historico.fechaBajaRolUsuarioFinca = datetime.now()
                    ultimo_historico.save()
                    usuario_finca_a_eliminar.save()
                response.content = armar_response_content(None)
                response.status_code = 200
                return response
            else:
                raise ValueError(ERROR_FINCA_NO_ENCONTRADA, "No se encontro la finca seleccionada")
        else:
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
    except ValueError as err:
        return build_bad_request_error(response, err.args[0], err.args[1])
    except (IntegrityError, TypeError, KeyError) as err:
        print err.args
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")

@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def buscar_usuarios_no_encargado(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if (KEY_ID_FINCA) in datos:
            if datos[KEY_ID_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
            usuarios_finca = UsuarioFinca.objects.filter(finca=finca, fechaBajaUsuarioFinca__isnull=True)
            rol_encargado = Rol.objects.get(nombreRol=ROL_ENCARGADO)
            dto_usuario_finca_list = []
            for usuario_finca in usuarios_finca:

                rol_actual = RolUsuarioFinca.objects.get(usuarioFinca=usuario_finca,
                                                            fechaBajaRolUsuarioFinca__isnull=True)
                if rol_actual.rol != rol_encargado:
                    dto_usuario_finca_list.append(DtoUsuarioFinca(idUsuarioFinca=usuario_finca.idUsuarioFinca,
                                                                  usuario=usuario_finca.usuario.user.username,
                                                                  nombreUsuario=usuario_finca.usuario.user.first_name,
                                                                  apellidoUsuario=usuario_finca.usuario.user.last_name,
                                                                  email=usuario_finca.usuario.user.email,
                                                                  imagenUsuario=usuario_finca.usuario.imagenUsuario,
                                                                  rol= rol_actual.rol.nombreRol))

                    #SI EXISTE SIGNIFICA QUE ES UN USUARIO DE ESA FINCA CON EL ROL STAKEHOLDER Y LO AGREGO A LA LISTA
            response.content = armar_response_list_content(dto_usuario_finca_list)
            response.status_code=200
            return response
        else:
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
    except (IntegrityError, TypeError, KeyError):
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def eliminar_usuario_finca(request):
    response=HttpResponse()
    datos=obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if (KEY_ID_USUARIO_FINCA) in datos:
            if datos[KEY_ID_USUARIO_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            usuarios_finca = UsuarioFinca.objects.get(idUsuarioFinca=datos[KEY_ID_USUARIO_FINCA])
            usuarios_finca.fechaBajaUsuarioFinca = datetime.now()
            usuarios_finca.save()
            response.content = armar_response_content(None)
            response.status_code = 200
            return response
        else:
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
    except IntegrityError as e:
        print e.args
        response.status_code=401
        return response


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
@manejar_errores()
def buscar_usuarios_no_finca(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)

    if datos == '':
        raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
    if (KEY_ID_FINCA) in datos:
        if datos[KEY_ID_FINCA] == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        usuarios_todos = DatosUsuario.objects.all()
        user = request.user
        usuario_logueado = user.datosusuario
        usuarios = []
        finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
        for usuario in usuarios_todos:
            if ((UsuarioFinca.objects.filter(usuario=usuario, finca= finca,
                                             fechaBajaUsuarioFinca__isnull=True).__len__() == 0) and
                    ((usuario == usuario_logueado)==False)) and usuario.user.is_staff == False:
                usuarios.append(usuario)
        response.content=armar_response_list_content(usuarios)
        response.status_code = 200
        return response
    else:
        raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_PUT])
def agregar_usuario_finca(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if User.objects.filter(username=datos[KEY_USUARIO]).__len__() == 0:
            raise ValueError(ERROR_USUARIO_NO_ENCONTRADO, "No se encuentra al usuario")
        user = User.objects.get(username=datos[KEY_USUARIO])
        usuario_ingresado = user.datosusuario
        finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
        rol_ingresado = Rol.objects.get(nombreRol=datos[KEY_NOMBRE_ROL])
        rol_usuario_finca = RolUsuarioFinca(rol=rol_ingresado, fechaAltaRolUsuarioFinca=datetime.now())
        usuario_finca_nuevo = UsuarioFinca(usuario=usuario_ingresado, finca=finca, fechaAltaUsuarioFinca=datetime.now())
        usuario_finca_nuevo.save()
        print "joya"
        rol_usuario_finca.usuarioFinca = usuario_finca_nuevo
        usuario_finca_nuevo.rolUsuarioFincaList.add(rol_usuario_finca,bulk=False)
        response.content=armar_response_content(None)
        response.status_code=200
        return response
    except ValueError as err:
        return build_bad_request_error(response, err.args[0], err.args[1])
    except (IntegrityError, TypeError, KeyError) as err:
        print err.args
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def modificar_rol_usuario(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if (KEY_ID_FINCA and KEY_USUARIO and KEY_NOMBRE_ROL) in datos:
            if datos[KEY_ID_FINCA] == '' or datos[KEY_USUARIO] == '' or datos[KEY_NOMBRE_ROL] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            user = User.objects.get(username=datos[KEY_USUARIO])
            usuario_ingresado = user.datosusuario
            finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
            rol_ingresado = Rol.objects.get(nombreRol=datos[KEY_NOMBRE_ROL])

            usuario_finca = UsuarioFinca.objects.get(usuario=usuario_ingresado,finca=finca,
                                                     fechaBajaUsuarioFinca__isnull=True)

            rol_usuario_finca_viejo=RolUsuarioFinca.objects.get(usuarioFinca=usuario_finca,
                                                                fechaBajaRolUsuarioFinca__isnull=True)
            if rol_ingresado == rol_usuario_finca_viejo.rol:
                raise ValueError(ERROR_USUARIO_YA_TIENE_ESE_ROL, "El usuario ya dispone de ese rol, por favor intente con otro rol")
            rol_usuario_finca_viejo.fechaBajaRolUsuarioFinca=datetime.now()
            rol_usuario_finca_viejo.save()
            rol_usuario_finca_nuevo = RolUsuarioFinca(usuarioFinca=usuario_finca,fechaAltaRolUsuarioFinca=datetime.now(),rol=rol_ingresado)
            usuario_finca.rolUsuarioFincaList.add(rol_usuario_finca_nuevo,bulk=False)
            usuario_finca.save()
            response.content = armar_response_content(None)
            return response
        else:
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
    except (ValueError,IntegrityError) as err:
        print err.args
        response.content=err.args
        response.status_code=401


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def buscar_finca_id(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if (KEY_ID_FINCA) in datos:
            if datos[KEY_ID_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
            response.content = armar_response_content(finca)
            return response
        else:
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
    except (ValueError,IntegrityError) as err:
        print err.args
        response.content=err.args

@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def devolver_permisos(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if (KEY_ID_FINCA) in datos:
            if datos[KEY_ID_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
            finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
            user=request.user
            usuario=user.datosusuario
            usuario_finca = UsuarioFinca.objects.get(usuario=usuario, finca=finca)
            rol_usuario = RolUsuarioFinca.objects.get(usuarioFinca=usuario_finca, fechaBajaRolUsuarioFinca__isnull=True)
            rol = rol_usuario.rol
            permisos = rol.conjuntoPermisos
            response.content = armar_response_content(permisos)
            response.status_code=200
            return response
        else:
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
    except (IntegrityError, TypeError, KeyError) as err:
        print err.args
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")

