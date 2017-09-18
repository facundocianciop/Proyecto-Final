# -*- coding: UTF-8 -*-
from django.db import IntegrityError

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# noinspection PyUnresolvedReferences
from ..models import DatosUsuario, EstadoUsuario, HistoricoEstadoUsuario, Rol, ConjuntoPermisos

from supportClases.security_util_functions import *  # Se importa para que se ejecuten los handlers de sesion
from supportClases.security_decorators import *
from supportClases.views_util_functions import *
from supportClases.views_constants import *
from supportClases.error_handler import *


@transaction.atomic()
@metodos_requeridos([METHOD_PUT])
def registrar_usuario(request):

    datos = obtener_datos_json(request)
    response = HttpResponse()

    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")

        if User.objects.filter(username=datos[KEY_USUARIO]).__len__() >= 1:
            raise ValueError(ERROR_USUARIO_EXISTENTE, "El usuario ya existe en el sistema")

        if KEY_USUARIO in datos:
            username = datos[KEY_USUARIO]
        else:
            raise ValueError(ERROR_DATOS_INCORRECTOS, "Falta ingresar usuario")

        if KEY_CONTRASENIA in datos:
            contrasenia = datos[KEY_CONTRASENIA]
        else:
            raise ValueError(ERROR_DATOS_INCORRECTOS, "Falta ingresar contrasenia")

        if KEY_EMAIL in datos:
            email = datos[KEY_EMAIL]
        else:
            raise ValueError(ERROR_DATOS_INCORRECTOS, "Falta ingresar email")

        if KEY_NOMBRE_USUARIO in datos:
            first_name = datos[KEY_NOMBRE_USUARIO]
        else:
            raise ValueError(ERROR_DATOS_INCORRECTOS, "Falta ingresar nombre")

        if KEY_APELLIDO_USUARIO in datos:
            last_name = datos[KEY_APELLIDO_USUARIO]
        else:
            raise ValueError(ERROR_DATOS_INCORRECTOS, "Falta ingresar apellido")

        estado = EstadoUsuario.objects.get(nombreEstadoUsuario=ESTADO_ACTIVADO)
        historico = HistoricoEstadoUsuario(fechaInicioEstadoUsuario=datetime.now(), estadoUsuario=estado)
        historico.save()

        user = User.objects.create_user(username=username, password=contrasenia)

        user.first_name = first_name
        user.last_name = last_name
        user.email = email

        if KEY_DNI in datos:
            user.datosusuario.dni = int(datos[KEY_DNI])

        if KEY_CUIT in datos:
            user.datosusuario.cuit = int(datos[KEY_CUIT])

        if KEY_DOMICILIO in datos:
            user.datosusuario.domicilio = datos[KEY_DOMICILIO]

        if KEY_FECHA_NACIMIENTO in datos:
            user.datosusuario.fechaNacimiento = datos[KEY_FECHA_NACIMIENTO]

        if KEY_IMAGEN_USUARIO in datos:
            user.datosusuario.imagenUsuario = datos[KEY_IMAGEN_USUARIO]

        user.datosusuario.historicoEstadoUsuarioList.add(historico)

        user.datosusuario.save()
        user.save()

        response.content = armar_response_content(None)
        response.status_code = 200

        return response

    except ValueError as err:
        return build_bad_request_error(response, err.args[0], err.args[1])

    except KeyError:
        return build_bad_request_error(response, ERROR_DATOS_FALTANTES, "Faltan ingresar datos")

    except (IntegrityError, TypeError):
        return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, "Datos incorrectos")


@transaction.atomic()
@metodos_requeridos([METHOD_POST])
def iniciar_sesion(request):

    datos = obtener_datos_json(request)
    response = HttpResponse()

    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")

        nombre_usuario = datos[KEY_USUARIO]
        contrasenia = datos[KEY_CONTRASENIA]

        usuario = authenticate(username=nombre_usuario, password=contrasenia)
        if usuario is not None:
            login(request, usuario)

            response.content = armar_response_content(usuario.datosusuario)
            response.status_code = 200
            return response
        else:
            raise ValueError(ERROR_CREDENCIALES_INCORRECTAS, "Usuario o contrasenia incorrecta")

    except ValueError as err:
        return build_bad_request_error(response, err.args[0], err.args[1])

    except KeyError:
        return build_bad_request_error(response, ERROR_DATOS_FALTANTES, "Faltan ingresar datos")

    except (IntegrityError, TypeError):
        return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, "Datos incorrectos")


