class DtoConfiguracionEventoPersonalizado:
    def __init__(self, idConfiguracionEvento, nombre, descripcion, fechaHoraCreacion, activado, numeroSector, idSector,
                 notificacionActivada, listaMedicionesExternas, listaMedicionesInterna):
        self.id_configuracion_evento = idConfiguracionEvento
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_hora_creacion = fechaHoraCreacion
        self.activado = activado
        self.numero_sector = numeroSector
        self.id_sector = idSector
        self.notificacion_activada = notificacionActivada
        self.lista_mediciones_externas = listaMedicionesExternas
        self.lista_mediciones_internas = listaMedicionesInterna

    def as_json(self):
        return dict(
            id_configuracion_evento=self.id_configuracion_evento,
            nombre=self.nombre,
            descripcion=self.descripcion,
            fecha_hora_creacion=self.fecha_hora_creacion,
            activado=self.activado,
            numero_sector=self.numero_sector,
            id_sector=self.id_sector,
            notificacion_activada=self.notificacion_activada,
            lista_mediciones_externas=self.lista_mediciones_externas,
            lista_mediciones_internas=self.lista_mediciones_internas)


class DtoEstadoActualSector:
    def __init__(self, idSector, numeroSector, superficieSector, descripcionSector, componenteSector, mecanismoSector,
                 ultimaMedicion, ejecucionRiego, configuracionRiego):
        self.id_sector = idSector
        self.numero_sector = numeroSector
        self.superficie_sector = superficieSector
        self.descripcion_sector = descripcionSector
        self.componente_sector = componenteSector
        self.mecanismo_sector = mecanismoSector
        self.ultima_medicion = ultimaMedicion
        self.ejecucion_riego = ejecucionRiego
        self.configuracion_riego = configuracionRiego

    def as_json(self):
        return dict(id_sector=self.id_sector,
                    numero_sector=self.numero_sector,
                    superficie_sector=self.superficie_sector,
                    descripcion_sector=self.descripcion_sector,
                    componente_sector=self.componente_sector,
                    mecanismo_sector=self.mecanismo_sector,
                    ultima_medicion=self.ultima_medicion,
                    ejecucion_riego=self.ejecucion_riego,
                    configuracion_riego=self.configuracion_riego)

class DtoRiegoEjecucionSector:
    def __init__(self, idSector, numeroSector, mecanismoSector, ejecucionRiego, configuracionRiego):
        self.id_sector = idSector
        self.numero_sector = numeroSector
        self.mecanismo_sector = mecanismoSector
        self.ejecucion_riego = ejecucionRiego
        self.configuracion_riego = configuracionRiego

    def as_json(self):
        return dict(id_sector=self.id_sector,
                    numero_sector=self.numero_sector,
                    mecanismo_sector=self.mecanismo_sector,
                    ejecucion_riego=self.ejecucion_riego,
                    configuracion_riego=self.configuracion_riego)
class DtoMedicionClimatica:
    def __init__(self, medicion_climatica):
        self.medicion_climatica = medicion_climatica

    def as_json(self):
        return dict(medicionClimatica=self.medicion_climatica)

class DtoHistoricoSector:
    def __init__(self, dto_medicion_climatica_list, dto_componente_medicion_list):
        self.dto_medicion_climatica_list = dto_medicion_climatica_list
        self.dto_componente_medicion_list = dto_componente_medicion_list

    def as_json(self):
        return dict(
            componenteMedicionListaMediciones= [dto_componente.as_json() for dto_componente in
                                                self.dto_componente_medicion_list],
        medicionClimaticaList= [dto_medicion_climatica.as_json() for dto_medicion_climatica in self.dto_medicion_climatica_list]
        )


class DtoComponenteMedicion:
    def __init__(self, componente, medicion_cabecera):
        self.componente = componente
        self.medicion_cabecera = medicion_cabecera

    def as_json(self):
        return dict(
                    componente=self.componente,
                    medicionCabecera=self.medicion_cabecera
                )


class DtoMecanismoRiegoConfiguracion:
    def __init__(self, mecanismo_riego_finca_sector, ejecucion, configuracion):
        self.mecanismo_riego_finca_sector = mecanismo_riego_finca_sector
        self.ejecucion = ejecucion
        self.configuracion = configuracion

    def as_json(self):
        return dict(
            mecanismo_riego_finca_sector=self.mecanismo_riego_finca_sector,
            ejecucion=self.ejecucion,
            configuracion=self.configuracion
        )


class DtoMedicionCruzadaRiego:
    def __init__(self, mecanismo_riego_finca_sector, ejecucion, configuracion, lista_mediciones_componente,
                 lista_mediciones_climaticas_antes, lista_mediciones_climaticas_despues):
        self.mecanismo_riego_finca_sector = mecanismo_riego_finca_sector
        self.ejecucion = ejecucion
        self.configuracion = configuracion
        self.lista_mediciones_componente = lista_mediciones_componente
        self.lista_mediciones_climaticas_antes = lista_mediciones_climaticas_antes
        self.lista_mediciones_climaticas_despues = lista_mediciones_climaticas_despues


    def as_json(self):
        return dict(
            mecanismo_riego_finca_sector=self.mecanismo_riego_finca_sector,
            ejecucion=self.ejecucion,
            configuracion=self.configuracion,
            listaMedicionesComponente=[medicion.as_json() for medicion in self.lista_mediciones_componente],
            listaMedicionesClimaticasAntes=[medicion_antes.as_json() for medicion_antes in self.lista_mediciones_climaticas_antes],
            listaMedicionClimaticasDespues=[medicion_despues.as_json() for medicion_despues in self.lista_mediciones_climaticas_despues]
        )
