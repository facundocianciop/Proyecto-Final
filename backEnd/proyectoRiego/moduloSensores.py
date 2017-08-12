import uuid
from django.db import models
from . import moduloFinca,moduloSectores

class Sensor(models.Model):
    OIDSensor=models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    idSensor=models.IntegerField()
    fechaAltaSensor=models.DateField()
    fechaBajaSensor=models.DateField()
    habilitado=models.BooleanField()
    modelo=models.CharField(max_length=20)

    componente_sensor=models.ForeignKey(ComponenteSensor,db_column="OIDComponenteSensor",related_name="sensor")
    sensor_tipo_Interna=models.ForeignKey(TipoMedicion,db_column="OIDTipoMedicion")
    finca=models.ForeignKey(moduloFinca.Finca,db_column="OIDFinca")

class TipoMedicion(models.Model):
    OIDTipoMedicion=models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    idTipoMedicion=models.IntegerField()
    nombreTipoMedicion=models.CharField(max_length=20)
    unidadMedicion = models.CharField(max_length=20)
    habilitado=models.BooleanField()
    fechaAltaTipoMedicion=models.DateField()
    fechaBajaTipoMedicion=models.DateField()

class ComponenteSensor(models.Model):
    OIDComponenteSensor=models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    numeroComponente=models.IntegerField()
    habilitado=models.BooleanField()
    fechaAltaComponenteSensor=models.DateField()
    fechaBajaComponenteSensor=models.DateField()

class ComponenteSensorSector(models.Model):
    OIDComponenteSensorSector=models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    idComponenteSensores=models.IntegerField()

    componente_sensor=models.ForeignKey(moduloSectores.Sector,db_column="OIDSector")
class HistoricoComponenteSensorSector(models.Model):
    OIDHistoricoComponenteSensorSector=models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    fechaAltaComponenteSensorSector=models.DateField()
    fechaBajaComponenteSensorSecto=models.DateField()
    componenteSensorSector_=models.ForeignKey(ComponenteSensorSector,db_column="OIDComponenteSensorSector",related_name="historico_componente_sensor_sector")

class EstadoComponenteSensorSector(models.Model):
    models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombreEstadoSensorSector=models.CharField()
    descripcionEstadoSensorSector=models.CharField()

class TipoMedicion(models.Model):
    OIDTipoMedicion=models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    idTipoMedicion=models.IntegerField()
    nombreTipoMedicion=models.CharField()
    unidadMedicion=models.CharField()
    fechaAltaTipoMedicion=models.DateField()
    fechaBajaTipoMedicion=models.DateField()

class MedicionCabecera(models.Model):
    OIDMedicionCabecera=models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    fechaYHora=models.DateField()
    nroMedicion=models.IntegerField()

class MedicionDetalle(models.Model):
    OIDMedicionDetalle=models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    nroRenglon=models.IntegerField()
    valor=models.FloatField()
    medicionCabecera=models.ForeignKey(MedicionCabecera,db_column="OIDMedicionCabecera",related_name="medicion_detalle")

class MedicionFuenteInterna(models.Model):
    #falta la herencia