import uuid

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session


# MODULO SEGURIDAD

class SesionUsuario(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    session = models.ForeignKey(Session, null=True, on_delete=models.SET_NULL)

    tipo_sesion = models.ForeignKey('TipoSesion', db_column="OIDTipoSesion", null=True)

    fecha_y_hora_ultimo_acceso = models.DateTimeField(null=True)
    fecha_y_hora_fin = models.DateTimeField(null=True)
    fecha_y_hora_inicio = models.DateTimeField(null=True)


class TipoSesion(models.Model):
    OIDTipoSesion = models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    idTipo=models.IntegerField()
    nombre=models.CharField(max_length=15)


class DatosUsuario(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    OIDDatosUsuario = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    cuit=models.CharField(max_length=15,null=True)
    dni=models.IntegerField(null=True)
    domicilio=models.CharField(max_length=50,null=True)
    fechaNacimiento=models.DateTimeField(null=True)
    imagenUsuario=models.ImageField(null=True)

    reset_password = models.BooleanField(default=False)
    codigoVerificacion=models.CharField(max_length=10,null=True)

    @receiver(post_save,sender=User)
    def crearDatosUsuario(sender,instance,created,**kwargs):
        if created:
            DatosUsuario.objects.create(user=instance)

    @receiver(post_save,sender=User)
    def guardarDatosUsuario(sender,instance,**kwargs):
        instance.datosusuario.save()

    def as_json(self):
        return dict(usuario=self.user.username,
                    nombre=self.user.first_name,
                    apellido=self.user.last_name,
                    email=self.user.email,
                    cuit=self.cuit,
                    dni=self.dni,
                    domicilio=self.domicilio,
                    fechaNacimiento=self.fechaNacimiento)
                    #imagenUsuario=self.imagenUsuario)


class EstadoUsuario(models.Model):
    OIDEstadoUsuario = models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    descripcionEstadoUsuario=models.CharField(max_length=100)
    nombreEstadoUsuario=models.CharField(max_length=100)


    def __str__(self):
        return self.nombreEstadoUsuario


class HistoricoEstadoUsuario(models.Model):
    OIDHistoricoEstadoUsuario =models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    fechaFinEstadoUsuario=models.DateTimeField(null=True)
    fechaInicioEstadoUsuario=models.DateTimeField()

    usuario=models.ForeignKey(DatosUsuario,db_column="OIDUsuario",related_name="historicoEstadoUsuarioList",null=True)
    estadoUsuario=models.ForeignKey(EstadoUsuario,db_column="OIDEstadoUsuario")

    def __str__(self):
        return self.usuario.user.username + "-" + self.fechaInicioEstadoUsuario + "-" + \
               self.estadoUsuario.nombreEstadoUsuario


class Rol(models.Model):
    OIDRol = models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    nombreRol=models.CharField(max_length=30)
    fechaAltaRol=models.DateTimeField()
    fechaBajaRol=models.DateTimeField(null=True)


class UsuarioFinca(models.Model):
    OIDUsuarioFinca=models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    idUsuarioFinca = models.IntegerField(default=1, unique=True)
    fechaAltaUsuarioFinca=models.DateTimeField()
    fechaBajaUsuarioFinca=models.DateTimeField(null=True)

    finca=models.ForeignKey('Finca',db_column="OIDFinca")
    usuario=models.ForeignKey(DatosUsuario,db_column="OIDUsuario", related_name='usuarioFincaList')
    def save(self):
        "Get last value of Code and Number from database, and increment before save"
        if UsuarioFinca.objects.all().__len__() == 0:
            self.idUsuarioFinca = 1
            super(UsuarioFinca, self).save()
        else:
            if UsuarioFinca.objects.get(idUsuarioFinca=self.idUsuarioFinca) == self:
                super(UsuarioFinca, self).save()
            else:
                ultimoUsuarioFinca = UsuarioFinca.objects.order_by('-idUsuarioFinca')[0]
                self.idUsuarioFinca = ultimoUsuarioFinca.idUsuarioFinca + 1
                super(UsuarioFinca, self).save()


class RolUsuarioFinca(models.Model):
    OIDRolUsuarioFinca=models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    fechaAltaRolUsuarioFinca=models.DateTimeField()
    fechaBajaRolUsuarioFinca=models.DateTimeField(null=True)

    rol=models.ForeignKey(Rol,db_column="OIDRol")
    usuarioFinca=models.ForeignKey(UsuarioFinca,db_column="OIDUsuarioFinca",related_name="rolUsuarioFincaList",
                                   null=True)


class ConjuntoPermisos (models.Model):
    OIDConjuntoPermisos=models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    puedeAsignarComponenteSensor=models.BooleanField()
    puedeAsignarCultivo = models.BooleanField()
    puedeAsignarMecRiegoAFinca = models.BooleanField()
    puedeAsignarMecRiegoASector = models.BooleanField()
    puedeConfigurarObtencionInfoExterna = models.BooleanField()
    puedeCrearComponenteSensor = models.BooleanField()
    puedeCrearConfiguracionRiego = models.BooleanField()
    puedeCrearSector= models.BooleanField()
    puedeGenerarInformeCruzadoRiegoMedicion= models.BooleanField()
    puedeGenerarInformeEstadoActualSectores= models.BooleanField()
    puedeGenerarInformeEstadoHistoricoSectoresFinca= models.BooleanField()
    puedeGenerarInformeEventoPersonalizado= models.BooleanField()
    puedeGenerarInformeHeladasHistorico= models.BooleanField()
    puedeGenerarInformeRiegoEnEjecucion= models.BooleanField()
    puedeGenerarInformeRiegoPorSectoresHistorico= models.BooleanField()
    puedeGestionarComponenteSensor= models.BooleanField()
    puedeGestionarCultivoSector= models.BooleanField()
    puedeGestionarEventoPersonalizado= models.BooleanField()
    puedeGestionarFinca= models.BooleanField()
    puedeGestionarSector= models.BooleanField()
    puedeGestionarSensores= models.BooleanField()
    puedeGestionarUsuariosFinca= models.BooleanField()
    puedeIniciarODetenerRiegoManualmente= models.BooleanField()
    puedeModificarConfiguracionRiego= models.BooleanField()

    rol = models.ForeignKey(Rol, db_column="OIDRol", related_name="conjuntoPermisos")

    def as_json(self):
        return dict(
        puedeAsignarComponenteSensor = self.puedeAsignarComponenteSensor,
        puedeAsignarCultivo = self.puedeAsignarCultivo,
        puedeAsignarMecRiegoAFinca = self.puedeAsignarMecRiegoAFinca,
        puedeAsignarMecRiegoASector = self.puedeAsignarMecRiegoASector,
        puedeConfigurarObtencionInfoExterna = self.puedeConfigurarObtencionInfoExterna,
        puedeCrearComponenteSensor = self.puedeCrearComponenteSensor,
        puedeCrearConfiguracionRiego = self.puedeCrearConfiguracionRiego,
        puedeCrearSector = self.puedeCrearSector,
        puedeGenerarInformeCruzadoRiegoMedicion = self.puedeGenerarInformeCruzadoRiegoMedicion,
        puedeGenerarInformeEstadoActualSectores = self.puedeGenerarInformeEstadoActualSectores,
        puedeGenerarInformeEstadoHistoricoSectoresFinca = self.puedeGenerarInformeEstadoHistoricoSectoresFinca,
        puedeGenerarInformeEventoPersonalizado = self.puedeGenerarInformeEventoPersonalizado,
        puedeGenerarInformeHeladasHistorico = self.puedeGenerarInformeHeladasHistorico,
        puedeGenerarInformeRiegoEnEjecucion = self.puedeGenerarInformeRiegoEnEjecucion,
        puedeGenerarInformeRiegoPorSectoresHistorico = self.puedeGenerarInformeRiegoPorSectoresHistorico,
        puedeGestionarComponenteSensor = self.puedeGestionarComponenteSensor,
        puedeGestionarCultivoSector = self.puedeGestionarCultivoSector,
        puedeGestionarEventoPersonalizado = self.puedeGestionarEventoPersonalizado,
        puedeGestionarFinca = self.puedeGestionarFinca,
        puedeGestionarSector = self.puedeGestionarSector,
        puedeGestionarSensores = self.puedeGestionarSensores,
        puedeGestionarUsuariosFinca = self.puedeGestionarUsuariosFinca,
        puedeIniciarODetenerRiegoManualmente = self.puedeIniciarODetenerRiegoManualmente,
        puedeModificarConfiguracionRiego = self.puedeModificarConfiguracionRiego)


#MODULO FINCA

class ProveedorInformacionClimaticaFinca(models.Model):
    OIDProveedorInformacionClimaticaFinca = models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    fechaAltaProveedorInfoClimaticaFinca=models.DateTimeField()
    fechaBajaProveedorInfoClimaticaFinca=models.DateTimeField(null=True)
    frecuencia=models.IntegerField(null=True)

    finca=models.ForeignKey("Finca",db_column="OIDFinca",null=True)
    proveedorInformacionClimatica=models.ForeignKey("ProveedorInformacionClimatica",db_column="OIDProveedorInformacionClimatica",null=True)


class Finca(models.Model):
    OIDFinca=models.UUIDField( primary_key=True ,default=uuid.uuid4, editable=False)
    idFinca=models.IntegerField(default=1, unique=True)
    direccionLegal=models.CharField(max_length=50)
    logoFinca=models.ImageField(null=True)
    nombre=models.CharField(max_length=50)
    tamanio=models.FloatField()
    ubicacion=models.CharField(max_length=50)

    def __str__(self):
        return str(self.idFinca) + "-" + self.nombre

    def save(self):
        "Get last value of Code and Number from database, and increment before save"
        if Finca.objects.all().__len__() == 0:
            self.idFinca = 1
            super(Finca, self).save()
        else:
            if Finca.objects.get(idFinca=self.idFinca) == self:
                super(Finca, self).save()
            else:
                ultimaFinca = Finca.objects.order_by('-idFinca')[0]
                self.idFinca = ultimaFinca.idFinca + 1
                super(Finca, self).save()

    def as_json(self):
        return dict(
            direccionLegal=self.direccionLegal,
            idFinca=self.idFinca,
            nombre=self.nombre,tamanio=self.tamanio,
            ubicacion=self.ubicacion)
            #logoFinca=self.logoFinca)


class EstadoFinca(models.Model):
    OIDFinca = models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    descripcionEstadoFinca=models.CharField(max_length=100)
    nombreEstadoFinca=models.CharField(max_length=50)


class HistoricoEstadoFinca(models.Model):
    OIDHistoricoEstadoFinca = models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    fechaFinEstadoFinca=models.DateTimeField(null=True)
    fechaInicioEstadoFinca=models.DateTimeField()

    finca=models.ForeignKey(Finca,db_column="OIDFinca",related_name="historicoEstadoFincaList")
    estadoFinca=models.ForeignKey(EstadoFinca,db_column="OIDEstadoFinca")


class MecanismoRiegoFinca(models.Model):
    OIDMecanismoRiegoFinca = models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    direccionIP=models.CharField(max_length=20)
    fechaInstalacion=models.DateTimeField()
    idMecanismoRiegoFinca=models.IntegerField(default=1, unique=True)


    finca=models.ForeignKey(Finca,db_column="OIDFinca")
    tipoMecanismoRiego=models.ForeignKey("TipoMecanismoRiego",db_column="OIDTipoMecanismoRiego",null=True)

    def as_json(self):
        return dict(
                    direccionIP=self.direccionIP,
                    fechaInstalacion=self.fechaInstalacion,
                    idMecanismoRiegoFinca=self.idMecanismoRiegoFinca,
                    tipoMecanismoRiego=self.tipoMecanismoRiego.nombreMecanismo)


                    #imagenUsuario=self.imagenUsuario)
    def save(self):
        if MecanismoRiegoFinca.objects.all().__len__() == 0:
                self.idMecanismoRiegoFinca = 1
                super(MecanismoRiegoFinca, self).save()
        else:
            if MecanismoRiegoFinca.objects.get(idMecanismoRiegoFinca=self.idMecanismoRiegoFinca) == self:
                super(MecanismoRiegoFinca, self).save()
            else:
                ultimoMecanismo = MecanismoRiegoFinca.objects.order_by('-idMecanismoRiegoFinca')[0]
                self.idMecanismoRiegoFinca = ultimoMecanismo.idMecanismoRiegoFinca + 1
                super(MecanismoRiegoFinca, self).save()
        super(MecanismoRiegoFinca, self).save()



class EstadoMecanismoRiegoFinca(models.Model):
    OIDEstadoMecanismoRiegoFinca = models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    nombreEstadoMecanismoRiegoFinca=models.CharField(max_length=20)
    descripcionEstadoMecanismoRiegoFinca=models.CharField(max_length=100)


class HistoricoMecanismoRiegoFinca(models.Model):
    OIDHistoricoMecanismoRiegoFinca =models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    fechaInicioEstadoMecanismoRiegoFinca=models.DateTimeField(null=True)
    fechaFinEstadoMecanismoRiegoFinca = models.DateTimeField(null=True)
    mecanismo_riego_finca=models.ForeignKey(MecanismoRiegoFinca,db_column="OIDMecanismoRiegoFinca",related_name="historicoMecanismoRiegoFincaList")
    estado_mecanismo_riego_finca=models.ForeignKey(EstadoMecanismoRiegoFinca,db_column="OIDEstadoMecanismoRiegoFinca")


#MODULO SECTORES

class Sector(models.Model):
    OIDSector=models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False)
    idSector = models.IntegerField(default=1, unique=True)
    numeroSector=models.IntegerField()
    nombreSector=models.CharField(max_length=30)
    descripcionSector=models.CharField(max_length=100)
    superficie=models.FloatField()

    finca = models.ForeignKey("Finca", db_column="OIDFinca", related_name="sectorList", null=True)


    def save(self):
        "Get last value of Code and Number from database, and increment before save"
        if Sector.objects.all().__len__() == 0:
            self.idSector = 1
            super(Sector, self).save()
        else:
            if Sector.objects.get(idSector=self.idSector) == self:
                super(Sector, self).save()
            else:
                ultimoSector = Sector.objects.order_by('-idSector')[0]
                self.idSector = ultimoSector.idSector + 1
                super(Sector, self).save()

    def __str__(self):
        return ("Este es el sector %d")%self.numeroSector

    def as_json(self):
        return dict(
                    idSector=self.idSector,
                    numeroSector=self.numeroSector,
                    nombreSector=self.nombreSector,
                    descripcionSector=self.descripcionSector,
                    superficieSector=self.superficie)



class Cultivo(models.Model):
    OIDCultivo = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    idCultivo = models.IntegerField(default=1, unique=True)
    descripcion = models.CharField(max_length=100)
    nombre = models.CharField(max_length=20)
    fechaPlantacion = models.DateTimeField()
    fechaEliminacion = models.DateTimeField(null=True)
    habilitado = models.BooleanField()

    subtipo_cultivo = models.ForeignKey('SubtipoCultivo', db_column="OIDSubtipoCultivo")
    sector= models.ForeignKey(Sector, db_column="OIDSector")



    def save(self):
        "Get last value of Code and Number from database, and increment before save"
        if Cultivo.objects.all().__len__() == 0:
            self.idCultivo = 1
            super(Cultivo, self).save()
        else:
            if Cultivo.objects.get(idCultivo=self.idCultivo) == self:
                super(Cultivo, self).save()
            else:
                ultimoCultivo = Cultivo.objects.order_by('-idCultivo')[0]
                self.idCultivo = ultimoCultivo.idCultivo + 1
                super(Cultivo, self).save()


    def __str__(self):
        return ("Este es el cultivo %s")%self.nombre


    def as_json(self):
        return dict(descripcion=self.descripcion,
                    idCultivo=self.idCultivo,
                    nombre=self.nombre,
                    fechaPlantacion=self.fechaPlantacion,
                    fechaEliminacion=self.fechaEliminacion,
                    habilitado=self.habilitado,
                    subtipo=self.subtipo_cultivo.nombreSubtipo,
                    tipo=self.subtipo_cultivo.tipo_cultivo.nombreTipoCultivo)


class EstadoSector(models.Model):
    OIDEstadoSector=models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False)
    descripcionEstadoSector=models.CharField(max_length=100)
    nombreEstadoSector=models.CharField(max_length=20)

    def __str__(self):
        return ("Este es el estado %s") % self.nombreEstadoSector


