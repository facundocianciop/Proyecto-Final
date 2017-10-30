import time
from pytz import timezone

# noinspection PyUnresolvedReferences
from riegoInteligente.models import *

# noinspection PyUnresolvedReferences
from riegoInteligente.views.supportClases.views_constants import *
from riegoInteligente.views.supportClases.views_util_functions import enviar_email
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

            configuraciones_riego_habilitadas = obtener_configuraciones_riego_mecanismo_finca_sector_programados_habilitados(
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

                    elif numero_dia == datetime.now(timezone('America/Argentina/Buenos_Aires')).isocalendar()[2]:
                        if comparar_hora_riego(hora_elegida=hora_elegida):
                            print 'Iniciar riego'
                            iniciar_ejecucion_riego(mecanismo_riego_finca_sector=mecanismo_riego_finca_sector,
                                                    detalle_riego="Riego por hora",
                                                    configuracion_riego=configuracion_riego
                                                    )


def comprobar_fin_riego_criterio_hora_volumen():
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

                if configuracion_riego.tipoConfiguracionRiego.nombre == TIPO_CONFIGURACION_RIEGO_PROGRAMADO:

                    print "Comprobando configuraciones de riego: " + str(configuracion_riego)

                    # Controlar criterio hora
                    criterios_hora = obtener_criterios_fin_hora_configuracion_riego(
                        configuracion_riego.id_configuracion_riego)
                    for criterio in criterios_hora:
                        print "Comprobando criterio fin hora: " + criterio.nombre

                        hora_elegida = criterio.hora
                        numero_dia = criterio.numeroDia

                        if numero_dia == 0:
                            if comparar_hora_riego(hora_elegida=hora_elegida):
                                print 'Detener riego'
                                detener_riego(riego_en_ejecucion)

                        elif numero_dia == datetime.now(timezone('America/Argentina/Buenos_Aires')).isocalendar()[2]:
                            if comparar_hora_riego(hora_elegida=hora_elegida):
                                print 'Detener riego'
                                detener_riego(riego_en_ejecucion)

                    # Controlar criterio volumen
                    criterios_volumen = obtener_criterios_fin_volumen_configuracion_riego(
                        configuracion_riego.id_configuracion_riego)
                    for criterio in criterios_volumen:
                        print "Comprobando criterio fin volumen: " + criterio.nombre

                        cantidad_agua_utilizada = float(riego_en_ejecucion.as_json()['cantidadAguaUtilizadaLitros'])

                        print cantidad_agua_utilizada
                        if cantidad_agua_utilizada >= criterio.volumen:
                            print 'Detener riego'
                            detener_riego(riego_en_ejecucion)

                elif configuracion_riego.tipoConfiguracionRiego.nombre == TIPO_CONFIGURACION_RIEGO_AUTOMATICO:
                        if datetime.now(pytz.utc) > riego_en_ejecucion.fecha_hora_final_programada:
                            detener_riego(riego_en_ejecucion)


def procesar_medicion_sensor(oid_sector, oid_medicion_cabecera):
    print ""

    try:
        sector = Sector.objects.get(OIDSector=oid_sector)

        cabecera_medicion = MedicionCabecera.objects.get(OIDMedicionCabecera=oid_medicion_cabecera)

        detalles_medicion = MedicionDetalle.objects.filter(medicionCabecera=cabecera_medicion)

        mecanismo_riego_finca_sector_elegido = None
        mecanismos_riego_finca_sector_habilitados = obtener_mecanismos_riego_finca_sector_habilitados(
            sector.finca.idFinca)
        for mecanismo_riego_finca_sector in mecanismos_riego_finca_sector_habilitados:
            if mecanismo_riego_finca_sector.sector == sector:
                mecanismo_riego_finca_sector_elegido = mecanismo_riego_finca_sector

        for detalle in detalles_medicion:
            if mecanismo_riego_finca_sector_elegido is not None:
                comprobar_inicio_riego_criterio_medicion(mecanismo_riego_finca_sector_elegido, detalle)
                comprobar_fin_riego_criterio_medicion(mecanismo_riego_finca_sector_elegido, detalle)

            comprobar_ocurrencia_evento_medicion_interna(sector, detalle)

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned):
        return False


def comprobar_inicio_riego_criterio_medicion(mecanismo_riego_finca_sector, detalle_medicion):
    print "Comprobando inicio de riego por medicion"

    configuraciones_riego_habilitadas = obtener_configuraciones_riego_mecanismo_finca_sector_programados_habilitados(
        mecanismo_riego_finca_sector.idMecanismoRiegoFincaSector)

    riego_en_ejecucion = obtener_riego_en_ejecucion_mecanismo_riego_finca_sector(
        mecanismo_riego_finca_sector.idMecanismoRiegoFincaSector)

    for configuracion_riego in configuraciones_riego_habilitadas:
        print "Comprobando configuraciones de riego: " + str(configuracion_riego)

        if riego_en_ejecucion and riego_en_ejecucion.configuracion_riego == configuracion_riego:
            print "Riego ya se esta ejecutando para esta configuracion"
            break

        criterios_medicion = obtener_criterios_inicio_medicion_configuracion_riego(
            configuracion_riego.id_configuracion_riego)

        for criterio in criterios_medicion:
            print str(criterio)
            if criterio.tipo_medicion == detalle_medicion.tipoMedicion:
                if criterio.operador == 0:
                    if criterio.valor >= detalle_medicion.valor:
                        print 'Iniciar riego'
                        iniciar_ejecucion_riego(mecanismo_riego_finca_sector=mecanismo_riego_finca_sector,
                                                detalle_riego="Riego por medicion",
                                                configuracion_riego=configuracion_riego
                                                )

                elif criterio.operador == 1:
                    if criterio.valor <= detalle_medicion.valor:
                        print 'Iniciar riego'
                        iniciar_ejecucion_riego(mecanismo_riego_finca_sector=mecanismo_riego_finca_sector,
                                                detalle_riego="Riego por medicion",
                                                configuracion_riego=configuracion_riego
                                                )


