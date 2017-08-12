from django.db import models

class Sector(models.Model):
    OIDSector=models.UUIDField( primary_key=True, editable=False)
    numeroSector=models.IntegerField()
    nombreSector=models.CharField
    descripcionSector=models.CharField()
    superficie=models.FloatField()

class EstadoSector(models.Model):
    OIDEstadoSector=models.UUIDField( primary_key=True, editable=False)
    descripcionEstadoSector=models.CharField()
    nombreEstadoSector=models.CharField()

class HistoricoEstadoSector(models.Model):
    OIDHistoricoEstadoSector=models.UUIDField( primary_key=True, editable=False)
    fechaFinEstadoSector=models.DateField()
    fechaInicioEstadoSector=models.UUIDField( primary_key=True, editable=False)

    estado_sector=models.ForeignKey(EstadoSector,db_column="OIDEstadoSector")
    sector_=models.ForeignKey(Sector,db_column="OIDSector",related_name="historico_estado_secto")


class MecanismoRiegoFincaSector(models.Model):
    OIDMecanismoRiegoFincaSector=models.UUIDField( primary_key=True, editable=False)
    caudal=models.FloatField()
    presion=models.FloatField()

class HistoricoMecanismoRiegoFincaSector(models.Model):
    OIDHistoricoMecanismoRiegoFincaSector=models.UUIDField( primary_key=True, editable=False)
    fechaFinEstadoMecanismoRiegoFincaSector=models.DateField()
    fechaInicioEstadoMecanismoRiegoFincaSector=models.DateField()

    mecanismo_riego_finca_sector=models.ForeignKey(MecanismoRiegoFincaSector,db_column="OIDMecanismoRiegoFincaSector",related_name="historico_mecanismo_riego_finca_sector")
    estado_mecanismo_riego_finca_sector=models.ForeignKey(EstadoMecanismoRiegoFincaSector,db_column="OIDEstadoMecanismoRiegoFincaSector")

class EstadoMecanismoRiegoFincaSector(models.Model):
    OIDEstadoMecanismoRiegoFincaSector=models.UUIDField( primary_key=True, editable=False)
    descripcionEstadoMecanismoRiegoFincaSector=models.CharField()
    nombreEstadoMecanismoRiegoFincaSector=models.CharField()