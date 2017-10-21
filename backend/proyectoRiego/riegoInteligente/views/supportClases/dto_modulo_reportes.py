class DtoConfiguracionEventoPersonalizado:
    def __init__(self, idConfiguracionEvento, nombre, descripcion, fechaHoraCreacion, activado, numeroSector, idSector,
                 notificacionActivada, listaMedicionesExternas, listaMedicionesInterna, usuarioFincaId):
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
        self.id_usuario_finca = usuarioFincaId

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
            lista_mediciones_internas=self.lista_mediciones_internas,
            id_usuario_finca=self.id_usuario_finca)


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
    def __init__(self, mecanismo_riego_finca_sector, ejecucion, configuracion, mediciones_componente_antes,
                mediciones_componente_despues, mediciones_climaticas_antes):
        self.mecanismo_riego_finca_sector = mecanismo_riego_finca_sector
        self.ejecucion = ejecucion
        self.configuracion = configuracion
        self.mediciones_componente_antes = mediciones_componente_antes
        self.mediciones_componente_despues = mediciones_componente_despues
        self.mediciones_climaticas_antes = mediciones_climaticas_antes


    def as_json(self):
        return dict(
            mecanismo_riego_finca_sector=self.mecanismo_riego_finca_sector.as_json(),
            ejecucion=self.ejecucion.as_json(),
            configuracion=self.configuracion.as_json(),
            medicionesComponenteAntes=self.mediciones_componente_antes.as_json(),
            medicionesComponenteDespues=self.mediciones_componente_despues.as_json(),
            medicionesClimaticasAntes=self.mediciones_climaticas_antes.as_json()
        )
