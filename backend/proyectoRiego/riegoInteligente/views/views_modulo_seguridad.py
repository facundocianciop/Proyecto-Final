# -*- coding: UTF-8 -*-
from smtplib import SMTPException

from django.db import IntegrityError, DataError, DatabaseError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned

# noinspection PyUnresolvedReferences
from ..models import DatosUsuario, EstadoUsuario, HistoricoEstadoUsuario, Rol, ConjuntoPermisos

from supportClases.security_util_functions import *  # Se importa para que se ejecuten los handlers de sesion
from supportClases.security_decorators import *
from supportClases.views_util_functions import *
from supportClases.views_constants import *
from supportClases.error_handler import *
from supportClases.dto_modulo_seguridad import *


@transaction.atomic()
@metodos_requeridos([METHOD_PUT])
def registrar_usuario(request):

    datos = obtener_datos_json(request)
    response = HttpResponse()

    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

        # Comprobar que se mandaron los datos obligatorios
        if KEY_USUARIO in datos:
            username = datos[KEY_USUARIO]
        else:
            raise KeyError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_USUARIO_FALTANTE)
        if username == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_REGISTRACION_USUARIO_INCORRECTO)

        if KEY_EMAIL in datos:
            email = datos[KEY_EMAIL]
        else:
            raise KeyError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_EMAIL_FALTANTE)
        if email == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_EMAIL_INCORRECTO)
        if not validar_email(email):
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_EMAIL_INCORRECTO)

        if KEY_CONTRASENIA in datos:
            contrasenia = datos[KEY_CONTRASENIA]
        else:
            raise KeyError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_CONTRASENIA_FALTANTE)
        if contrasenia == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_CONTRASENIA_FORMATO_INCORRECTO)
        elif not validar_contrasenia(password=contrasenia, user=None):
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CONTRASENIA_FORMATO_INCORRECTO)

        if KEY_NOMBRE_USUARIO in datos:
            first_name = datos[KEY_NOMBRE_USUARIO]
        else:
            raise KeyError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_NOMBRE_FALTANTE)
        if first_name == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_REGISTRACION_NOMBRE_INCORRECTO)

        if KEY_APELLIDO_USUARIO in datos:
            last_name = datos[KEY_APELLIDO_USUARIO]
        else:
            raise KeyError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_APELLIDO_FALTANTE)
        if last_name == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_REGISTRACION_APELLIDO_INCORRECTO)

        # Se comprueba si se mandan los datos no obligatorios
        dni = None
        if KEY_DNI in datos:
            dni = datos[KEY_DNI]
            if dni.isdigit() and len(str(dni)) == 8:
                dni = int(dni)
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_DNI_INCORRECTO)

        cuit = None
        if KEY_CUIT in datos:
            cuit = str(datos[KEY_CUIT])
            validate_regex(cuit, REGEX_CUIT, DETALLE_ERROR_REGISTRACION_CUIT_INCORRECTO)

        domicilio = None
        if KEY_DOMICILIO in datos:
            domicilio = datos[KEY_DOMICILIO]

        fecha_nacimiento = None
        if KEY_FECHA_NACIMIENTO in datos:
            if datos[KEY_FECHA_NACIMIENTO] != '':
                fecha_nacimiento = parsear_datos_fecha(datos[KEY_FECHA_NACIMIENTO])

        imagen_usuario = None
        if KEY_IMAGEN_USUARIO in datos:
            if datos[KEY_IMAGEN_USUARIO] != '':
                # TODO Validar tipo de archivo imagen
                imagen_usuario = datos[KEY_IMAGEN_USUARIO]

        # Se comprueba que el usuario ingresado no exista en el sistema
        if User.objects.filter(username=datos[KEY_USUARIO]).__len__() >= 1:
            raise ValueError(ERROR_USUARIO_EXISTENTE, DETALLE_ERROR_REGISTRACION_USUARIO_EXISTENTE)

        # Se comprueba que el email ingresado no exista en el sistema
        if User.objects.filter(email=datos[KEY_EMAIL]).__len__() >= 1:
            raise ValueError(ERROR_EMAIL_EXISTENTE, DETALLE_ERROR_EMAIL_EXISTENTE)

        # Creo los objetos necesarios
        estado = EstadoUsuario.objects.get(nombreEstadoUsuario=ESTADO_ACTIVADO)
        historico = HistoricoEstadoUsuario(fechaInicioEstadoUsuario=datetime.now(pytz.utc), estadoUsuario=estado)
        historico.save()

        user = User.objects.create_user(username=username,
                                        email=email,
                                        password=contrasenia,
                                        )
        user.first_name = first_name
        user.last_name = last_name

        user.datosusuario.historicoEstadoUsuarioList.add(historico)
        if cuit:
            user.datosusuario.cuit = cuit
        if dni:
            user.datosusuario.dni = dni
        if domicilio:
            user.datosusuario.domicilio = domicilio
        if fecha_nacimiento:
            user.datosusuario.fechaNacimiento = fecha_nacimiento
        if imagen_usuario:
            user.datosusuario.imagenUsuario = imagen_usuario

        user.datosusuario.save()
        user.save()

        response.content = armar_response_content(None, DETALLE_REGISTRACION_USUARIO_CREADO_CORRECTAMENTE)
        response.status_code = 200

        return response

    except KeyError as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

    except (ValueError, TypeError, AttributeError, DataError, IntegrityError) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned, DatabaseError) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (SystemError, RuntimeError) as err:
        if len(err.args) == 2:
            return build_internal_server_error(response, err.args[0], err.args[1])
        else:
            return build_internal_server_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_DESCONOCIDO)


