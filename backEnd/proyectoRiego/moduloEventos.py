import uuid
from django.db import models
from . import moduloSensores,moduloSeguridad

class MedicionEvento(models.Model):
    OIDMedicionEvento=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    valorMaximo=models.FloatField()
    valorMinimo=models.FloatField()

    class Meta:#CON ESTO HACEMOS Q LA CLASE SEA ABSTRACTA
        abstract=True

class MediciónFuenteInterna(models.Model,MedicionEvento):
    tipo_medicion=models.ForeignKey(moduloSensores.TipoMedicion,db_column="OIDTipoMedicion")
    #RECIBE COMO PARAMETRO A LA CLASE MEDICION EVENTO PORQUE HEREDA DE ELLA
class ConfiguracionEventoPersonalizado(models.Model):
    OIDConfiguracionEventoPersonalizado=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    idConfiguracion=models.IntegerField(unique=True)
    nombre=models.CharField(max_length=20)
    descripcion=models.CharField(max_length=100)
    notificacionActivada=models.BooleanField()
    fechaAltaConfiguracionEventoPersonalizado=models.DateField()
    fechaBajaConfiguracionEventoPersonalizado=models.DateField()
    fechaHoraCreacion=models.DateField()

    usuario_finca=models.ForeignKey(moduloSeguridad.UsuarioFinca,db_column="OIDUsuarioFinca",related_name="usuario_finca")

class EventoPersonalizadoo(models.Model):
    OIDEventoPersonalizado=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    nroEvento=models.IntegerField(unique=True)
    fechaHora=models.DateField()

    configuracion_evento_personalizado=models.ForeignKey(ConfiguracionEventoPersonalizado,db_column="OIDConfiguracionEventoPersonalizado")