class HistoricoEstadoSector(models.Model):
    OIDHistoricoEstadoSector=models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    fechaFinEstadoSector=models.DateTimeField(null=True)
    fechaInicioEstadoSector=models.DateTimeField()

    estado_sector=models.ForeignKey(EstadoSector,db_column="OIDEstadoSector")
    sector=models.ForeignKey(Sector,db_column="OIDSector",related_name="historicoEstadoSectorList")


class EstadoMecanismoRiegoFincaSector(models.Model):
    OIDEstadoMecanismoRiegoFincaSector=models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    descripcionEstadoMecanismoRiegoFincaSector=models.CharField(max_length=100)
    nombreEstadoMecanismoRiegoFincaSector=models.CharField(max_length=20)


class HistoricoMecanismoRiegoFincaSector(models.Model):
    OIDHistoricoMecanismoRiegoFincaSector=models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    fechaFinEstadoMecanismoRiegoFincaSector=models.DateTimeField(null=True)
    fechaInicioEstadoMecanismoRiegoFincaSector=models.DateTimeField()

    mecanismo_riego_finca_sector=models.ForeignKey('MecanismoRiegoFincaSector',db_column="OIDMecanismoRiegoFincaSector",
                                                   related_name="historicoMecanismoRiegoFincaSector")
    estado_mecanismo_riego_finca_sector=models.ForeignKey(EstadoMecanismoRiegoFincaSector,
                                                          db_column="OIDEstadoMecanismoRiegoFincaSector")