@transaction.atomic()
@metodos_requeridos([METHOD_POST])
def iniciar_sesion(request):

    datos = obtener_datos_json(request)
    response = HttpResponse()

    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        if KEY_USUARIO in datos and KEY_CONTRASENIA in datos:
            if datos[KEY_USUARIO] == '' or datos[KEY_CONTRASENIA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_LOG_IN_FALLIDO)
            nombre_usuario = datos[KEY_USUARIO]
            contrasenia = datos[KEY_CONTRASENIA]
            usuario = authenticate(username=nombre_usuario, password=contrasenia)
            if usuario is not None:
                login(request, usuario)
                response.content = armar_response_content(usuario.datosusuario)
                response.status_code = 200
                return response
            else:
                raise ValueError(ERROR_CREDENCIALES_INCORRECTAS, DETALLE_ERROR_LOG_IN_FALLIDO)
        else:
            raise ValueError(ERROR_CREDENCIALES_INCORRECTAS, DETALLE_ERROR_LOG_IN_FALLIDO)

    except KeyError as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

    except (ValueError, TypeError, AttributeError, DataError, IntegrityError) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned, DatabaseError) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (SystemError, RuntimeError) as err:
        if len(err.args) == 2:
            return build_internal_server_error(response, err.args[0], err.args[1])
        else:
            return build_internal_server_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_DESCONOCIDO)


@transaction.atomic()
@metodos_requeridos([METHOD_POST])
def finalizar_sesion(request):

    response = HttpResponse()

    try:
        if request.user is not None:
            logout(request)
            response.content = armar_response_content(None)
            response.status_code = 200
            return response
        else:
            raise ValueError

    except (KeyError, ValueError, TypeError, AttributeError, IntegrityError, DataError, SystemError, RuntimeError,
            ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned, DatabaseError) as err:
        if len(err.args) == 2:
            return build_internal_server_error(response, err.args[0], err.args[1])
        else:
            return build_internal_server_error(response, ERROR_LOGOUT_FALLIDO, DETALLE_ERROR_LOG_OUT_FALLIDO)


