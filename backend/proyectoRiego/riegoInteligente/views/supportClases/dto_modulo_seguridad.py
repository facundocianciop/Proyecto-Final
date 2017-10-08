
class DtoRecuperarCuentaUsuario:
    def __init__(self, usuario, email):
        self.usuario = usuario
        self.email = email

    def as_json(self):
        return dict(
            KEY_USUARIO=self.usuario,
            KEY_EMAIL=self.email
        )