def comprobar_fin_riego_criterio_medicion(mecanismo_riego_finca_sector, detalle_medicion):
    print "Comprobando fin de riego por medicion"

    riego_en_ejecucion = obtener_riego_en_ejecucion_mecanismo_riego_finca_sector(
        mecanismo_riego_finca_sector.idMecanismoRiegoFincaSector)

    if not riego_en_ejecucion:
        return

    configuracion_riego = riego_en_ejecucion.configuracion_riego

    if configuracion_riego:
        print "Comprobando configuraciones de riego: " + str(configuracion_riego)

        criterios_medicion = obtener_criterios_fin_medicion_configuracion_riego(
            configuracion_riego.id_configuracion_riego)

        for criterio in criterios_medicion:
            print str(criterio)
            if criterio.tipo_medicion == detalle_medicion.tipoMedicion:
                if criterio.operador == 0:
                    if criterio.valor >= detalle_medicion.valor:
                        print 'Detener riego'
                        detener_riego(riego_en_ejecucion)

                elif criterio.operador == 1:
                    if criterio.valor <= detalle_medicion.valor:
                        print 'Detener riego'
                        detener_riego(riego_en_ejecucion)


def comprobar_ocurrencia_evento_medicion_interna(sector, detalle_medicion):
    print "Comprobando fin de riego por medicion"

    lista_configuraciones_habilitadas = obtener_configuraciones_eventos_personalizados_habilitados(sector)

    for configuracion_evento in lista_configuraciones_habilitadas:

        lista_mediciones_evento_internas = MedicionFuenteInterna.objects.filter(
            configuracionEventoPersonalizado=configuracion_evento
        )
        for medicion_evento in lista_mediciones_evento_internas:
            if detalle_medicion.tipoMedicion == medicion_evento.tipoMedicion:
                if medicion_evento.valorMinimo <= detalle_medicion.valor <= medicion_evento.valorMaximo:
                    crear_suceso_evento_personalizado(sector=sector,
                                                      configuracion_evento_personalizado=configuracion_evento
                                                      )


def procesar_medicion_informacion_climatica(oid_finca, oid_medicion_informacion_climatica_cabecera):
    print "Procesando informacion climatica"
    try:

        comprobar_ocurrencia_evento_medicion_externa(oid_finca, oid_medicion_informacion_climatica_cabecera)

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned):
        return False


def comprobar_ocurrencia_evento_medicion_externa(oid_finca, oid_medicion_informacion_climatica_cabecera):
    print "Comprobando ocurrencia evento medicion externa"

    cabecera_medicion_externa = MedicionInformacionClimaticaCabecera.objects.get(
        OIDMedicionInformacionClimaticaCabecera=oid_medicion_informacion_climatica_cabecera
    )

    finca = Finca.objects.get(OIDFinca=oid_finca)
    lista_sectores = obtener_sectores_habilitados_finca(id_finca=finca.idFinca)

    for sector in lista_sectores:
        lista_configuraciones_habilitadas = obtener_configuraciones_eventos_personalizados_habilitados(sector)

        for configuracion_evento in lista_configuraciones_habilitadas:

            lista_mediciones_evento_externas = MedicionEstadoExterno.objects.filter(
                configuracionEventoPersonalizado=configuracion_evento
            )

            for medicion_evento in lista_mediciones_evento_externas:
                for detalle_medicion_externa in cabecera_medicion_externa.medicionInformacionClimaticaDetalle.all():

                    if detalle_medicion_externa.tipo_medicion_climatica == medicion_evento.tipoMedicion:

                        if medicion_evento.valorMinimo < detalle_medicion_externa.valor < medicion_evento.valorMaximo:

                            crear_suceso_evento_personalizado(
                                sector=sector,
                                configuracion_evento_personalizado=configuracion_evento
                            )


def enviar_notificacion_evento_personalizado(oid_configuracion_evento, mensaje=None):

    configuracion_evento_personalizado = ConfiguracionEventoPersonalizado.objects.get(
        OIDConfiguracionEventoPersonalizado=oid_configuracion_evento
    )

    if configuracion_evento_personalizado.notificacionActivada:
        for usuario_finca in configuracion_evento_personalizado.usuariofinca_set.all():
            email = usuario_finca.usuario.user.email
            if mensaje is not None:
                enviar_email(titulo="Notificacion Evento Personalizado", mensaje=mensaje, destino=email)
            else:
                mensaje = "Notificacion de evento: " + configuracion_evento_personalizado.nombre
                enviar_email(titulo="Notificacion Evento Personalizado", mensaje=mensaje, destino=email)
            print "email enviado"


def enviar_notificacion_riego(oid_ejecucion_riego, mensaje=None):
    ejecucion_riego = EjecucionRiego.objects.get(oid_ejecucion_riego=oid_ejecucion_riego)

    finca = ejecucion_riego.mecanismo_riego_finca_sector.sector.finca
    usuarios_finca = UsuarioFinca.objects.filter(finca=finca)

    for usuario_finca in usuarios_finca:
        email = usuario_finca.usuario.user.email

        if mensaje is not None:
            enviar_email(titulo="Notificacion Riego", mensaje=mensaje, destino=email)
        else:
            mensaje = "Notificacion Riego: " + ejecucion_riego.detalle
            enviar_email(titulo="Notificacion Riego", mensaje=mensaje, destino=email)

        print "email enviado"
