import uuid
from django.db import models
from . import moduloFinca

class MedicionEstadoExterno(models.Model):
    #Falta Herencia
    tipo_medicion_climatica=models.ForeignKey(TipoMedicionClimatica,db_column="OIDTipoMedicionClimatica")
    pass
class TipoMedicionClimatica(models.Model):
    OIDTipoMedicionClimatica=models.UUIDField(default=uuid.uuid4,primary_key=True)
    idTipoMedicionClimatica=models.IntegerField(unique=True)
    nombreTipoMedicionClimatica=models.IntegerField(unique=True)
    tipoDato=models.CharField(max_length=10)
    fechaAltaTipoMedicionClimatica=models.DateField()
    fechaBajaTipoMedicionClimatica=models.DateField()
    habilitada=models.BooleanField()

    metodo_proveedor_informacion_climatica=models.ForeignKey(MetodoProveedorInformacionClimatica,db_column="OIDMetodoProveedorInformacionClimatica",related_name="tipo_medicion_climatica")

class MetodoProveedorInformacionClimatica(models.Model):
    OIDMetodoProveedorInformacionClimatica=models.UUIDField(default=uuid.uuid4,primary_key=True)
    nombreMetodo=models.CharField(max_length=40)
    tipoMetodo=models.CharField(max_length=10,unique=True)
    proveedor_informacion_climatica=models.ForeignKey(ProveedorInformacionClimatica,db_column="OIDProveedorInformacionClimatica",related_name="metodo_proveedor_informacion_climatica_list")

class Parametro(models.Model):
    OIDParametro=models.UUIDField(default=uuid.uuid4,primary_key=True)
    nombre=models.CharField(max_length=20)
    tipo=models.CharField(max_length=20)
    descripcion=models.CharField(max_length=100)

    metodo_proveedor_informacion_climatica=models.ForeignKey(MetodoProveedorInformacionClimatica,db_column="OIDMetodoProveedorInformacionClimatica",related_name="parametro_list")
class ProveedorInformacionClimatica(models.Model):
    OIDProveedorInformacionClimatica=models.UUIDField(default=uuid.uuid4,primary_key=True)
    nombreProveedor=models.CharField(max_length=20,unique=True)
    habilitado=models.BooleanField()
    urlAPI=models.CharField(max_length=100)
    frecuenciaMaxPosible=models.IntegerField()
    fechaAltaProveedorInfoClimatica=models.DateField()
    fechaBajaProveedorInfoClimatica=models.DateField()
    #FALTA RELACION N A N

class MediciónInformaciónClimáticaCabecera(models.Model):
    OIDMedicionInformacionClimaticaCabecera=models.UUIDField(default=uuid.uuid4,primary_key=True)
    nroMedicion=models.IntegerField(unique=True)
    fechaHora=models.DateField()

    proveedor_informacion_climatica_externa=models.ForeignKey(moduloFinca.ProveedorInformacionClimaticaFinca,db_column="OIDProveedorInformacionClimaticaFinca",related_name="medicion_informacion_climatica_cabecera_list")

class MediciónInformaciónClimáticaDetalle(models.Model):
    OIDMedicionInformacionClimaticaCabecera=models.UUIDField(default=uuid.uuid4,primary_key=True)
    nroRenglon=models.IntegerField()
    valor=models.FloatField()

    medicion_informacion_climatica_cabecera=models.ForeignKey(MediciónInformaciónClimáticaCabecera,db_column="OIDMedicionInformacionClimaticaCabecera",related_name="medicion_informacion_climatica_detalle")
    tipo_medicion_climatica=models.ForeignKey(TipoMedicionClimatica,db_column="OIDTipoMedicionClimatica")

