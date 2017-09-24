class DtoTipoSubtipo() :
    def __init__(self, nombreSubtipo, nombreTipo):
        self.nombreSubtipo = nombreSubtipo
        self.nombreTipo = nombreTipo


    def as_json(self):
        return dict(
            nombreSubtipo=self.nombreSubtipo,
            nombreTipo=self.nombreTipo)