class ComponenteSensor(models.Model):
    OIDComponenteSensor=models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    numeroComponente=models.IntegerField()
    habilitado=models.BooleanField()
    fechaAltaComponenteSensor=models.DateTimeField()
    fechaBajaComponenteSensor=models.DateTimeField(null=True)


#MODULO CULTIVOS

class TipoCultivo(models.Model):
    OIDTipoCultivo = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombreTipoCultivo = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=100)
    habilitado = models.BooleanField()
    fechaAltaTipoCultivo = models.DateTimeField()
    fechaBajaTipoCultivo = models.DateTimeField(null=True)


class SubtipoCultivo(models.Model):
    OIDSubtipoCultivo = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombreSubtipo = models.CharField(max_length=20)
    habilitado = models.BooleanField()
    descripcion = models.CharField(max_length=100)
    fechaAltaSubtipoCultivo = models.DateTimeField()
    fechaBajaSubtipoCultivo = models.DateTimeField(null=True)

    tipo_cultivo = models.ForeignKey(TipoCultivo, db_column="OIDTipoCultivo")


class CaracteristicaSubtipo(models.Model):
    OIDCaracteristicaSubtipo = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    atributo = models.CharField(max_length=20)
    comentario = models.CharField(max_length=100)
    valor = models.CharField(max_length=20)

    subtipo_cultivo = models.ForeignKey(SubtipoCultivo, db_column="OIDSubtipoCultivo",
                                            related_name="caracteristicaSubtipoList")