@transaction.atomic()
@metodos_requeridos([METHOD_POST])
def recuperar_cuenta(request):

    datos = obtener_datos_json(request)
    response = HttpResponse()

    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")

        email = datos[KEY_EMAIL]
        usuario = User.objects.get(email=email)

        codigo_verificacion = id_generator()
        usuario.datosusuario.codigoVerificacion = codigo_verificacion



        # TODO mandar mail

        # with mail.get_connection() as connection:
        # mail.EmailMessage('SmartFarming: Recuperacion de cueta ',body="Su nueva contraseña es
        # %s"%contrasenia_aleatoria,from1='facundocianciop',
        #                       to1='facundocianciop',connection=connection).send()
        # FALTA MANDAR EL MAIL, CONFIGURAR LA CONTRASEÑA Y EL PUERTO
        # ACA PENSE QUE EN CASO DE RECHAZAR LA FINCA QUE EL ADMINISTRADOR ESCRIBIERA UN MENSAJE DICIENDO
        # POR QUÉ LA RECHAZÓ

        usuario.save()

        response.content = armar_response_content(None, DETALLE_RECUPERAR_CUENTA_EJECUTADA)
        response.status_code = 200
        return response

    except KeyError as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

    except (ValueError, TypeError, AttributeError, DataError, IntegrityError) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned, DatabaseError) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (SystemError, RuntimeError) as err:
        if len(err.args) == 2:
            return build_internal_server_error(response, err.args[0], err.args[1])
        else:
            return build_internal_server_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_DESCONOCIDO)


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def cambiar_contrasenia(request):

    datos = obtener_datos_json(request)
    response = HttpResponse()

    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

        # Se comprueba que se enviaron los datos requeridos
        if KEY_CONTRASENIA_VIEJA in datos:
            contrasenia_vieja = datos[KEY_CONTRASENIA_VIEJA]
        else:
            raise KeyError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CAMBIAR_CONTRASENIA_VIEJA_FALTANTE)
        if contrasenia_vieja == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_CAMBIAR_CONTRASENIA_VIEJA_FALTANTE)

        if KEY_CONTRASENIA_NUEVA in datos:
            contrasenia_nueva = datos[KEY_CONTRASENIA_NUEVA]
        else:
            raise KeyError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CAMBIAR_CONTRASENIA_NUEVA_FALTANTE)
        if contrasenia_nueva == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_CONTRASENIA_FORMATO_INCORRECTO)
        elif not validar_contrasenia(password=contrasenia_nueva, user=request.user):
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CONTRASENIA_FORMATO_INCORRECTO)

        username = request.user.get_username()

        user = authenticate(username=username, password=contrasenia_vieja)
        if user is not None:
            user.set_password(contrasenia_nueva)
            user.save()

            logout(request)
            response.content = armar_response_content(None, DETALLE_CONTRASENIA_MODIFICADA_CORRECTAMENTE)
            response.status_code = 200
            return response

        else:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CONTRASENIA_VIEJA_INCORRECTA)

    except KeyError as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

    except (ValueError, TypeError, AttributeError, DataError, IntegrityError) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned, DatabaseError) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (SystemError, RuntimeError) as err:
        if len(err.args) == 2:
            return build_internal_server_error(response, err.args[0], err.args[1])
        else:
            return build_internal_server_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_DESCONOCIDO)