@transaction.atomic()
@metodos_requeridos([METHOD_POST])
def finalizar_sesion(request):

    response = HttpResponse()

    try:
        if request.user is None:
            logout(request)
            response.content = armar_response_content(None)
            response.status_code = 200
            return response
        else:
            raise ValueError

    except (IntegrityError, ValueError, KeyError):
        return build_bad_request_error(response, ERROR_LOGOUT_FALLIDO, "Log out fallo")


@transaction.atomic()
@metodos_requeridos([METHOD_POST])
def recuperar_cuenta(request):

    datos = obtener_datos_json(request)
    response = HttpResponse()

    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")

        email = datos[KEY_EMAIL]
        print email
        usuario = User.objects.get(email=email)
        print usuario.email
        codigo_verificacion = id_generator()
<<<<<<< HEAD
        usuario.datosusuario.codigoVerificacion(codigo_verificacion)
        print(codigo_verificacion)
=======
        usuario.datosusuario.codigoVerificacion=codigo_verificacion
>>>>>>> 459914e712c1ce5693539e244df67783e1ea93ac
        # with mail.get_connection() as connection:
        # mail.EmailMessage('SmartFarming: Recuperacion de cueta ',body="Su nueva contraseña es
        # %s"%contrasenia_aleatoria,from1='facundocianciop',
        #                       to1='facundocianciop',connection=connection).send()
        # FALTA MANDAR EL MAIL, CONFIGURAR LA CONTRASEÑA Y EL PUERTO
        # ACA PENSE QUE EN CASO DE RECHAZAR LA FINCA QUE EL ADMINISTRADOR ESCRIBIERA UN MENSAJE DICIENDO
        # POR QUÉ LA RECHAZÓ
        response_data = {}
        response_data[KEY_USUARIO] = usuario.username
        response.content=dumps(response_data)
        #response.content = armar_response_content(response_data)
        response.status_code = 200
        return response

    except ValueError as err:
        return build_bad_request_error(response, err.args[0], err.args[1])

    except KeyError:
        return build_bad_request_error(response, ERROR_DATOS_FALTANTES, "Faltan ingresar datos")

    except (IntegrityError, TypeError) as err:
        print err.args
        return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, "Datos incorrectos")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def cambiar_contrasenia(request):

    datos = obtener_datos_json(request)
    response = HttpResponse()

    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")

        usuario_a_modificar = request.user
        username = usuario_a_modificar.get_username()
        contrasenia_vieja = datos[KEY_CONTRASENIA_VIEJA]
        contrasenia_nueva = datos[KEY_CONTRASENIA_NUEVA]

        user = authenticate(username=username, password=contrasenia_vieja)
        if user is not None:
            user.set_password(contrasenia_nueva)
            user.save()

            logout(request)
            response.content = armar_response_content(None)
            response.status_code = 200
            return response

        else:
            raise ValueError(ERROR_DATOS_INCORRECTOS, "Contrasenia incorrecta")

    except ValueError as err:
        return build_unauthorized_error(response, err.args[0], err.args[1])

    except KeyError:
        return build_bad_request_error(response, ERROR_DATOS_FALTANTES, "Faltan ingresar datos")

    except (IntegrityError, TypeError):
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def modificar_usuario(request):

    datos = obtener_datos_json(request)
    response = HttpResponse()

    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")

        usuario_a_modificar = request.user

        if KEY_USUARIO in datos:
            usuario_a_modificar.username = datos[KEY_USUARIO]
        else:
            raise ValueError(ERROR_DATOS_INCORRECTOS, "Falta ingresar usuario")

        if KEY_EMAIL in datos:
            usuario_a_modificar.email = datos[KEY_EMAIL]
        else:
            raise ValueError(ERROR_DATOS_INCORRECTOS, "Falta ingresar email")

        if KEY_NOMBRE_USUARIO in datos:
            usuario_a_modificar.first_name = datos[KEY_NOMBRE_USUARIO]
        else:
            raise ValueError(ERROR_DATOS_INCORRECTOS, "Falta ingresar nombre")

        if KEY_APELLIDO_USUARIO in datos:
            usuario_a_modificar.last_name = datos[KEY_APELLIDO_USUARIO]
        else:
            raise ValueError(ERROR_DATOS_INCORRECTOS, "Falta ingresar apellido")

        if KEY_DNI in datos:
            usuario_a_modificar.datosusuario.dni = int(datos[KEY_DNI])

        if KEY_CUIT in datos:
            usuario_a_modificar.datosusuario.cuit = int(datos[KEY_CUIT])

        if KEY_DOMICILIO in datos:
            usuario_a_modificar.datosusuario.domicilio = datos[KEY_DOMICILIO]

        if KEY_FECHA_NACIMIENTO in datos:
            usuario_a_modificar.datosusuario.fechaNacimiento = datos[KEY_FECHA_NACIMIENTO]

        if KEY_IMAGEN_USUARIO in datos:
            usuario_a_modificar.datosusuario.imagenUsuario = datos[KEY_IMAGEN_USUARIO]

        usuario_a_modificar.datosusuario.save()
        usuario_a_modificar.save()

        response.content = armar_response_content(None)
        response.status_code = 200

        return response

    except ValueError as err:
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, TypeError, KeyError):
        return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, "Datos incorrectos")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_DELETE])
