import time

# noinspection PyUnresolvedReferences
from riegoInteligente.models import *

# noinspection PyUnresolvedReferences
from riegoInteligente.views.supportClases.views_constants import *
from riegoInteligente.views.supportClases.informacionClimatica.informacionClimatica import \
    obtener_mediciones_climaticas_finca
from riegoInteligente.views.supportClases.configuracion_riego_util_functions import *

from procesosBackgroundUtils import *


def obtener_mediciones_climaticas():

    # Iniciar proceso de obtencion de estado climatico para todas las fincas habilitadas

    fincas_habilitadas = obtener_fincas_habilitadas()

    for finca in fincas_habilitadas:
        time.sleep(1)
        print "Obteniendo mediciones climaticas para finca: " + finca.nombre
        obtener_mediciones_climaticas_finca(finca.idFinca)


def comprobar_incio_riego_criterio_hora():
    print "Comprobando inicio de riegos por hora"

    fincas_habilitadas = obtener_fincas_habilitadas()

    for finca in fincas_habilitadas:
        print "Comprobando inicio de riegos por hora para finca: " + finca.nombre
        mecanismos_riego_finca_sector_habilitados = obtener_mecanismos_riego_finca_sector_habilitados(finca.idFinca)
        for mecanismo_riego_finca_sector in mecanismos_riego_finca_sector_habilitados:
            print "Comprobando configuraciones de riego de: " + str(mecanismo_riego_finca_sector)

            riego_en_ejecucion = obtener_riego_en_ejecucion_mecanismo_riego_finca_sector(
                mecanismo_riego_finca_sector.idMecanismoRiegoFincaSector)

            configuraciones_riego_habilitadas = obtener_configuraciones_riego_mecanismo_finca_sector_habilitados(
                mecanismo_riego_finca_sector.idMecanismoRiegoFincaSector)

            for configuracion_riego in configuraciones_riego_habilitadas:
                print "Comprobando configuraciones de riego: " + str(configuracion_riego)

                if riego_en_ejecucion and riego_en_ejecucion.configuracion_riego == configuracion_riego:
                    print "Riego ya se esta ejecutando para esta configuracion"
                    break

                criterios_hora = obtener_criterios_inicio_hora_configuracion_riego(
                    configuracion_riego.id_configuracion_riego)

                for criterio in criterios_hora:
                    print "Comprobando criterio: " + criterio.nombre

                    hora_elegida = criterio.hora
                    numero_dia = criterio.numeroDia

                    if numero_dia == 0:
                        if comparar_hora_riego(hora_elegida=hora_elegida):
                            print 'Iniciar riego'
                            iniciar_ejecucion_riego(mecanismo_riego_finca_sector=mecanismo_riego_finca_sector,
                                                    detalle_riego="Riego por hora",
                                                    configuracion_riego=configuracion_riego
                                                    )

                    elif numero_dia == datetime.now(pytz.utc).isocalendar()[2]:
                        if comparar_hora_riego(hora_elegida=hora_elegida):
                            print 'Iniciar riego'
                            iniciar_ejecucion_riego(mecanismo_riego_finca_sector=mecanismo_riego_finca_sector,
                                                    detalle_riego="Riego por hora",
                                                    configuracion_riego=configuracion_riego
                                                    )


def comprobar_fin_riego_criterio_hora():
    print "Comprobando fin de riegos por hora"

    fincas_habilitadas = obtener_fincas_habilitadas()

    for finca in fincas_habilitadas:
        print "Comprobando fin de riegos por hora para finca: " + finca.nombre
        mecanismos_riego_finca_sector_habilitados = obtener_mecanismos_riego_finca_sector_habilitados(finca.idFinca)
        for mecanismo_riego_finca_sector in mecanismos_riego_finca_sector_habilitados:
            print "Comprobando configuraciones de riego de: " + str(mecanismo_riego_finca_sector)

            riego_en_ejecucion = obtener_riego_en_ejecucion_mecanismo_riego_finca_sector(
                mecanismo_riego_finca_sector.idMecanismoRiegoFincaSector)

            if not riego_en_ejecucion:
                break

            configuracion_riego = riego_en_ejecucion.configuracion_riego

            if configuracion_riego:

                print "Comprobando configuraciones de riego: " + str(configuracion_riego)

                criterios_hora = obtener_criterios_inicio_hora_configuracion_riego(
                    configuracion_riego.id_configuracion_riego)

                for criterio in criterios_hora:
                    print "Comprobando criterio: " + criterio.nombre

                    hora_elegida = criterio.hora
                    numero_dia = criterio.numeroDia

                    if numero_dia == 0:
                        if comparar_hora_riego(hora_elegida=hora_elegida):
                            print 'Detener riego'
                            detener_riego(riego_en_ejecucion)

                    elif numero_dia == datetime.now(pytz.utc).isocalendar()[2]:
                        if comparar_hora_riego(hora_elegida=hora_elegida):
                            print 'Detener riego'
                            detener_riego(riego_en_ejecucion)


def comprobar_inicio_riego_criterio_medicion(id_sector, id_medicion_cabecera):
    print "Comprobando inicio de riego por medicion"



def comprobar_fin_riego_criterio_medicion(id_sector, id_medicion_cabecera):
    print "Comprobando fin de riego por medicion"



def comprobar_fin_riego_criterio_medicion(id_ejecucion_riego):
    print "Comprobando fin de riego por medicion"



def comprobar_ocurrencia_evento_medicion_interna(id_ejecucion_riego):
    print "Comprobando fin de riego por medicion"


def comprobar_ocurrencia_evento_medicion_externa(id_ejecucion_riego):
    print "Comprobando fin de riego por medicion"