#MODULO RIEGO

class TipoMecanismoRiego(models.Model):
    OIDTipoMecanismoRiego = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombreMecanismo = models.CharField(max_length=30,unique=True)
    descripcion=models.CharField(max_length=200,null=True)
    caudalEstandar = models.FloatField(null=True)
    presionEstandar=models.FloatField(null=True)
    eficiencia=models.FloatField(null=True)
    fechaAltaTipoMecanismoRiego=models.DateTimeField()
    fechaBajaTipoMecanismoRiego=models.DateTimeField(null=True)
    habilitado=models.BooleanField(default=True)
    def as_json(self):
        return dict(
            nombreMecanismo=self.nombreMecanismo,
            descripcion=self.descripcion,
            presionEstandar=self.presionEstandar,
            eficiencia=self.eficiencia,
            fechaAltaTipoMecanismoRiego=self.fechaAltaTipoMecanismoRiego,
            habilitado=self.habilitado
        )


class TipoConfiguracionRiego(models.Model):
    OIDTipoConfiguracionRiego=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    idTipoConfiguracion=models.IntegerField(unique=True)
    nombre=models.CharField(max_length=20,unique=True)


class ConfiguracionRiego(models.Model):
    OIDConfiguracionRiego=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre=models.CharField(max_length=20)
    descripcion=models.CharField(max_length=100)
    duracionMaxima=models.FloatField()
    fechaCreacion=models.DateTimeField()
    fechaFinalizacion=models.DateTimeField()

    tipoConfiguracionRiego=models.ForeignKey(TipoConfiguracionRiego,db_column="OIDTipoConfiguracionRiego")
    mecanismoRiegoFincaSector=models.ForeignKey('MecanismoRiegoFincaSector',db_column="OIDMecanismoRiegoFincaSector",null=True)


