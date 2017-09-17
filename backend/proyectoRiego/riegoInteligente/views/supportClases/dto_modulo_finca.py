class DtoFincaRol():
    def __init__(self, nombreFinca, nombreRol, idFinca):
        self.nombreFinca = nombreFinca
        self.nombreRol = nombreRol
        self.idFinca = idFinca

    def as_json(self):
        return dict(
            nombreFinca=self.nombreFinca,
            idFinca=self.idFinca,
            nombreRol=self.nombreRol)


class DtoUsuarioFinca:
    def __init__(self, OIDUsuarioFinca, usuario, nombreUsuario, apellidoUsuario, email, imagenUsuario,
                 rol):
        self.OID_usuario_finca=OIDUsuarioFinca
        self.usuario=usuario
        self.nombre_usuario=nombreUsuario
        self.apellido_usuario=apellidoUsuario
        self.email=email
        # self.imagen_usuario=imagenUsuario
        self.rol=rol

    def as_json(self):
        return dict(
            OIDUsuarioFinca=self.OID_usuario_finca,
            nombreUsuario=self.nombre_usuario,
            apellidoUsuario=self.apellido_usuario,
            email=self.email,
            # imagenUsuario=self.imagen_usuario,
            rol=self.rol
        )
