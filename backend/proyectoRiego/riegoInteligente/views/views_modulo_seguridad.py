# -*- coding: UTF-8 -*-
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


@transaction.atomic()
@metodos_requeridos([METHOD_PUT])
def registrar_usuario(request):

    datos = obtener_datos_json(request)
    response = HttpResponse()

    try:
        if datos == '':
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")

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
            raise KeyError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_EMAIL_FALTANTE)
        if email == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_REGISTRACION_EMAIL_INCORRECTO)
        if not validar_email(email):
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_EMAIL_INCORRECTO)

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
        if KEY_DNI in datos:
            dni = int(datos[KEY_DNI])
        else:
            raise KeyError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_DNI_FALTANTE)

        if KEY_CUIT in datos:
            cuit = int(datos[KEY_CUIT])
        else:
            raise KeyError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_CUIT_FALTANTE)

        if KEY_DOMICILIO in datos:
            domicilio = datos[KEY_DOMICILIO]
        else:
            raise KeyError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_DOMICILIO_FALTANTE)

        if KEY_FECHA_NACIMIENTO in datos:
            if datos[KEY_FECHA_NACIMIENTO] != '':
                fecha_nacimiento = parsear_datos_fecha(datos[KEY_FECHA_NACIMIENTO])
            else:
                fecha_nacimiento = None
        else:
            raise KeyError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_FECHA_NACIMIENTO_FALTANTE)

        if KEY_IMAGEN_USUARIO in datos:
            if datos[KEY_IMAGEN_USUARIO] != '':
                # TODO Validar tipo de archivo imagen
                imagen_usuario = datos[KEY_IMAGEN_USUARIO]
            else:
                imagen_usuario = None
        else:
            raise KeyError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_IMAGEN_FALTANTE)

        # Se comprueba que el usuario ingresado no exista en el sistema
        if User.objects.filter(username=datos[KEY_USUARIO]).__len__() >= 1:
            raise ValueError(ERROR_USUARIO_EXISTENTE, DETALLE_ERROR_REGISTRACION_USUARIO_EXISTENTE)

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
        user.datosusuario.cuit = cuit
        user.datosusuario.dni = dni
        user.datosusuario.domicilio = domicilio
        user.datosusuario.fechaNacimiento = fecha_nacimiento
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
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")
        if (KEY_USUARIO and KEY_CONTRASENIA) in datos:
            if datos[KEY_USUARIO] == '' or datos[KEY_CONTRASENIA] == '':
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
        else:
            raise ValueError(ERROR_CREDENCIALES_INCORRECTAS, "Usuario o contrasenia incorrecta")

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
        if request.user is None:
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
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")

        # Se comprueba que se enviaron los datos requeridos
        if KEY_CONTRASENIA_VIEJA in datos:
            contrasenia_vieja = datos[KEY_CONTRASENIA_VIEJA]
        else:
            raise KeyError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CAMBIAR_CONTRASENIA_VIEJA_FALTANTE)
        if contrasenia_vieja == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_CONTRASENIA_INCORRECTA)

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
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CONTRASENIA_INCORRECTA)

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
            raise ValueError(ERROR_DATOS_FALTANTES, "Datos incompletos")

        # TODO validar datos como el registrarse
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
