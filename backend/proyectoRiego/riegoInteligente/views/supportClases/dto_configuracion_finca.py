from views_constants import *
class DtoMecanismoRiegoFinca():
    def __init__(self, habilitado, direccionIP, fechaInstalacion, idMecanismoRiegoFinca, tipoMecanismoRiego):
        if habilitado == ESTADO_HABILITADO:
            self.habilitado = True
        else:
            self.habilitado = False
        self.direccionIP = direccionIP
        self.fechaInstalacion = fechaInstalacion
        self.idMecanismoRiegoFinca = idMecanismoRiegoFinca
        self.tipoMecanismoRiego = tipoMecanismoRiego


    def as_json(self):
        return dict(
            direccionIP=self.direccionIP,
            fechaInstalacion=self.fechaInstalacion,
            idMecanismoRiegoFinca=self.idMecanismoRiegoFinca,
            tipoMecanismoRiego=self.tipoMecanismoRiego,
            habilitado=self.habilitado)
