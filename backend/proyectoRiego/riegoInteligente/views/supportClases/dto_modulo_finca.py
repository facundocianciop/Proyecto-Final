class DtoFincaRol():
    def __init__(self, nombreFinca, nombreRol, idFinca, ubicacion, estadoFinca, tamanio, idUsuarioFinca, direccionLegal):
        self.nombreFinca = nombreFinca
        self.nombreRol = nombreRol
        self.idFinca = idFinca
        self.ubicacion = ubicacion
        self.estadoFinca = estadoFinca
        self.tamanio = tamanio
        self.idUsuarioFinca = idUsuarioFinca
        self.direccionLegal = direccionLegal
    def as_json(self):
        return dict(
            nombreFinca=self.nombreFinca,
            ubicacion=self.ubicacion,
            idFinca=self.idFinca,
            nombreRol=self.nombreRol,
            tamanio=self.tamanio,
            estadoFinca=self.estadoFinca,
            idUsuarioFinca=self.idUsuarioFinca,
            direccionLegal=self.direccionLegal)


class DtoUsuarioFinca:
    def __init__(self, idUsuarioFinca, usuario, nombreUsuario, apellidoUsuario, email, imagenUsuario,
                 rol):
        self.id_usuario_finca = idUsuarioFinca
        self.usuario = usuario
        self.nombre_usuario = nombreUsuario
        self.apellido_usuario = apellidoUsuario
        self.email = email
        # self.imagen_usuario=imagenUsuario
        self.rol = rol

    def as_json(self):
        return dict(
            usuario=self.usuario,
            idUsuarioFinca=self.id_usuario_finca,
            nombre=self.nombre_usuario,
            apellido=self.apellido_usuario,
            email=self.email,
            # imagenUsuario=self.imagen_usuario,
            rol=self.rol
        )


class DtoFincaIdUsuarioFinca:
    def __init__(self, idUsuarioFinca, finca):
        self.id_usuario_finca = idUsuarioFinca
        self.finca = finca

    def as_json(self):
        return dict(

            idUsuarioFinca=self.id_usuario_finca,
            finca = self.finca)


class DtoFinca:
    def __init__(self, finca, id_usuario_finca, nombre_rol):

        self.finca = finca
        self.id_usuario_finca = id_usuario_finca
        self.nombre_rol = nombre_rol

    def as_json(self):
        return dict(
            direccionLegal=self.finca.direccionLegal,
            idFinca=self.finca.idFinca,
            nombre=self.finca.nombre,
            tamanio=self.finca.tamanio,
            ubicacion=self.finca.ubicacion,
            idUsuarioFinca=self.id_usuario_finca,
            nombreRol=self.nombre_rol
            # logoFinca=self.logoFinca
        )
