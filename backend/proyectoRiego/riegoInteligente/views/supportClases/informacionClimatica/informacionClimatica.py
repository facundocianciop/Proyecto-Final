from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned

from riegoInteligente.models import *
from riegoInteligente.views.supportClases.informacionClimatica import adaptadorOpenWeather


@transaction.atomic()
def obtener_mediciones_finca(id_finca):

    try:
        finca = Finca.objects.get(idFinca=id_finca)

        if not finca.ubicacion:
            print "Finca no tiene ubicacion definida"
            return False

        proveedor_info_climatica_finca = \
            ProveedorInformacionClimaticaFinca.objects.get(finca=finca,
                                                           fechaBajaProveedorInfoClimaticaFinca=None)

        proveedor_informacion_climatica = proveedor_info_climatica_finca.proveedorInformacionClimatica

        if not proveedor_informacion_climatica:
            print "Finca no tiene proveedor informacion climatica definido"
            return False

        ultima_medicion = None
        try:
            ultima_medicion = MedicionInformacionClimaticaCabecera.\
                objects.get(proveedor_informacion_climatica_externa=proveedor_info_climatica_finca)
        except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned) as err:
            pass

        if ultima_medicion:
            if not controlar_frecuencia(proveedor_info_climatica_finca.frecuencia, ultima_medicion.fechaHora):
                print "La llamada no cumple con la frecuencia"
                return False

        detalles = obtener_medicion_climatica_proveedor(proveedor_informacion_climatica.nombreProveedor,
                                                        finca.ubicacion)
        if not detalles:
            print "No se crearon los detalles de mediciones"
            return False

        cabecera = armar_cabecera_medicion(proveedor_info_climatica_finca)

        for detalle in detalles:
            detalle.medicion_informacion_climatica_cabecera = cabecera

        return True

    except Exception:
        print "Error obteniendo informacion climatica"
        return False


def controlar_frecuencia(frecuencia, fecha_utima_medicion):

    minutos_minimos_entre_llamadas = 60.0/frecuencia

    tiempo_entre_llamadas = datetime.now(pytz.utc) - fecha_utima_medicion

    minutos_entre_llamadas = tiempo_entre_llamadas.total_seconds()/60.0

    if minutos_entre_llamadas >= minutos_minimos_entre_llamadas:
        return True
    else:
        return False


def obtener_medicion_climatica_proveedor(nombre_proveedor, ubicacion):
    if nombre_proveedor == adaptadorOpenWeather.NOMBRE_PROVEEDOR_OPEN_WEATHER:
        return adaptadorOpenWeather.obtener_mediciones_climaticas(ubicacion)
    else:
        return None


def armar_cabecera_medicion(proveedor_informacion_climatica_finca):

    cabecera_medicion_climatica = MedicionInformacionClimaticaCabecera(
        proveedor_informacion_climatica_externa=proveedor_informacion_climatica_finca,
        fechaHora=datetime.now(pytz.utc)
    )

    return cabecera_medicion_climatica
