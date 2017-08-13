import uuid
from django.db import models
from . import moduloSectores
class Cultivo(models.Model):
    OIDCultivo=models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    descripcion=models.CharField(max_length=100)
    nombre=models.CharField(max_length=20)
    fechaPlantacion=models.DateField()
    fechaEliminacion=models.DateField()
    habilitado=models.BooleanField()

    subtipo_cultivo=models.ForeignKey(SubtipoCultivo,db_column="OIDSubtipoCultivo")
sector_=models.ForeignKey(moduloSectores.Sector,db_column="OIDSector")

class SubtipoCultivo(models.Model):
    OIDSubtipoCultivo=models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    idSubtipo=models.IntegerField(unique=True)
    nombreSubtipo=models.CharField(max_length=20)
    habilitado=models.BooleanField()
    descripcion=models.CharField(max_length=100)
    fechaAltaSubtipoCultivo=models.DateField()
    fechaBajaSubtipoCultivo=models.DateField()

    tipo_cultivo=models.ForeignKey(TipoCultivo,db_column="OIDTipoCultivo")

class TipoCultivo(models.Model):
    OIDTipoCultivo=models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    idTipo=models.IntegerField(unique=True)
    nombreTipoCultivo=models.CharField(max_length=20)
    descripcion=models.CharField(max_length=100)
    habilitado=models.BooleanField()
    fechaAltaTipoCultivo=models.DateField()
    fechaBajaTipoCultivo=models.DateField()

class CaracteristicaSubtipo(models.Model):
    OIDCaracteristicaSubtipo=models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    atributo=models.CharField(max_length=20)
    comentario=models.CharField(max_length=100)
    valor=models.CharField(max_length=20)

    subtipo_cultivo=models.ForeignKey(SubtipoCultivo,db_column="OIDSubtipoCultivo",related_name="caracteristica_subtipo_list")