class EstadoConfiguracionRiego(models.Model):
    OIDEstadoConfiguracionRiego=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombreEstadoConfiguracionRiego=models.CharField(max_length=20,unique=True)
    descripcionEstadoConfiguracionRiego=models.CharField(max_length=100)


class HistoricoEstadoConfiguracionRiego(models.Model):
    OIDHistoricoEstadoConfiguracionRiego=  models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fechaFinEstadoConfiguracionRiego = models.DateTimeField()
    fechaInicioEstadoConfiguracionRiego = models.DateTimeField()

    configuracion_riego = models.ForeignKey(ConfiguracionRiego,db_column="OIDConfiguracionRiego",
                                          related_name="historicoEstadoConfiguracionRiegoList")
    estado_configuracion_riego = models.ForeignKey(EstadoConfiguracionRiego,
                                                 db_column="OIDEstadoConfiguracionRiego")


class EstadoEjecucionRiego(models.Model):
    OIDEstadoEjecucionRiego = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombreEstadoEjecucionRiego = models.CharField(max_length=20,unique=True)
    descripcionEstadoEjecucionRiego = models.CharField(max_length=100)


class MecanismoRiegoFincaSector(models.Model):
    OIDMecanismoRiegoFincaSector = models.UUIDField(default=uuid.uuid4(), primary_key=True, editable=False)
    idMecanismoRiegoFincaSector = models.IntegerField(default=1, unique=True)
    caudal = models.FloatField()
    presion = models.FloatField()

    mecanismoRiegoFinca = models.ForeignKey(MecanismoRiegoFinca, db_column="OIDMecanismoRiegoFinca",
                                              related_name="mecanismoRiegoSectorList", null=True)
    sector = models.ForeignKey(Sector, db_column="OIDSector", related_name="mecanismoRiegoFincaSector", null=True)


    def save(self):
        "Get last value of Code and Number from database, and increment before save"
        if MecanismoRiegoFincaSector.objects.all().__len__() == 0:
            self.idMecanismoRiegoFincaSector = 1
            super(MecanismoRiegoFincaSector, self).save()
        else:
            if MecanismoRiegoFincaSector.objects.get(idMecanismoRiegoFincaSector=self.idMecanismoRiegoFincaSector) == self:
                super(MecanismoRiegoFincaSector, self).save()
            else:
                ultimoMecanismoFincaRiegoSector = MecanismoRiegoFincaSector.objects.order_by('-idMecanismoRiegoFincaSector')[0]
                self.idMecanismoRiegoFincaSector = ultimoMecanismoFincaRiegoSector.idMecanismoRiegoFincaSector + 1
                super(MecanismoRiegoFincaSector, self).save()
    def as_json(self):
        return dict(idMecanismoRiegoFincaSector=self.idMecanismoRiegoFincaSector,
                    caudal=self.caudal,
                    presion=self.presion,
                    sector=self.sector.numeroSector,
                    mecanismoRiegoFinca=self.mecanismoRiegoFinca.idMecanismoRiegoFinca)
