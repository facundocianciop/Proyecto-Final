import uuid
from django.db import models
from . import moduloInformacionExterna

class Finca(models.Model):
    OIDFinca=models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    direcciónLegal=models.CharField(max_length=50)
    idFinca=models.IntegerField()
    logoFinca=models.ImageField()
    nombre=models.CharField(max_length=50)
    tamanio=models.FloatField()
    ubicacion=models.CharField(max_length=50)

    proveedor_informacion_climatica_finca=models.ForeignKey(ProveedorInformacionClimaticaFinca,db_column="OIDProveedorInformacionClimaticaFinca",related_name="finca")

class HistoricoEstadoFinca(models.Model):
    OIDHistoricoEstadoFinca = models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    fechaFinEstadoFinca=models.DateField()
    fechaInicioEstadoFinca=models.DateField()

    finca=models.ForeignKey(Finca,db_column="OIDFinca",related_name="historico_estado_finca")
    estado_finca=models.ForeignKey(EstadoFinca,db_column="OIDEstadoFinca")
class EstadoFinca(models.Model):
    OIDFinca = models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    descripcionEstadoFinca=models.CharField(max_length=100)
    nombreEstadoFinca=models.CharField(max_length=15)

class MecanismoRiegoFinca(models.Model):
    OIDFinca = models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    direccionIP=models.CharField(max_length=20)
    fechaInstalacion=models.DateField()
    idFincaMecanismoRiego=models.IntegerField()

    finca=models.ForeignKey(Finca,db_column="OIDFinca")

class HistoricoMecanismoRiegoFinca(models.Model):
    OIDHistoricoMecanismoRiegoFinca =models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    mecanismo_riego_finca=models.ForeignKey(MecanismoRiegoFinca,db_column="OIDMecanismoRiegoFinca",related_name="historico_mecanismo_riego_finca")
    estado_mecanismo_riego_finca=models.ForeignKey(EstadoMecanismoRiegoFinca,db_column="OIDEstadoMecanismoRiegoFinca")

class EstadoMecanismoRiegoFinca(models.Model):
    OIDEstadoMecanismoRiegoFinca = models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    nombreEstadoMecanismoRiegoFincaSector=models.CharField(max_length=20)
    descripcionEstadoMecanismoRiegoFincaSector=models.CharField(max_length=100)

class ProveedorInformacionClimaticaFinca(models.Model):
    OIDProveedorInformacionClimaticaFinca = models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    fechaAltaProveedorInfoClimaticaFinca=models.DateField()
    fechaBajaProveedorInfoClimaticaFinca=models.DateField()
    frecuencia=models.IntegerField()
