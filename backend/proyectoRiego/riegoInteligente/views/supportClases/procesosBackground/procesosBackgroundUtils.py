from riegoInteligente.models import *
from riegoInteligente.views.supportClases.views_constants import *

# noinspection PyUnresolvedReferences
from django.db import IntegrityError, DataError, DatabaseError
from django.core.exceptions import ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned


def obtener_fincas_habilitadas():

    try:

        estado_finca_habilitado = EstadoFinca.objects.get(nombreEstadoFinca=ESTADO_HABILITADO)
        historicos_habilitados = HistoricoEstadoFinca.objects.filter(estadoFinca=estado_finca_habilitado,
                                                                     fechaFinEstadoFinca__isnull=True)
        fincas_habilitadas = []
        for historico in historicos_habilitados:
            fincas_habilitadas.append(historico.finca)

        return fincas_habilitadas

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned):
        return []


def obtener_sectores_habilitados_finca(id_finca):

    try:
        finca = Finca.objects.get(idFinca=id_finca)

        estado_sector_habilitado = EstadoSector.objects.get(nombreEstadoSector=ESTADO_HABILITADO)

        sectores_habilitados = []

        sectores_finca = Sector.objects.filter(finca=finca)
        for sector in sectores_finca:
            try:
                historico_sector_habilitado = HistoricoEstadoSector.objects.get(
                    sector=sector,
                    estado_sector=estado_sector_habilitado,
                    fechaFinEstadoSector__isnull=True
                )

                if historico_sector_habilitado:
                    sectores_habilitados.append(sector)

            except (ObjectDoesNotExist, EmptyResultSet):
                pass

        return sectores_habilitados

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned):
        return []


def obtener_mecanismo_riego_finca_habilitados_finca(id_finca):

    try:
        finca = Finca.objects.get(idFinca=id_finca)

        estado_mecanismo_riego_finca_habilitado = EstadoMecanismoRiegoFinca.objects.get(
            nombreEstadoMecanismoRiegoFinca=ESTADO_HABILITADO)

        mecanismos_riego_finca_habilitados = []

        mecanismos_riego_finca = MecanismoRiegoFinca.objects.filter(finca=finca)
        for mecanismo_riego_finca in mecanismos_riego_finca:
            try:
                historico_mecanismo_riego_finca_habilitado = \
                    HistoricoMecanismoRiegoFinca.objects.get(
                        mecanismo_riego_finca=mecanismo_riego_finca,
                        estado_mecanismo_riego_finca=estado_mecanismo_riego_finca_habilitado,
                        fechaFinEstadoMecanismoRiegoFinca__isnull=True
                    )

                if historico_mecanismo_riego_finca_habilitado:
                    mecanismos_riego_finca_habilitados.append(mecanismo_riego_finca)

            except (ObjectDoesNotExist, EmptyResultSet):
                pass

        return mecanismos_riego_finca_habilitados

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned):
        return []


def comprobar_mecanismo_riego_finca_habilitado(mecanismo_riego_finca_sector):

    try:
        estado_mecanismo_riego_finca_habilitado = EstadoMecanismoRiegoFinca.objects.get(
            nombreEstadoMecanismoRiegoFinca=ESTADO_HABILITADO)

        mecanismo_riego_finca = mecanismo_riego_finca_sector.mecanismoRiegoFinca

        historico_mecanismo_riego_finca_habilitado = \
            HistoricoMecanismoRiegoFinca.objects.get(
                mecanismo_riego_finca=mecanismo_riego_finca,
                estado_mecanismo_riego_finca=estado_mecanismo_riego_finca_habilitado,
                fechaFinEstadoMecanismoRiegoFinca__isnull=True
            )

        if historico_mecanismo_riego_finca_habilitado:
            return True
        else:
            return False

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned):
        return False


