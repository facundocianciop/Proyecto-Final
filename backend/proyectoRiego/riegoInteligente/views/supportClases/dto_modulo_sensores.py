class DtoComponenteSensorFinca():
    def __init__(self, idComponenteSensor, modelo, descripcion, finca, fechaAltaComponenteSensor,
                 fechaBajaComponenteSensor, estado):
        self.idComponenteSensor = idComponenteSensor
        self.modelo = modelo
        self.descripcion = descripcion
        self.finca = finca
        self.fechaAltaComponenteSensor = fechaAltaComponenteSensor
        self.fechaBajaComponenteSensor = fechaBajaComponenteSensor
        self.estado = estado


    def as_json(self):
        return dict(idComponenteSensor=self.idComponenteSensor,
                    modelo=self.modelo,
                    descripcion=self.descripcion,
                    estado=self.estado,
                    fechaAltaComponenteSensor=self.fechaAltaComponenteSensor,
                    fechaBajaComponenteSensor=self.fechaBajaComponenteSensor,
                    finca=self.finca.idFinca)