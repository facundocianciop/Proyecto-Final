import time

from riegoInteligente.models import *
from riegoInteligente.views.supportClases.views_constants import *
from riegoInteligente.views.supportClases.informacionClimatica.informacionClimatica import \
    obtener_mediciones_climaticas_finca

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

            criterios_hora = obtener_criterios_inicio_hora_configuracion_riego(
                mecanismo_riego_finca_sector.idMecanismoRiegoFincaSector)


def comprobar_fin_riego_criterio_hora():
    print "Comprobando fin de riegos por hora"

    fincas_habilitadas = obtener_fincas_habilitadas()


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
