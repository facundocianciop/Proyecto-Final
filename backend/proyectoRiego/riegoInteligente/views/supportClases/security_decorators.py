# noinspection PyUnresolvedReferences
from datetime import datetime
import pytz
from functools import wraps

from django.http import HttpResponse
from django.utils.decorators import available_attrs
from django.db import IntegrityError, DataError, DatabaseError
from django.core.exceptions import ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned

# noinspection PyUnresolvedReferences
from ...models import DatosUsuario, EstadoUsuario, HistoricoEstadoUsuario, Rol, ConjuntoPermisos, \
    SesionUsuario, UsuarioFinca, ConjuntoPermisos, Finca, Sector, MecanismoRiegoFinca, MecanismoRiegoFincaSector

from views_util_functions import *


def login_requerido(funcion):
    """
    Controla si el usuario haciendo una llamada esta loggeado
    :param funcion:
    :return:
    """
    def wrap(request, *args, **kwargs):
        # verificar que el usuario haciendo la llamada este autenticado
        if request.user.is_authenticated:
            request.session.modified = True
            sesion_usuario = SesionUsuario.objects.get(session_id=request.session.session_key)
            sesion_usuario.fecha_y_hora_ultimo_acceso = datetime.now(pytz.utc)
            sesion_usuario.fecha_y_hora_fin = request.session.get_expiry_date()

            sesion_usuario.save()

            return funcion(request, *args, **kwargs)
        else:
            return build_unauthorized_error(HttpResponse(), ERROR_LOGIN_REQUERIDO, "Usuario no inicio sesion")

    wrap. __doc__ = funcion.__doc__
    wrap. __name__ = funcion.__name__

    return wrap


def metodos_requeridos(request_method_list):
    """
    Controla si el metodo enviado es correcto
    :param request_method_list:
    :return:
    """
    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):
            if request.method not in request_method_list:
                return build_method_not_allowed_error(HttpResponse(), ERROR_METODO_INCORRECTO,
                                                      'Metodo/s requeridos: ' + ', '.join(request_method_list))
            return func(request, *args, **kwargs)
        return inner
    return decorator


def manejar_errores():
    """
    Maneja errores en la operacion
    :return:
    """
    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):

            response = HttpResponse()
            try:

                return func(request, *args, **kwargs)

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
        return inner
    return decorator