def eliminar_usuario(request):

    response = HttpResponse()

    try:
        usuario_a_desactivar = request.user

        ultimo_historico = HistoricoEstadoUsuario.objects.get(usuario=usuario_a_desactivar.datosusuario,
                                                              fechaFinEstadoUsuario__isnull=True)
        ultimo_historico.fechaFinEstadoUsuario = datetime.now()
        ultimo_historico.save()

        estado_desactivado = EstadoUsuario.objects.get(nombreEstadoUsuario=ESTADO_DESACTIVADO)
        nuevo_historico = HistoricoEstadoUsuario(estadoUsuario=estado_desactivado,
                                                 fechaInicioEstadoUsuario=datetime.now(),
                                                 usuario=usuario_a_desactivar.datosusuario)
        nuevo_historico.save()

        usuario_a_desactivar.datosusuario.historicoEstadoUsuarioList.add(nuevo_historico)
        usuario_a_desactivar.datosusuario.save()

        logout(request)
        usuario_a_desactivar.is_active = False
        usuario_a_desactivar.save()

        response.content = armar_response_content(None)
        response.status_code = 200

        return response

    except (IntegrityError, TypeError, KeyError):
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_GET])
def mostrar_usuario(request):

    response = HttpResponse()

    try:
        usuario_actual = request.user

        response.content = armar_response_content(usuario_actual.datosusuario)
        response.status_code = 200

        return response

    except (IntegrityError, TypeError, KeyError):
        return build_bad_request_error(response, ERROR_DE_SISTEMA, "Error procesando llamada")


@transaction.atomic()
@metodos_requeridos([METHOD_POST])
def cambiar_contrasenia_recuperar_cuenta(request):
    response = HttpResponse()
    datos = obtener_datos_json(request)
    try:
        if KEY_CONTRASENIA_NUEVA not in datos:
            raise KeyError(ERROR_DATOS_FALTANTES, "Falta el dato contrasenia")
        contrasenia_nueva = datos[KEY_CONTRASENIA_NUEVA]
        user = User.objects.filter(codigoVerificacion=datos[KEY_CODIGO_VERIFICACION], username=datos[KEY_USUARIO])

        if user is not None:
            user.set_password(contrasenia_nueva)
            user.save()
            response_data = {}
            response_data[KEY_RESULTADO_OPERACION] = True
            response.content = armar_response_content(response_data)
            response.status_code = 200
            return response
        else:
            raise ValueError(ERROR_DATOS_INCORRECTOS, "No hay un usuario con esos datos")
    except KeyError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])

    except ValueError as err:
        print(err.args)
        return build_bad_request_error(response, err.args[0], err.args[1])