@transaction.atomic()
@login_requerido
@metodos_requeridos([METHOD_POST])
def modificar_usuario(request):

    datos = obtener_datos_json(request)
    response = HttpResponse()

    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

        # Comprobar que se mandaron los datos obligatorios
        if KEY_EMAIL in datos:
            email = datos[KEY_EMAIL]
        else:
            raise KeyError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_EMAIL_FALTANTE)
        if email == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_EMAIL_INCORRECTO)
        if not validar_email(email):
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_EMAIL_INCORRECTO)

        if KEY_CONTRASENIA in datos:
            contrasenia = datos[KEY_CONTRASENIA]
        else:
            raise KeyError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_CONTRASENIA_FALTANTE)
        if contrasenia == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_CONTRASENIA_FORMATO_INCORRECTO)
        elif not validar_contrasenia(password=contrasenia, user=None):
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CONTRASENIA_FORMATO_INCORRECTO)

        if KEY_NOMBRE_USUARIO in datos:
            first_name = datos[KEY_NOMBRE_USUARIO]
        else:
            raise KeyError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_NOMBRE_FALTANTE)
        if first_name == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_REGISTRACION_NOMBRE_INCORRECTO)

        if KEY_APELLIDO_USUARIO in datos:
            last_name = datos[KEY_APELLIDO_USUARIO]
        else:
            raise KeyError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_APELLIDO_FALTANTE)
        if last_name == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_REGISTRACION_APELLIDO_INCORRECTO)

        # Se comprueba si se mandan los datos no obligatorios
        dni = None
        if KEY_DNI in datos:
            dni = datos[KEY_DNI]
            if dni.isdigit() and len(str(dni)) == 8:
                dni = int(dni)
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_DNI_INCORRECTO)

        cuit = None
        if KEY_CUIT in datos:
            cuit = str(datos[KEY_CUIT])
            validate_regex(cuit, REGEX_CUIT, DETALLE_ERROR_REGISTRACION_CUIT_INCORRECTO)

        domicilio = None
        if KEY_DOMICILIO in datos:
            domicilio = datos[KEY_DOMICILIO]

        fecha_nacimiento = None
        if KEY_FECHA_NACIMIENTO in datos:
            if datos[KEY_FECHA_NACIMIENTO] != '':
                fecha_nacimiento = parsear_datos_fecha(datos[KEY_FECHA_NACIMIENTO])

        imagen_usuario = None
        if KEY_IMAGEN_USUARIO in datos:
            if datos[KEY_IMAGEN_USUARIO] != '':
                # TODO Validar tipo de archivo imagen
                imagen_usuario = datos[KEY_IMAGEN_USUARIO]

        # Se comprueba que el email ingresado no exista en el sistema
            if User.objects.filter(email=datos[KEY_EMAIL]).__len__() >= 1:
                raise ValueError(ERROR_EMAIL_EXISTENTE, DETALLE_ERROR_EMAIL_EXISTENTE)

        usuario_a_modificar = request.user

        usuario_a_modificar.email = datos[KEY_EMAIL]
        usuario_a_modificar.first_name = datos[KEY_NOMBRE_USUARIO]
        usuario_a_modificar.last_name = datos[KEY_APELLIDO_USUARIO]

        if cuit:
            usuario_a_modificar.datosusuario.cuit = cuit
        if dni:
            usuario_a_modificar.datosusuario.dni = dni
        if domicilio:
            usuario_a_modificar.datosusuario.domicilio = domicilio
        if fecha_nacimiento:
            usuario_a_modificar.datosusuario.fechaNacimiento = fecha_nacimiento
        if imagen_usuario:
            usuario_a_modificar.datosusuario.imagenUsuario = imagen_usuario

        usuario_a_modificar.datosusuario.save()
        usuario_a_modificar.save()

        response.content = armar_response_content(usuario_a_modificar, )
        response.status_code = 200

        return response

    except KeyError as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

    except (ValueError, TypeError, AttributeError, DataError, IntegrityError) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned, DatabaseError) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (SystemError, RuntimeError) as err:
        if len(err.args) == 2:
            return build_internal_server_error(response, err.args[0], err.args[1])
        else:
            return build_internal_server_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_DESCONOCIDO)


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

    except(KeyError, ValueError, TypeError, AttributeError, IntegrityError, DataError, SystemError, RuntimeError,
           ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned, DatabaseError) as err:
        if len(err.args) == 2:
            return build_internal_server_error(response, err.args[0], err.args[1])
        else:
            return build_internal_server_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_SISTEMA)


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

    except(KeyError, ValueError, TypeError, AttributeError, IntegrityError, DataError, SystemError, RuntimeError,
           ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned, DatabaseError) as err:
        if len(err.args) == 2:
            return build_internal_server_error(response, err.args[0], err.args[1])
        else:
            return build_internal_server_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_SISTEMA)