class EjecucionRiego(models.Model):
    OIDEjecucionRiego = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cantidadAguaUtilizada = models.FloatField()
    detalle = models.CharField(max_length=100)
    duracionActual = models.FloatField()
    fechaHoraFinalizacion = models.DateTimeField()
    fechaHoraFinalProgramada = models.DateTimeField()
    fechaHoraInicio = models.DateTimeField()
    fechaHoraInicioProgramada = models.DateTimeField()

    configuracion_riego = models.ForeignKey(ConfiguracionRiego, db_column="OIDConfiguracionRiego")
    estado_ejecucion_riego = models.ForeignKey(EstadoEjecucionRiego, db_column="OIDEstadoEjecucionRiego")
    mecanismo_riego_finca_sector = models.ForeignKey(MecanismoRiegoFincaSector, db_column="OIDMecanismoRiegoFincaSector",
                                                   related_name="ejecucionRiegoList")


class CriterioRiego(models.Model):
    OIDCriterioRiego = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    fechaCreacionCriterio = models.DateTimeField()
    # class Meta:
    #     abstract=True
    #ESTO ES LO MAS IMPORTANTE HAY Q VER COMO IMPLEMENTAMOS LOS CRITERIOS INICIALES Y FINALES
    #COMO LAS RELACIONES SE MANEJAN AL REVES LO Q YO HICE FUE Q APUNTARA DOS VECSE A LA CONFIGURACION DE RIEGO
    #Y Q LA OTRA TENGA DOS ATRIBUTOS Q PARA LOS CRITERIOS INICIALES Y PARA LOS FINALES(LOS Q ESTAN EN EL related_name)
    # configuracionRiegoInicial = models.ForeignKey(ConfiguracionRiego, db_column="OIDConfiguracionRiegoInicial",
    #                                               related_name="criterioRiegoInicioList")
    configuracionRiegoInicial = models.OneToOneField(ConfiguracionRiego, on_delete=models.CASCADE,
                                                     db_column="OIDConfiguracionRiegoInicial",
                                                     related_name="criterioRiegoInicial", null=True)
    configuracionRiegoFinal = models.ForeignKey(ConfiguracionRiego, db_column="OIDConfiguracionRiegoFinal",
                                                related_name="criterioRiegoFinal", null=True)


class CriterioRiegoPorMedicion(CriterioRiego):
    valor = models.FloatField()
    # class Meta(CriterioRiego.Meta):
    #     db_table="CriterioRiegoPorMedicion"
    # configuracionRiegoInicial=models.ForeignKey(ConfiguracionRiego,db_column="OIDConfiguracionRiegoInicial",related_name="%(class)scriterioRiegoInicioList")
    # configuracionRiegoFinal = models.ForeignKey(ConfiguracionRiego, db_column="OIDConfiguracionRiegoFinal", related_name="%(class)scriterioRiegoFinal")


class CriterioRiegoVolumenAgua(CriterioRiego):
    volumen = models.FloatField()
    # class Meta(CriterioRiego.Meta):
    #     db_table="CriterioRiegoVolumenAgua"
    # configuracionRiegoInicial=models.ForeignKey(ConfiguracionRiego,db_column="OIDConfiguracionRiegoInicial",related_name="%(class)scriterioRiegoInicioList")
    # configuracionRiegoFinal = models.ForeignKey(ConfiguracionRiego, db_column="OIDConfiguracionRiegoFinal", related_name="%(class)scriterioRiegoFinal")


