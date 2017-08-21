import uuid

from django.db import models

from . import moduloSectores


class ConfiguracionRiego(models.Model):
    OIDConfiguracionRiego=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    nombre=models.CharField(max_length=20)
    descripcion=models.CharField(max_length=100)
    duracionMaxima=models.FloatField()
    fechaCreacion=models.DateField()
    fechaFinalizacion=models.DateField()

    tipo_configuracion_riego=models.ForeignKey(TipoConfiguracionRiego,db_column="OIDTipoConfiguracionRiego")


class TipoConfiguracionRiego(models.Model):
    OIDTipoConfiguracionRiego=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    idTipoConfiguracion=models.IntegerField(unique=True)
    nombre=models.CharField(max_length=20,unique=True)

class HistoricoEstadoConfiguracionRiego(models.Model):
    OIDHistoricoEstadoConfiguracionRiego=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    fechaFinEstadoConfiguracionRiego=models.DateField()
    fechaInicioEstadoConfiguracionRiego=models.DateField()

    configuracion_riego=models.ForeignKey(ConfiguracionRiego,db_column="OIDConfiguracionRiego",related_name="historico_estado_configuracion_riego_list")
    estado_configuracion_riego=models.ForeignKey(EstadoConfiguracionRiego,db_column="OIDEstadoConfiguracionRiego")

class EstadoConfiguracionRiego(models.Model):
    OIDEstadoConfiguracionRiego=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    nombreEstadoConfiguracionRiego=models.CharField(max_length=20,unique=True)
    descripcionEstadoConfiguracionRiego=models.CharField(max_length=100)

class EjecucionRiego(models.Model):
    OIDEjecucionRiego=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    cantidadAguaUtilizada=models.FloatField()
    detalle=models.CharField(max_length=100)
    duracionActual=models.FloatField()
    fechaHoraFinalizacion=models.DateField()
    fechaHoraFinalProgramada=models.DateField()
    fechaHoraInicio=models.DateField()
    fechaHoraInicioProgramada=models.DateField()

    configuracion_riego=models.ForeignKey(ConfiguracionRiego,db_column="OIDConfiguracionRiego")
    estado_ejecucion_riego=models.ForeignKey(EstadoEjecucionRiego,db_column="OIDEstadoEjecucionRiego")
    mecanismo_riego_finca_sector=models.ForeignKey(moduloSectores.MecanismoRiegoFincaSector, db_column="OIDMecanismoRiegoFincaSector", related_name="ejecucion_riego_list")

class EstadoEjecucionRiego(models.Model):
    OIDEstadoEjecucionRiego=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    nombreEstadoEjecucionRiego=models.CharField(max_length=20,unique=True)
    descripcionEstadoEjecucionRiego=models.CharField(max_length=100)

class CriterioRiego(models.Model):
    OIDCriterioRiego=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    fechaCreacionCriterio=models.DateField()
    class Meta:
        True
    #ESTO ES LO MAS IMPORTANTE HAY Q VER COMO IMPLEMENTAMOS LOS CRITERIOS INICIALES Y FINALES
    #COMO LAS RELACIONES SE MANEJAN AL REVES LO Q YO HICE FUE Q APUNTARA DOS VECSE A LA CONFIGURACION DE RIEGO
    #Y Q LA OTRA TENGA DOS ATRIBUTOS Q PARA LOS CRITERIOS INICIALES Y PARA LOS FINALES(LOS Q ESTAN EN EL related_name)
    configuracion_riego=models.ForeignKey(ConfiguracionRiego,db_column="OIDConfiguracionRiego",related_name="criterio_riego_inicio_list")
    configuracion_riego1 = models.ForeignKey(ConfiguracionRiego, db_column="OIDConfiguracionRiego", related_name="criterio_riego_final")
class CriterioRiegoPorMedicion(models.Model,CriterioRiego):
    valor=models.FloatField()

class CriterioRiegoVolumenAgua(models.Model,CriterioRiego):
    volumen=models.FloatField()

class CriterioRiegoPorHora(models.Model,CriterioRiego):
    hora=models.DateField()
    numeroDia=models.IntegerField()