def obtener_mecanismos_riego_finca_sector_habilitados(id_finca):
    try:
        estado_mecanismo_riego_finca_sector_habilitado = \
            EstadoMecanismoRiegoFincaSector.objects.get(nombreEstadoMecanismoRiegoFincaSector=ESTADO_HABILITADO)

        mecanismos_riego_finca_sector_habilitados = []

        sectores_habilitados = obtener_sectores_habilitados_finca(id_finca)
        for sector_habilitado in sectores_habilitados:
            try:
                mecanismos_riego_finca_sector = MecanismoRiegoFincaSector.objects.filter(sector=sector_habilitado)

                for mecanismo_riego_finca_sector in mecanismos_riego_finca_sector:

                    if not comprobar_mecanismo_riego_finca_habilitado(mecanismo_riego_finca_sector):
                        continue

                    historico_mecanismo_riego_finca_sector_habilitado = \
                        HistoricoMecanismoRiegoFincaSector.objects.filter(
                            mecanismo_riego_finca_sector=mecanismo_riego_finca_sector,
                            estado_mecanismo_riego_finca_sector=estado_mecanismo_riego_finca_sector_habilitado,
                            fechaFinEstadoMecanismoRiegoFincaSector__isnull=True
                        )
                    if historico_mecanismo_riego_finca_sector_habilitado:
                        mecanismos_riego_finca_sector_habilitados.append(mecanismo_riego_finca_sector)

            except (ObjectDoesNotExist, EmptyResultSet):
                pass

        return mecanismos_riego_finca_sector_habilitados

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned):
        return []


def obtener_riego_en_ejecucion_mecanismo_riego_finca_sector(id_mecanismo_riego_finca_sector):
    try:
        mecanismo_riego_finca_sector = MecanismoRiegoFincaSector.objects.get(
            idMecanismoRiegoFincaSector=id_mecanismo_riego_finca_sector)

        estado_ejecucion_riego_en_ejecucion = EstadoEjecucionRiego.objects.get(
            nombreEstadoEjecucionRiego=ESTADO_EN_EJECUCION)
        estado_ejecucion_riego_pausado = EstadoEjecucionRiego.objects.get(
            nombreEstadoEjecucionRiego=ESTADO_PAUSADO)

        ejecucion_riego_actual = EjecucionRiego.objects.filter(
            mecanismo_riego_finca_sector=mecanismo_riego_finca_sector
        ).order_by('-fecha_hora_inicio').first()

        if ejecucion_riego_actual.estado_ejecucion_riego == estado_ejecucion_riego_pausado \
                or ejecucion_riego_actual.estado_ejecucion_riego == estado_ejecucion_riego_en_ejecucion:
            return ejecucion_riego_actual
        else:
            return None

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned):
        return None


def obtener_configuraciones_riego_mecanismo_finca_sector_habilitados(id_mecanismo_riego_finca_sector):
    try:
        mecanismo_riego_finca_sector = MecanismoRiegoFincaSector.objects.get(
            idMecanismoRiegoFincaSector=id_mecanismo_riego_finca_sector)

        estado_configuracion_riego_habilitado = EstadoConfiguracionRiego.objects.get(
            nombreEstadoConfiguracionRiego=ESTADO_HABILITADO
        )

        configuraciones_riego_habilitadas = []

        configuraciones_riego_mecanismo = ConfiguracionRiego.objects.filter(
            mecanismoRiegoFincaSector=mecanismo_riego_finca_sector,
            fechaFinalizacion__isnull=True
        )
        for configuracion_riego in configuraciones_riego_mecanismo:
            try:
                criterios_iniciales = CriterioRiego.objects.filter(configuracionRiegoInicial=configuracion_riego,
                                                                   fecha_eliminacion_criterio__isnull=True)
                criterios_finales = CriterioRiego.objects.filter(configuracionRiegoFinal=configuracion_riego,
                                                                 fecha_eliminacion_criterio__isnull=True)

                if criterios_iniciales.__len__() != 0 and criterios_finales.__len__() != 0:

                    historico_configuracion_riego_habilitado = HistoricoEstadoConfiguracionRiego.objects.get(
                        configuracion_riego=configuracion_riego,
                        estado_configuracion_riego=estado_configuracion_riego_habilitado,
                        fechaFinEstadoConfiguracionRiego__isnull=True
                    )

                    if historico_configuracion_riego_habilitado:
                        configuraciones_riego_habilitadas.append(configuracion_riego)

            except (ObjectDoesNotExist, EmptyResultSet):
                pass

        return configuraciones_riego_habilitadas

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned):
        return []


def obtener_criterios_inicio_medicion_configuracion_riego(id_configuracion_riego):

    criterios_medicion = []

    try:
        configuracion_riego = ConfiguracionRiego.objects.get(id_configuracion_riego=id_configuracion_riego)

        criterios = CriterioRiego.objects.filter(
            configuracionRiegoInicial=configuracion_riego,
            fecha_eliminacion_criterio__isnull=True
        ).select_subclasses()
        for criterio in criterios:
            if isinstance(criterio, CriterioRiegoPorMedicion):
                criterios_medicion.append(criterio)

        return criterios_medicion

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned):
        return criterios_medicion


