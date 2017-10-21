class DtoFincaRol():
    def __init__(self, nombreFinca, nombreRol, idFinca, ubicacion, estadoFinca, tamanio, idUsuarioFinca):
        self.nombreFinca = nombreFinca
        self.nombreRol = nombreRol
        self.idFinca = idFinca
        self.ubicacion = ubicacion
        self.estadoFinca = estadoFinca
        self.tamanio = tamanio
        self.idUsuarioFinca = idUsuarioFinca
    def as_json(self):
        return dict(
            nombreFinca=self.nombreFinca,
            ubicacion=self.ubicacion,
            idFinca=self.idFinca,
            nombreRol=self.nombreRol,
            tamanio=self.tamanio,
            estadoFinca=self.estadoFinca,
            idUsuarioFinca=self.idUsuarioFinca)


class DtoUsuarioFinca:
    def __init__(self, idUsuarioFinca, usuario, nombreUsuario, apellidoUsuario, email, imagenUsuario,
                 rol):
        self.id_usuario_finca = idUsuarioFinca
        self.usuario=usuario
        self.nombre_usuario=nombreUsuario
        self.apellido_usuario=apellidoUsuario
        self.email=email
        # self.imagen_usuario=imagenUsuario
        self.rol=rol

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