@transaction.atomic()
@metodos_requeridos([METHOD_POST])
def recuperar_cuenta(request):

    datos = obtener_datos_json(request)
    response = HttpResponse()

    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_EMAIL_FALTANTE)

        if KEY_EMAIL in datos:
            email = datos[KEY_EMAIL]
        else:
            raise KeyError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_EMAIL_FALTANTE)
        if email == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_EMAIL_FALTANTE)
        if not validar_email(email):
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_EMAIL_INCORRECTO)

        email = datos[KEY_EMAIL]
        usuario = User.objects.get(email=email)

        codigo_verificacion = id_generator()
        usuario.datosusuario.codigoVerificacion = codigo_verificacion

        # TODO mandar mail
        # with mail.get_connection() as connection:
        # mail.EmailMessage('SmartFarming: Recuperacion de cueta ',body="Su nueva contraseña es
        # %s"%contrasenia_aleatoria,from1='facundocianciop',
        #                       to1='facundocianciop',connection=connection).send()
        # FALTA MANDAR EL MAIL, CONFIGURAR LA CONTRASEÑA Y EL PUERTO
        # ACA PENSE QUE EN CASO DE RECHAZAR LA FINCA QUE EL ADMINISTRADOR ESCRIBIERA UN MENSAJE DICIENDO
        # POR QUÉ LA RECHAZÓ

        titulo_email = "Recuperar cuenta Smart Farming"
        cuerpo_email = "Codigo de verificacion: " + codigo_verificacion
        destino = email

        enviar_email(titulo=titulo_email, mensaje=cuerpo_email, destino=destino)

        usuario.save()

        dto_usuario = DtoRecuperarCuentaUsuario(usuario=usuario.username, email=usuario.email)

        response.content = armar_response_content(dto_usuario, DETALLE_RECUPERAR_CUENTA_EJECUTADA)
        response.status_code = 200
        return response

    except KeyError as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

    except (ValueError, TypeError, AttributeError, DataError, IntegrityError) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned, DatabaseError) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except SMTPException:
        return build_internal_server_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_ENVIO_EMAIL)

    except (SystemError, RuntimeError) as err:
        if len(err.args) == 2:
            return build_internal_server_error(response, err.args[0], err.args[1])
        else:
            return build_internal_server_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_DESCONOCIDO)


@transaction.atomic()
@metodos_requeridos([METHOD_POST])
def cambiar_contrasenia_recuperar_cuenta(request):

    response = HttpResponse()
    datos = obtener_datos_json(request)

    try:
        if KEY_USUARIO in datos:
            username = datos[KEY_USUARIO]
        else:
            raise KeyError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_USUARIO_FALTANTE)
        if username == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_REGISTRACION_USUARIO_INCORRECTO)

        user = User.objects.get(username=username)

        if KEY_CONTRASENIA_NUEVA in datos:
            contrasenia_nueva = datos[KEY_CONTRASENIA_NUEVA]
        else:
            raise KeyError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CAMBIAR_CONTRASENIA_NUEVA_FALTANTE)
        if contrasenia_nueva == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_CONTRASENIA_FORMATO_INCORRECTO)
        elif not validar_contrasenia(password=contrasenia_nueva, user=user):
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CONTRASENIA_FORMATO_INCORRECTO)

        if KEY_CODIGO_VERIFICACION in datos:
            codigo_verificacion = datos[KEY_CODIGO_VERIFICACION]
        else:
            raise KeyError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_VERIFICACION_FALTANTE)
        if codigo_verificacion == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_CODIGO_VERIFICACION_INCORRECTO)

        usuario = user.datosusuario
        if usuario.codigoVerificacion == codigo_verificacion:

            user.set_password(contrasenia_nueva)
            user.save()

            response.content = armar_response_content(None, DETALLE_CONTRASENIA_MODIFICADA_CORRECTAMENTE)
            response.status_code = 200
            return response

        else:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_VERIFICACION_INCORRECTO)

    except KeyError as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

    except (ValueError, TypeError, AttributeError, DataError, IntegrityError) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned, DatabaseError) as err:
        if len(err.args) == 2:
            return build_bad_request_error(response, err.args[0], err.args[1])
        else:
            return build_bad_request_error(response, ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DATOS_INCORRECTOS)

    except (SystemError, RuntimeError) as err:
        if len(err.args) == 2:
            return build_internal_server_error(response, err.args[0], err.args[1])
        else:
            return build_internal_server_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_DESCONOCIDO)