def obtener_criterios_inicio_hora_configuracion_riego(id_configuracion_riego):
    criterios_hora = []

    try:
        configuracion_riego = ConfiguracionRiego.objects.get(id_configuracion_riego=id_configuracion_riego)

        criterios = CriterioRiego.objects.filter(
            configuracionRiegoInicial=configuracion_riego,
            fecha_eliminacion_criterio__isnull=True
        ).select_subclasses()
        for criterio in criterios:
            if isinstance(criterio, CriterioRiegoPorHora):
                criterios_hora.append(criterio)

        return criterios_hora

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned):
        return criterios_hora


def obtener_criterios_fin_medicion_configuracion_riego(id_configuracion_riego):
    criterios_medicion = []

    try:
        configuracion_riego = ConfiguracionRiego.objects.get(id_configuracion_riego=id_configuracion_riego)

        criterios = CriterioRiego.objects.filter(
            configuracionRiegoFinal=configuracion_riego,
            fecha_eliminacion_criterio__isnull=True
        ).select_subclasses()
        for criterio in criterios:
            if isinstance(criterio, CriterioRiegoPorMedicion):
                criterios_medicion.append(criterio)

        return criterios_medicion

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned):
        return criterios_medicion


def obtener_criterios_fin_hora_configuracion_riego(id_configuracion_riego):
    criterios_hora = []

    try:
        configuracion_riego = ConfiguracionRiego.objects.get(id_configuracion_riego=id_configuracion_riego)

        criterios = CriterioRiego.objects.filter(
            configuracionRiegoFinal=configuracion_riego,
            fecha_eliminacion_criterio__isnull=True
        ).select_subclasses()
        for criterio in criterios:
            if isinstance(criterio, CriterioRiegoPorHora):
                criterios_hora.append(criterio)

        return criterios_hora

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned):
        return criterios_hora


def obtener_criterios_fin_volumen_configuracion_riego(id_configuracion_riego):
    criterios_volumen = []

    try:
        configuracion_riego = ConfiguracionRiego.objects.get(id_configuracion_riego=id_configuracion_riego)

        criterios = CriterioRiego.objects.filter(
            configuracionRiegoFinal=configuracion_riego,
            fecha_eliminacion_criterio__isnull=True
        ).select_subclasses()
        for criterio in criterios:
            if isinstance(criterio, CriterioRiegoVolumenAgua):
                criterios_volumen.append(criterio)

        return criterios_volumen

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned):
        return criterios_volumen


# noinspection PyBroadException
def comparar_hora_riego(hora_elegida):

    try:
        ahora = datetime.now(pytz.utc)
        hora = ahora.replace(hour=hora_elegida.hour,
                             minute=hora_elegida.minute,
                             second=hora_elegida.second
                             )

        diferencia_hora = datetime.now(pytz.utc) - hora

        print diferencia_hora.seconds

        if diferencia_hora.seconds < 5:
            return True
        else:
            return False

    except Exception:
        return False


def obtener_configuraciones_eventos_personalizados_habilitados(sector):

    try:
        configuraciones_eventos_personalizados = ConfiguracionEventoPersonalizado. \
            objects.filter(
                           fechaBajaConfiguracionEventoPersonalizado__isnull=True
                           )

        configuraciones_eventos_personalizados_habilitados = []

        for configuracion_evento in configuraciones_eventos_personalizados:
            for sector_configuracion in configuracion_evento.sectorList.all():
                if sector_configuracion == sector:
                    configuraciones_eventos_personalizados_habilitados.append(configuracion_evento)

        return configuraciones_eventos_personalizados_habilitados

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned):
        return None


def crear_suceso_evento_personalizado(sector, configuracion_evento_personalizado):

    try:
        evento_personalizado = EventoPersonalizado(
            sector=sector,
            configuracion_evento_personalizado=configuracion_evento_personalizado,
            fechaHora=datetime.now(pytz.utc)
        )
        evento_personalizado.save()

        return evento_personalizado

    except (ObjectDoesNotExist, EmptyResultSet, MultipleObjectsReturned):
        return None
