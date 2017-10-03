class DtoProveedorFinca():
    def __init__(self, nombre_proveedor, frecuencia_maxima_posible, frecuencia_actual, fecha_alta_proveedor_finca,
                 lista_tipo_medicion, url_api):
        self.nombre_proveedor = nombre_proveedor
        self.frecuencia_maxima_posible = frecuencia_maxima_posible
        self.frecuencia_actual = frecuencia_actual
        self.fecha_alta_proveedor_finca = fecha_alta_proveedor_finca
        self.lista_tipo_medicion = lista_tipo_medicion
        self.url_api = url_api


    def as_json(self):
        return dict(nombreProveedor=self.nombre_proveedor,
                    frecuenciaMaximaPosible=self.frecuencia_maxima_posible,
                    frecuenciaActual=self.frecuencia_actual,
                    fechaAltaProveedorFinca=self.fecha_alta_proveedor_finca,
                    urlApi=self.url_api,
                    listaTipoMedicion=self.lista_tipo_medicion)


