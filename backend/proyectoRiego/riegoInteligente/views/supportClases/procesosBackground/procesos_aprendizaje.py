from datetime import timedelta

from procesosBackgroundUtils import *
from riegoInteligente.aprendizaje.redNeuronal import evaluarNuevaMedicion, llenarDatasetNuevosDatos, principal
from riegoInteligente.views.supportClases.configuracion_riego_util_functions import *


def proceso_actualizar_data_set():
    print "Actualizar data set"
    llenarDatasetNuevosDatos()
    principal()


def proceso_controlar_ejecucion_riego_por_aprendizaje():
    print "Comprobar ejecucuion de riego por aprendizaje"

    try:
        fincas_habilitadas = obtener_fincas_habilitadas()

        for finca in fincas_habilitadas:
            mecanismos_riego_finca_sector_habilitados = obtener_mecanismos_riego_finca_sector_habilitados(finca.idFinca)
            for mecanismo_riego_finca_sector in mecanismos_riego_finca_sector_habilitados:
                print "Comprobando configuraciones de riego de: " + str(mecanismo_riego_finca_sector)

                configuraciones_automaticas = obtener_configuraciones_riego_automaticas_habilitadas(
                    mecanismo_riego_finca_sector.idMecanismoRiegoFincaSector
                )

                if configuraciones_automaticas.__len__() >= 0:

                    sector = mecanismo_riego_finca_sector.sector

                    componentes_sensor_habilitados = obtener_componentes_sensor_sector_habiltiados(sector)

                    ultima_medicion_cabecera_sector = obtener_ultima_medicion_cabecera(componentes_sensor_habilitados)

                    temperatura_a = 20
                    temperatura_s = 10
                    humedad_a = 60
                    humedad_s = 60
                    radiacion_solar = 3000

                    if ultima_medicion_cabecera_sector:

                        tipo_medicion_temperatura_a = TipoMedicion.objects.get(
                            nombreTipoMedicion=TIPO_MEDICION_TEMPERATURA_AIRE)
                        medicion_temperatura_a = MedicionDetalle.objects.get(
                            medicionCabecera=ultima_medicion_cabecera_sector,
                            tipoMedicion=tipo_medicion_temperatura_a
                        )
                        temperatura_a = medicion_temperatura_a.valor

                        tipo_medicion_temperatura_s = TipoMedicion.objects.get(
                            nombreTipoMedicion=TIPO_MEDICION_TEMPERATURA_SUELO)
                        medicion_temperatura_s = MedicionDetalle.objects.get(
                            medicionCabecera=ultima_medicion_cabecera_sector,
                            tipoMedicion=tipo_medicion_temperatura_s
                        )
                        temperatura_s = medicion_temperatura_s.valor

                        tipo_medicion_humedad_a = TipoMedicion.objects.get(
                            nombreTipoMedicion=TIPO_MEDICION_HUMEDAD_AIRE)
                        medicion_humedad_a = MedicionDetalle.objects.get(
                            medicionCabecera=ultima_medicion_cabecera_sector,
                            tipoMedicion=tipo_medicion_humedad_a
                        )
                        humedad_a = medicion_humedad_a.valor

                        tipo_medicion_humedad_s = TipoMedicion.objects.get(
                            nombreTipoMedicion=TIPO_MEDICION_HUMEDAD_SUELO)
                        medicion_humedad_s = MedicionDetalle.objects.get(
                            medicionCabecera=ultima_medicion_cabecera_sector,
                            tipoMedicion=tipo_medicion_humedad_s
                        )
                        humedad_s = medicion_humedad_s.valor

                        tipo_medicion_radiacion_solar = TipoMedicion.objects.get(
                            nombreTipoMedicion=TIPO_MEDICION_RADIACION_SOLAR)
                        medicion_radiacion_solar = MedicionDetalle.objects.get(
                            medicionCabecera=ultima_medicion_cabecera_sector,
                            tipoMedicion=tipo_medicion_radiacion_solar
                        )
                        radiacion_solar = medicion_radiacion_solar.valor

                    ultima_medicion_climatica = obtener_ultima_cabecera_informacion_climatica(sector)

                    presion = 800
                    precipitacion = 0

                    if ultima_medicion_cabecera_sector:
                        tipo_medicion_presion = TipoMedicionClimatica.objects.get(
                            nombreTipoMedicionClimatica=TIPO_MEDICION_CLIMATICA_PRESION)

                        medicion_climatica_presion = MedicionInformacionClimaticaDetalle.objects.get(
                            tipo_medicion_climatica=tipo_medicion_presion,
                            medicion_informacion_climatica_cabecera=ultima_medicion_climatica
                        )
                        presion = medicion_climatica_presion.valor

                        tipo_medicion_precipitacion = TipoMedicionClimatica.objects.get(
                            nombreTipoMedicionClimatica=TIPO_MEDICION_CLIMATICA_PRECIPITACION)
                        medicion_climatica_precipitacion = MedicionInformacionClimaticaDetalle.objects.get(
                            tipo_medicion_climatica=tipo_medicion_precipitacion,
                            medicion_informacion_climatica_cabecera=ultima_medicion_climatica
                        )
                        precipitacion = medicion_climatica_precipitacion.valor

                    cultivo = obtener_cultivo_sector_habilitado(sector)

                    for configuracion in configuraciones_automaticas:

                        cantidad_agua_a_regar = evaluarNuevaMedicion(
                            mes=datetime.now().month,
                            dia=datetime.now().day,
                            cultivo=cultivo.idCultivo,
                            mecanismo=mecanismo_riego_finca_sector.idMecanismoRiegoFincaSector,
                            ppe=precipitacion,
                            presionA=presion,
                            tempA=temperatura_a,
                            humA=humedad_a,
                            radiacionS=radiacion_solar,
                            tempS=temperatura_s,
                            humS=humedad_s
                        )

                        print cantidad_agua_a_regar
                        if cantidad_agua_a_regar > 0:
                            minutos_a_regar = cantidad_agua_a_regar/mecanismo_riego_finca_sector.caudal

                            fecha_fin_riego = datetime.now(pytz.utc) + timedelta(minutes=minutos_a_regar)
                            iniciar_ejecucion_riego(
                                mecanismo_riego_finca_sector=mecanismo_riego_finca_sector,
                                detalle_riego="Riego automatico",
                                configuracion_riego=configuracion,
                                fecha_fin_programada=fecha_fin_riego
                            )

    except Exception as err:
        print "Error controlando ejecucion por aprendizaje " + err.message
