from urllib2 import urlopen, URLError
import json

from django.core.exceptions import ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned

from riegoInteligente.models import ProveedorInformacionClimatica, MedicionInformacionClimaticaDetalle, \
    TipoMedicionClimatica
from riegoInteligente.views.supportClases.informacionClimatica.informacionClimaticaUtils import *
from riegoInteligente.views.supportClases.views_constants import *


NOMBRE_PROVEEDOR_OPEN_WEATHER = 'openweather'

# Ejemplo llamada
# http://samples.openweathermap.org/data/2.5/weather?lat=35&lon=139&appid=b1b15e88fa797225412429c1c50c122a1


def obtener_mediciones_climaticas(cabecera_medicion, ubicacion):

    url = armar_url(ubicacion)

    try:
        response = urlopen(url)
        datos_respuesta = json.load(response)

        return armar_lista_detalle_mediciones(cabecera_medicion, datos_respuesta)

    except (URLError, Exception):
        print 'Error llamando openweather:'
        return None


def armar_url(ubicacion):

    open_weather = ProveedorInformacionClimatica.objects.get(nombreProveedor=NOMBRE_PROVEEDOR_OPEN_WEATHER)

    coordenadas = armar_coordenadas(ubicacion)

    url = "https://" + open_weather.urlAPI + "?" + coordenadas + "&appid=" + open_weather.apiKey

    return url


def armar_coordenadas(ubicacion):

    coordenadas = ubicacion.split(",")
    return "lat=" + coordenadas[0].strip() + "&lon=" + coordenadas[1].strip()


def armar_lista_detalle_mediciones(cabecera_medicion, datos_respuesta):
    print datos_respuesta

    detalles_medicion_climatica = []
    numero_renglon = 1

    # Detalle temperatura
    try:
        temperatura_k = datos_respuesta['main']['temp']
        temperatura_c = convertir_kelvin_a_celsius(temperatura_k)

        tipo_medicion_climatica = TipoMedicionClimatica.objects.get(
            nombreTipoMedicionClimatica=TIPO_MEDICION_CLIMATICA_TEMPERATURA)

        medicion_climatica_detalle = MedicionInformacionClimaticaDetalle(
            medicion_informacion_climatica_cabecera=cabecera_medicion,
            nroRenglon=numero_renglon,
            tipo_medicion_climatica=tipo_medicion_climatica,
            valor=temperatura_c
        )
        numero_renglon = numero_renglon + 1
        detalles_medicion_climatica.append(medicion_climatica_detalle)

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned, IndexError):
        pass

    # Detalle humedad
    try:
        humedad_porcentaje = datos_respuesta['main']['humidity']

        tipo_medicion_climatica = TipoMedicionClimatica.objects.get(
            nombreTipoMedicionClimatica=TIPO_MEDICION_CLIMATICA_HUMEDAD)

        medicion_climatica_detalle = MedicionInformacionClimaticaDetalle(
            medicion_informacion_climatica_cabecera=cabecera_medicion,
            nroRenglon=numero_renglon,
            tipo_medicion_climatica=tipo_medicion_climatica,
            valor=humedad_porcentaje
        )
        numero_renglon = numero_renglon + 1
        detalles_medicion_climatica.append(medicion_climatica_detalle)

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned, IndexError):
        pass

    # Detalle presion
    try:
        presion_hpa = datos_respuesta['main']['pressure']

        tipo_medicion_climatica = TipoMedicionClimatica.objects.get(
            nombreTipoMedicionClimatica=TIPO_MEDICION_CLIMATICA_PRESION)

        medicion_climatica_detalle = MedicionInformacionClimaticaDetalle(
            medicion_informacion_climatica_cabecera=cabecera_medicion,
            nroRenglon=numero_renglon,
            tipo_medicion_climatica=tipo_medicion_climatica,
            valor=presion_hpa
        )
        numero_renglon = numero_renglon + 1
        detalles_medicion_climatica.append(medicion_climatica_detalle)

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned, IndexError):
        pass

    # Detalle condicion climatica

    try:
        codigo_condicion = datos_respuesta['weather'][0]['id']

        tipo_medicion_climatica = TipoMedicionClimatica.objects.get(
            nombreTipoMedicionClimatica=TIPO_MEDICION_CLIMATICA_CONDICION)

        medicion_climatica_detalle = MedicionInformacionClimaticaDetalle(
            medicion_informacion_climatica_cabecera=cabecera_medicion,
            nroRenglon=numero_renglon,
            tipo_medicion_climatica=tipo_medicion_climatica,
            valor=codigo_condicion
        )

        numero_renglon = numero_renglon + 1
        detalles_medicion_climatica.append(medicion_climatica_detalle)

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned, IndexError):
        pass

    try:

        if 'rain' in datos_respuesta:
            if '3h' in datos_respuesta['rain']:
                valor = datos_respuesta['rain']['3h']

                tipo_medicion_climatica = TipoMedicionClimatica.objects.get(
                    nombreTipoMedicionClimatica=TIPO_MEDICION_CLIMATICA_PRECIPITACION)

                medicion_climatica_detalle = MedicionInformacionClimaticaDetalle(
                    medicion_informacion_climatica_cabecera=cabecera_medicion,
                    nroRenglon=numero_renglon,
                    tipo_medicion_climatica=tipo_medicion_climatica,
                    valor=valor
                )

                detalles_medicion_climatica.append(medicion_climatica_detalle)
            else:
                valor = 0

                tipo_medicion_climatica = TipoMedicionClimatica.objects.get(
                    nombreTipoMedicionClimatica=TIPO_MEDICION_CLIMATICA_PRECIPITACION)

                medicion_climatica_detalle = MedicionInformacionClimaticaDetalle(
                    medicion_informacion_climatica_cabecera=cabecera_medicion,
                    nroRenglon=numero_renglon,
                    tipo_medicion_climatica=tipo_medicion_climatica,
                    valor=valor
                )

                detalles_medicion_climatica.append(medicion_climatica_detalle)
        else:
            valor = 0

            tipo_medicion_climatica = TipoMedicionClimatica.objects.get(
                nombreTipoMedicionClimatica=TIPO_MEDICION_CLIMATICA_PRECIPITACION)

            medicion_climatica_detalle = MedicionInformacionClimaticaDetalle(
                medicion_informacion_climatica_cabecera=cabecera_medicion,
                nroRenglon=numero_renglon,
                tipo_medicion_climatica=tipo_medicion_climatica,
                valor=valor
            )

            detalles_medicion_climatica.append(medicion_climatica_detalle)

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned, IndexError):
        pass

    return detalles_medicion_climatica
