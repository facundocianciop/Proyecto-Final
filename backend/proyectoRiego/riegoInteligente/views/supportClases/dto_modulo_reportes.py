class DtoConfiguracionEventoPersonalizado():
    def __init__(self, idConfiguracionEvento, nombre, descripcion, fechaHoraCreacion, activado, numeroSector, idSector, notificacionActivada,
                 listaMedicionesExternas, listaMedicionesInterna):
        self.id_configuracion_evento = idConfiguracionEvento
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_hora_creacion = fechaHoraCreacion
        self.activado = activado
        self.numero_sector = numeroSector
        self.id_sector = idSector
        self.notificacion_activada = notificacionActivada
        self.lista_mediciones_externas = listaMedicionesExternas,
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