class CriterioRiegoPorHora(CriterioRiego):
    hora = models.DateTimeField()
    numeroDia = models.IntegerField()
    # class Meta(CriterioRiego.Meta):
    #     db_table = "CriterioRiegoPorHora"
    # configuracionRiegoInicial=models.ForeignKey(ConfiguracionRiego,db_column="OIDConfiguracionRiegoInicial",related_name="%(class)scriterioRiegoInicioList")
    # configuracionRiegoFinal = models.ForeignKey(ConfiguracionRiego, db_column="OIDConfiguracionRiegoFinal", related_name="%(class)scriterioRiegoFinal")


#MODULO SENSORES

class TipoMedicion(models.Model):
    OIDTipoMedicion = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False)
    idTipoMedicion = models.IntegerField(default=1, unique=True)
    nombreTipoMedicion = models.CharField(max_length=20)
    unidadMedicion = models.CharField(max_length=20)
    habilitado = models.BooleanField()
    fechaAltaTipoMedicion = models.DateTimeField()
    fechaBajaTipoMedicion = models.DateTimeField(null=True)

    def save(self):
        "Get last value of Code and Number from database, and increment before save"
        if TipoMedicion.objects.all().__len__() == 0:
            self.idTipoMedicion = 1
            super(TipoMedicion, self).save()
        else:
            if TipoMedicion.objects.get(idTipoMedicion=self.idTipoMedicion) == self:
                super(TipoMedicion, self).save()
            else:
                ultimaTipoMedicion = TipoMedicion.objects.order_by('-idTipoMedicion')[0]
                self.idTipoMedicion = ultimaTipoMedicion.idTipoMedicion + 1
                super(TipoMedicion, self).save()


    def as_json(self):
        return dict(idTipoMedicion=self.idTipoMedicion,
                    nombreTipoMedicion=self.nombreTipoMedicion,
                    unidadMedicion=self.unidadMedicion,
                    habilitado=self.habilitado,
                    fechaAltaTipoMedicion=self.fechaAltaTipoMedicion,
                    fechaBajaTipoMedicion=self.fechaBajaTipoMedicion)



class Sensor(models.Model):
    OIDSensor = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False)
    idSensor = models.IntegerField(default=1, unique=True)
    fechaAltaSensor = models.DateTimeField()
    fechaBajaSensor = models.DateTimeField(null=True)
    habilitado = models.BooleanField()
    modelo = models.CharField(max_length=20)

    ComponenteSensor = models.ForeignKey(ComponenteSensor,db_column="OIDComponenteSensor",
                                        related_name="sensor", null=True)
    tipoMedicion = models.ForeignKey('TipoMedicion',db_column="OIDTipoMedicion", null=True)
    finca = models.ForeignKey('Finca', db_column="OIDFinca", null=True)


    def save(self):
        "Get last value of Code and Number from database, and increment before save"
        if Sensor.objects.all().__len__() == 0:
            self.idSensor = 1
            super(Sensor, self).save()
        else:
            if Sensor.objects.get(idSensor=self.idSensor) == self:
                super(Sensor, self).save()
            else:
                ultimoSensor = Sensor.objects.order_by('-idSensor')[0]
                self.idSensor = ultimoSensor.idSensor + 1
                super(Sensor, self).save()

    def as_json(self):
        return dict(idSensor=self.idSensor,
                    fechaAltaSensor=self.FechaAltaSensor,
                    fechaBajaSensor=self.fechaBajaSensor,
                    habilitado=self.habilitado,
                    modelo=self.modelo,
                    tipoMedicion=self.tipoMedicion.nombreTipoMedicion)


class ComponenteSensorSector(models.Model):
    OIDComponenteSensorSector=models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    idComponenteSensores=models.IntegerField()

    componente_sensor=models.ForeignKey(Sector,db_column="OIDSector")


class HistoricoComponenteSensorSector(models.Model):
    OIDHistoricoComponenteSensorSector=models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    fechaAltaComponenteSensorSector=models.DateTimeField()
    fechaBajaComponenteSensorSecto=models.DateTimeField(null=True)
    componenteSensorSector=models.ForeignKey(ComponenteSensorSector,db_column="OIDComponenteSensorSector",related_name="historicoComponenteSensorSector")


class EstadoComponenteSensorSector(models.Model):
    models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombreEstadoSensorSector=models.CharField(max_length=20)
    descripcionEstadoSensorSector=models.CharField(max_length=100)


class MedicionCabecera(models.Model):
    OIDMedicionCabecera=models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    fechaYHora=models.DateTimeField()
    nroMedicion=models.IntegerField()


class MedicionDetalle(models.Model):
    OIDMedicionDetalle=models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    nroRenglon=models.IntegerField()
    valor=models.FloatField()
    medicionCabecera=models.ForeignKey(MedicionCabecera,db_column="OIDMedicionCabecera",related_name="medicionDetalle")