def permisos_rol_requeridos(permisos_rol_list):
    """
    Permite ejecutar funcion si el usuario cumple con por lo menos 1 de los permisos que se envian
    :param permisos_rol_list:
    :return:
    """
    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):

            response = HttpResponse()

            datos = obtener_datos_json(request)

            if KEY_ID_FINCA not in datos or datos[KEY_ID_FINCA] == '':
                raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_FINCA_DATOS_FALTANTES)

            finca = Finca.objects.get(idFinca=datos[KEY_ID_FINCA])
            datos_usuario = request.user.datosusuario

            usuario_finca = None
            if finca is not None and datos_usuario is not None:
                usuario_finca = UsuarioFinca.objects.get(finca=finca, usuario=datos_usuario,
                                                         fechaBajaUsuarioFinca=None)

            if usuario_finca is None:
                return build_unauthorized_error(response, ERROR_NO_TIENE_PERMISOS, DETALLE_ERROR_NO_TIENE_PERMISOS)

            if KEY_ID_SECTOR in datos:
                sector_pertenece_a_finca = False
                if Sector.objects.filter(idSector=datos[KEY_ID_SECTOR]).__len__() == 1:
                    sector = Sector.objects.get(idSector=datos[KEY_ID_SECTOR])
                    if finca.sectorList.filter(OIDSector=sector.OIDSector).__len__() == 1:
                            sector_pertenece_a_finca = True
                    if not sector_pertenece_a_finca:
                        return build_unauthorized_error(response, ERROR_NO_TIENE_PERMISOS,
                                                        DETALLE_ERROR_NO_TIENE_PERMISOS)
            if KEY_ID_MECANISMO_RIEGO_FINCA in datos:
                mecanismo_pertenece_a_finca = False
                if MecanismoRiegoFinca.objects.filter(
                        idMecanismoRiegoFinca=datos[KEY_ID_MECANISMO_RIEGO_FINCA]).__len__() == 1:
                    mecanismo_finca = MecanismoRiegoFinca.objects.get(
                        idMecanismoRiegoFinca=datos[KEY_ID_MECANISMO_RIEGO_FINCA])
                    if finca.mecanismoriegofinca_set.filter(
                            OIDMecanismoRiegoFinca=mecanismo_finca.OIDMecanismoRiegoFinca).__len__() == 1:
                        mecanismo_pertenece_a_finca = True
                    if not mecanismo_pertenece_a_finca:
                        return build_unauthorized_error(response, ERROR_NO_TIENE_PERMISOS,
                                                        DETALLE_ERROR_NO_TIENE_PERMISOS)
            if KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR in datos:
                mecanismo_sector_pertenece_a_finca = False
                if MecanismoRiegoFincaSector.objects.filter(
                        idMecanismoRiegoFincaSector=datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR]).__len__() == 1:
                    mecanismo_finca_sector = MecanismoRiegoFincaSector.objects.get(
                        idMecanismoRiegoFincaSector=datos[KEY_ID_MECANISMO_RIEGO_FINCA_SECTOR])
                    mecanismos_finca = finca.mecanismoriegofinca_set.all()
                    for mecanismo_finca in mecanismos_finca:
                        if mecanismo_finca.mecanismoRiegoSectorList.filter(
                                OIDMecanismoRiegoFincaSector=mecanismo_finca_sector.OIDMecanismoRiegoFincaSector)\
                                .__len__() == 1:
                            mecanismo_sector_pertenece_a_finca = True
                    if not mecanismo_sector_pertenece_a_finca:
                        return build_unauthorized_error(response, ERROR_NO_TIENE_PERMISOS,
                                                        DETALLE_ERROR_NO_TIENE_PERMISOS)

            rol_usuario_finca = usuario_finca.rolUsuarioFincaList.order_by('-fechaAltaRolUsuarioFinca').first()
            if rol_usuario_finca is not None:
                conjunto_permisos_rol = ConjuntoPermisos.objects.get(rol=rol_usuario_finca.rol)

                acceso_permitido = False
                for permiso in permisos_rol_list:

                    if permiso == PERMISO_PUEDEASIGNARCOMPONENTESENSOR:
                        acceso_permitido = conjunto_permisos_rol.puedeAsignarComponenteSensor
                        break

                    if permiso == PERMISO_PUEDEASIGNARCULTIVO:
                        acceso_permitido = conjunto_permisos_rol.puedeAsignarCultivo
                        break

                    if permiso == PERMISO_PUEDEASIGNARMECRIEGOAFINCA:
                        acceso_permitido = conjunto_permisos_rol.puedeAsignarMecRiegoAFinca
                        break

                    if permiso == PERMISO_PUEDEASIGNARMECRIEGOASECTOR:
                        acceso_permitido = conjunto_permisos_rol.puedeAsignarMecRiegoASector
                        break

                    if permiso == PERMISO_PUEDECONFIGURAROBTENCIONINFOEXTERNA:
                        acceso_permitido = conjunto_permisos_rol.puedeConfigurarObtencionInfoExterna
                        break

                    if permiso == PERMISO_PUEDECREARCOMPONENTESENSOR:
                        acceso_permitido = conjunto_permisos_rol.puedeCrearComponenteSensor
                        break

                    if permiso == PERMISO_PUEDECREARCONFIGURACIONRIEGO:
                        acceso_permitido = conjunto_permisos_rol.puedeCrearConfiguracionRiego
                        break

                    if permiso == PERMISO_PUEDECREARSECTOR:
                        acceso_permitido = conjunto_permisos_rol.puedeCrearSector
                        break

                    if permiso == PERMISO_PUEDEGENERARINFORMECRUZADORIEGOMEDICION:
                        acceso_permitido = conjunto_permisos_rol.puedeGenerarInformeCruzadoRiegoMedicion
                        break

                    if permiso == PERMISO_PUEDEGENERARINFORMEESTADOACTUALSECTORES:
                        acceso_permitido = conjunto_permisos_rol.puedeGenerarInformeEstadoActualSectores
                        break

                    if permiso == PERMISO_PUEDEGENERARINFORMEESTADOHISTORICOSECTORESFINCA:
                        acceso_permitido = conjunto_permisos_rol.puedeGenerarInformeEstadoHistoricoSectoresFinca
                        break

                    if permiso == PERMISO_PUEDEGENERARINFORMEEVENTOPERSONALIZADO:
                        acceso_permitido = conjunto_permisos_rol.puedeGenerarInformeEventoPersonalizado
                        break

                    if permiso == PERMISO_PUEDEGENERARINFORMEHELADASHISTORICO:
                        acceso_permitido = conjunto_permisos_rol.puedeGenerarInformeHeladasHistorico
                        break

                    if permiso == PERMISO_PUEDEGENERARINFORMERIEGOENEJECUCION:
                        acceso_permitido = conjunto_permisos_rol.puedeGenerarInformeRiegoEnEjecucion
                        break

                    if permiso == PERMISO_PUEDEGENERARINFORMERIEGOPORSECTORESHISTORICO:
                        acceso_permitido = conjunto_permisos_rol.puedeGenerarInformeRiegoPorSectoresHistorico
                        break

                    if permiso == PERMISO_PUEDEGESTIONARCOMPONENTESENSOR:
                        acceso_permitido = conjunto_permisos_rol.puedeGestionarComponenteSensor
                        break

                    if permiso == PERMISO_PUEDEGESTIONARCULTIVOSECTOR:
                        acceso_permitido = conjunto_permisos_rol.puedeGestionarCultivoSector
                        break

                    if permiso == PERMISO_PUEDEGESTIONAREVENTOPERSONALIZADO:
                        acceso_permitido = conjunto_permisos_rol.puedeGestionarEventoPersonalizado
                        break

                    if permiso == PERMISO_PUEDEGESTIONARFINCA:
                        acceso_permitido = conjunto_permisos_rol.puedeGestionarFinca
                        break

                    if permiso == PERMISO_PUEDEGESTIONARSECTOR:
                        acceso_permitido = conjunto_permisos_rol.puedeGestionarSector
                        break

                    if permiso == PERMISO_PUEDEGESTIONARSENSORES:
                        acceso_permitido = conjunto_permisos_rol.puedeGestionarSensores
                        break

                    if permiso == PERMISO_PUEDEGESTIONARUSUARIOSFINCA:
                        acceso_permitido = conjunto_permisos_rol.puedeGestionarUsuariosFinca
                        break

                    if permiso == PERMISO_PUEDEINICIARODETENERRIEGOMANUALMENTE:
                        acceso_permitido = conjunto_permisos_rol.puedeIniciarODetenerRiegoManualmente
                        break

                    if permiso == PERMISO_PUEDEMODIFICARCONFIGURACIONRIEGO:
                        acceso_permitido = conjunto_permisos_rol.puedeModificarConfiguracionRiego
                        break

                if acceso_permitido:
                    return func(request, *args, **kwargs)
                else:
                    return build_unauthorized_error(response, ERROR_NO_TIENE_PERMISOS,
                                                    DETALLE_ERROR_NO_TIENE_PERMISOS)
            else:
                return build_unauthorized_error(response, ERROR_NO_TIENE_PERMISOS, DETALLE_ERROR_NO_TIENE_PERMISOS)
        return inner
    return decorator
