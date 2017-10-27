
TIPO_MEDICION_CLIMATICA_TEMPERATURA = 'temperatura'
TIPO_MEDICION_CLIMATICA_HUMEDAD = 'humedad'
TIPO_MEDICION_CLIMATICA_PRESION = 'presion'
TIPO_MEDICION_CLIMATICA_CONDICION = 'condicionClima'


def convertir_fahrenheit_a_celsius(grados_f):
    return (grados_f - 32)/1.8


def convertir_kelvin_a_celsius(grados_k):
    return grados_k - 273.15
