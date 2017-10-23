from urllib2 import urlopen, URLError
import json

from riegoInteligente.models import ProveedorInformacionClimatica, MedicionInformacionClimaticaDetalle, \
    TipoMedicionClimatica

NOMBRE_PROVEEDOR_OPEN_WEATHER = 'openweather'

# Ejemplo llamada
# http://samples.openweathermap.org/data/2.5/weather?lat=35&lon=139&appid=b1b15e88fa797225412429c1c50c122a1


def obtener_mediciones_climaticas(ubicacion):

    url = armar_url(ubicacion)

    try:
        response = urlopen(url)
        datos_respuesta = json.load(response)

        armar_lista_detalle_mediciones(datos_respuesta)

    except (URLError, Exception) as err:
        print 'Error llamando openweather:'


def armar_url(ubicacion):

    open_weather = ProveedorInformacionClimatica.objects.get(nombreProveedor=NOMBRE_PROVEEDOR_OPEN_WEATHER)

    coordenadas = armar_coordenadas(ubicacion)

    url = "https://" + open_weather.urlAPI + "?" + coordenadas + "&appid=" + open_weather.apiKey

    return url


def armar_coordenadas(ubicacion):

    coordenadas = ubicacion.split(",")
    return "lat=" + coordenadas[0].strip() + "&lon=" + coordenadas[1].strip()


def armar_lista_detalle_mediciones(datos_respuesta):
    print datos_respuesta
