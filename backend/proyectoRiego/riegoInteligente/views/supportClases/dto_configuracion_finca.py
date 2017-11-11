from views_constants import *
from views_util_functions import parsear_fecha_a_hora_arg


class DtoMecanismoRiegoFinca():
    def __init__(self, habilitado, direccionIP, fechaInstalacion, idMecanismoRiegoFinca, tipoMecanismoRiego,
                 caudalMaximo, presionMaxima):
        if habilitado == ESTADO_HABILITADO:
            self.habilitado = True
        else:
            self.habilitado = False
        self.direccionIP = direccionIP
        self.fechaInstalacion = fechaInstalacion
        self.idMecanismoRiegoFinca = idMecanismoRiegoFinca
        self.tipoMecanismoRiego = tipoMecanismoRiego
        self.caudalMaximo = caudalMaximo
        self.presionMaxima = presionMaxima

    def as_json(self):
        return dict(
            direccionIP=self.direccionIP,
            fechaInstalacion=parsear_fecha_a_hora_arg(self.fechaInstalacion),
            idMecanismoRiegoFinca=self.idMecanismoRiegoFinca,
            tipoMecanismoRiego=self.tipoMecanismoRiego,
            habilitado=self.habilitado,
            presionMaxima=self.presionMaxima,
            caudalMaximo=self.caudalMaximo)
