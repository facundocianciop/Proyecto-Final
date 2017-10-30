from views_util_functions import parsear_fecha_a_hora_arg

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
                    fechaAltaComponenteSensor=parsear_fecha_a_hora_arg(self.fechaAltaComponenteSensor),
                    fechaBajaComponenteSensor=parsear_fecha_a_hora_arg(self.fechaBajaComponenteSensor),
                    finca=self.finca.idFinca
                    )