#MODULO EVENTOS

class MedicionEvento(models.Model):
    OIDMedicionEvento = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    valorMaximo = models.FloatField()
    valorMinimo = models.FloatField()
    # class Meta:
    #     ordering = ['valorMinimo']
    #     abstract = True# CON ESTO HACEMOS Q LA CLASE SEA ABSTRACTA

    configuracionEventoPersonalizado=models.ForeignKey('EventoPersonalizado',db_column="OIDConfiguracionEventoPersonalizado",related_name="medicionEventoList")


class MedicionFuenteInterna(MedicionEvento):
    # RECIBE COMO PARAMETRO A LA CLASE MEDICION EVENTO PORQUE HEREDA DE ELLA
    # class Meta(MedicionEvento.Meta):
    #     db_table = "MedicionFuenteInterna"
    tipoMedicion = models.ForeignKey('TipoMedicion',db_column="OIDTipoMedicion")


class ConfiguracionEventoPersonalizado(models.Model):
    OIDConfiguracionEventoPersonalizado = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    idConfiguracion = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=100)
    notificacionActivada = models.BooleanField()
    fechaAltaConfiguracionEventoPersonalizado = models.DateTimeField()
    fechaBajaConfiguracionEventoPersonalizado = models.DateTimeField(null=True)
    fechaHoraCreacion = models.DateTimeField()

    usuario_finca = models.ForeignKey(UsuarioFinca, db_column="OIDUsuarioFinca",
                                              related_name="usuarioFinca")


class EventoPersonalizado(models.Model):
    OIDEventoPersonalizado = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nroEvento = models.IntegerField(unique=True)
    fechaHora = models.DateTimeField()

    configuracion_evento_personalizado = models.ForeignKey(ConfiguracionEventoPersonalizado,
                                                                   db_column="OIDConfiguracionEventoPersonalizado")


#MODULO INFORMACION EXTERNA

class TipoMedicionClimatica(models.Model):
    OIDTipoMedicionClimatica=models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    idTipoMedicionClimatica=models.IntegerField(unique=True)
    nombreTipoMedicionClimatica=models.IntegerField(unique=True)
    tipoDato=models.CharField(max_length=10)
    fechaAltaTipoMedicionClimatica=models.DateTimeField()
    fechaBajaTipoMedicionClimatica=models.DateTimeField(null=True)
    habilitada=models.BooleanField()


class ProveedorInformacionClimatica(models.Model):
    OIDProveedorInformacionClimatica=models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    nombreProveedor=models.CharField(max_length=20,unique=True)
    habilitado=models.BooleanField()
    urlAPI=models.CharField(max_length=100,null=True)
    frecuenciaMaxPosible=models.IntegerField(null=True)
    fechaAltaProveedorInfoClimatica=models.DateTimeField()
    fechaBajaProveedorInfoClimatica=models.DateTimeField(null=True)

    tipo_medicion_climatica=models.ManyToManyField(TipoMedicionClimatica)


    def __str__(self):
        return self.nombreProveedor

    def as_json(self):
        return dict(
            nombreProveedor=self.nombreProveedor,
            habilitado=self.habilitado,
            frecuenciaMaxPosible=self.frecuenciaMaxPosible,
            urlAPI=self.urlAPI)


class MedicionEstadoExterno(MedicionEvento):
    #HERENCIA
    tipo_medicion_climatica=models.ForeignKey(TipoMedicionClimatica,db_column="OIDTipoMedicionClimatica")
    # class Meta(MedicionEvento.Meta):
    #     db_table = "MedicionEstadoExterno"



class MedicionInformacionClimaticaCabecera(models.Model):
    OIDMedicionInformacionClimaticaCabecera=models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    nroMedicion=models.IntegerField(unique=True)
    fechaHora=models.DateTimeField()

    proveedor_informacion_climatica_externa=models.ForeignKey(ProveedorInformacionClimaticaFinca,db_column="OIDProveedorInformacionClimaticaFinca",related_name="medicionInformacionClimaticaCabeceraList")


class MedicionInformacionClimaticaDetalle(models.Model):
    OIDMedicionInformacionClimaticaDetalle=models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    nroRenglon=models.IntegerField()
    valor=models.FloatField()

    medicion_informacion_climatica_cabecera=models.ForeignKey(MedicionInformacionClimaticaCabecera,db_column="OIDMedicionInformacionClimaticaCabecera",related_name="medicionInformacionClimaticaDetalle")
    tipo_medicion_climatica=models.ForeignKey(TipoMedicionClimatica,db_column="OIDTipoMedicionClimatica")