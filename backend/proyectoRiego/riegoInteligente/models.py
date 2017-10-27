from datetime import datetime
import pytz
import uuid
from model_utils.managers import InheritanceManager

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

    class Meta:
        verbose_name_plural = "Sesiones usuarios"

    def __str__(self):
        if self.session:
            if self.tipo_sesion:
                return "Usuario: " + self.user.username + " - Tipo de sesion: " + self.tipo_sesion.nombre + \
                       " - Id sesion activa: " + str(self.session.session_key)
            else:
                return "Usuario: " + self.user.username + " - Tipo de sesion: no definido" + \
                       " - Id sesion activa: " + str(self.session.session_key)
        else:
            if self.tipo_sesion:
                return "Usuario: " + self.user.username + " - Tipo de sesion: " + self.tipo_sesion.nombre + \
                       " - Sesion no activa"
            else:
                return "Usuario: " + self.user.username + " - Tipo de sesion: no definido" + " - Sesion no activa"


class TipoSesion(models.Model):
    OIDTipoSesion = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    idTipo = models.IntegerField()
    nombre = models.CharField(max_length=15)

    class Meta:
        verbose_name_plural = "_Tipos de sesion"

    def __str__(self):
        return "Tipo sesion: " + self.nombre


# noinspection PyPep8Naming,PyMethodParameters,PyUnusedLocal
class DatosUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    OIDDatosUsuario = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    cuit = models.CharField(max_length=15, null=True)
    dni = models.IntegerField(null=True)
    domicilio = models.CharField(max_length=50, null=True)
    fechaNacimiento = models.DateTimeField(null=True)
    imagenUsuario = models.ImageField(null=True)

    reset_password = models.BooleanField(default=False)
    codigoVerificacion = models.CharField(max_length=10, null=True)

    @receiver(post_save, sender=User)
    def crearDatosUsuario(sender, instance, created, **kwargs):
        if created:
            DatosUsuario.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def guardarDatosUsuario(sender, instance, **kwargs):
        instance.datosusuario.save()

    class Meta:
        verbose_name_plural = "Datos de usuarios"

    def __str__(self):
        return "Datos de usuario: " + self.user.username

    def as_json(self):
        fecha_nacimiento = None
        if self.fechaNacimiento is not None:
            fecha_nacimiento = self.fechaNacimiento.date()

        return dict(
            usuario=self.user.username,
            nombre=self.user.first_name,
            apellido=self.user.last_name,
            email=self.user.email,
            cuit=self.cuit,
            dni=self.dni,
            domicilio=self.domicilio,
            fechaNacimiento=fecha_nacimiento
            # imagenUsuario=self.imagenUsuario
        )


class EstadoUsuario(models.Model):
    OIDEstadoUsuario = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    descripcionEstadoUsuario = models.CharField(max_length=100)
    nombreEstadoUsuario = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "_Estados usuario"

    def __str__(self):
        return "Estado usuario: " + self.nombreEstadoUsuario


class HistoricoEstadoUsuario(models.Model):
    OIDHistoricoEstadoUsuario = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fechaFinEstadoUsuario = models.DateTimeField(null=True)
    fechaInicioEstadoUsuario = models.DateTimeField()

    usuario = models.ForeignKey(DatosUsuario, db_column="OIDUsuario",
                                related_name="historicoEstadoUsuarioList",
                                null=True)
    estadoUsuario = models.ForeignKey(EstadoUsuario, db_column="OIDEstadoUsuario")

    class Meta:
        verbose_name_plural = "Historicos estado usuarios"

    def __str__(self):
        if self.fechaFinEstadoUsuario:
            return "(Finalizado) " + self.usuario.user.username + " - estado: " + \
                   self.estadoUsuario.nombreEstadoUsuario + \
                   " - Creado en fecha: " + str(self.fechaInicioEstadoUsuario.date()) + \
                   " - hora: " + str(self.fechaInicioEstadoUsuario.time())
        else:
            return self.usuario.user.username + " - estado: " + self.estadoUsuario.nombreEstadoUsuario + \
                   " - Creado en fecha: " + str(self.fechaInicioEstadoUsuario.date()) + \
                   " - hora: " + str(self.fechaInicioEstadoUsuario.time())


class Rol(models.Model):
    OIDRol = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombreRol = models.CharField(max_length=30)
    fechaAltaRol = models.DateTimeField()
    fechaBajaRol = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Roles"

    def save(self, *args, **kwargs):
        if not self.fechaBajaRol:
            self.fechaBajaRol = None
        super(Rol, self).save(*args, **kwargs)

    def __str__(self):
        return "Nombre rol: " + self.nombreRol

    def as_json(self):
        return dict(
            nombreRol=self.nombreRol,
            fechaAltaRol=self.fechaAltaRol,
            fechaBajaRol=self.fechaBajaRol
        )


class UsuarioFinca(models.Model):
    OIDUsuarioFinca = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    idUsuarioFinca = models.IntegerField(default=1, unique=True, editable=False)
    fechaAltaUsuarioFinca = models.DateTimeField()
    fechaBajaUsuarioFinca = models.DateTimeField(null=True)

    finca = models.ForeignKey('Finca', db_column="OIDFinca")
    usuario = models.ForeignKey(DatosUsuario, db_column="OIDUsuario", related_name='usuarioFincaList')
    configuracionEventoPersonalizadoList = models.ManyToManyField("ConfiguracionEventoPersonalizado")

    def __str__(self):
        return "Usuario: " + str(self.usuario.user.username) + " de finca: " + str(self.finca.idFinca)

    def save(self, *args, **kwargs):
        """Get last value of Code and Number from database, and increment before save"""
        if UsuarioFinca.objects.all().__len__() == 0:
            self.idUsuarioFinca = 1
            super(UsuarioFinca, self).save(*args, **kwargs)
        else:
            if UsuarioFinca.objects.get(idUsuarioFinca=self.idUsuarioFinca) == self:
                super(UsuarioFinca, self).save(*args, **kwargs)
            else:
                ultimo_usuario_finca = UsuarioFinca.objects.order_by('-idUsuarioFinca')[0]
                self.idUsuarioFinca = ultimo_usuario_finca.idUsuarioFinca + 1
                super(UsuarioFinca, self).save(*args, **kwargs)


class RolUsuarioFinca(models.Model):
    OIDRolUsuarioFinca = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fechaAltaRolUsuarioFinca = models.DateTimeField()
    fechaBajaRolUsuarioFinca = models.DateTimeField(null=True)

    rol = models.ForeignKey(Rol, db_column="OIDRol")
    usuarioFinca = models.ForeignKey(UsuarioFinca, db_column="OIDUsuarioFinca", related_name="rolUsuarioFincaList",
                                     null=True)

    def __str__(self):
        return "Rol: " + self.rol.nombreRol + " usuario finca: " + str(self.usuarioFinca.idUsuarioFinca)


class ConjuntoPermisos (models.Model):
    OIDConjuntoPermisos = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    puedeAsignarComponenteSensor = models.BooleanField()
    puedeAsignarCultivo = models.BooleanField()
    puedeAsignarMecRiegoAFinca = models.BooleanField()
    puedeAsignarMecRiegoASector = models.BooleanField()
    puedeConfigurarObtencionInfoExterna = models.BooleanField()
    puedeCrearComponenteSensor = models.BooleanField()
    puedeCrearConfiguracionRiego = models.BooleanField()
    puedeCrearSector = models.BooleanField()
    puedeGenerarInformeCruzadoRiegoMedicion = models.BooleanField()
    puedeGenerarInformeEstadoActualSectores = models.BooleanField()
    puedeGenerarInformeEstadoHistoricoSectoresFinca = models.BooleanField()
    puedeGenerarInformeEventoPersonalizado = models.BooleanField()
    puedeGenerarInformeHeladasHistorico = models.BooleanField()
    puedeGenerarInformeRiegoEnEjecucion = models.BooleanField()
    puedeGenerarInformeRiegoPorSectoresHistorico = models.BooleanField()
    puedeGestionarComponenteSensor = models.BooleanField()
    puedeGestionarCultivoSector = models.BooleanField()
    puedeGestionarEventoPersonalizado = models.BooleanField()
    puedeGestionarFinca = models.BooleanField()
    puedeGestionarSector = models.BooleanField()
    puedeGestionarSensores = models.BooleanField()
    puedeGestionarUsuariosFinca = models.BooleanField()
    puedeIniciarODetenerRiegoManualmente = models.BooleanField()
    puedeModificarConfiguracionRiego = models.BooleanField()

    rol = models.ForeignKey(Rol, db_column="OIDRol", related_name="conjuntoPermisos")

    class Meta:
        verbose_name_plural = "Conjuntos de permisos"

    def __str__(self):
        return "Conjunto permisos de " + self.rol.nombreRol

    def as_json(self):
        return dict(
            puedeAsignarComponenteSensor=self.puedeAsignarComponenteSensor,
            puedeAsignarCultivo=self.puedeAsignarCultivo,
            puedeAsignarMecRiegoAFinca=self.puedeAsignarMecRiegoAFinca,
            puedeAsignarMecRiegoASector=self.puedeAsignarMecRiegoASector,
            puedeConfigurarObtencionInfoExterna=self.puedeConfigurarObtencionInfoExterna,
            puedeCrearComponenteSensor=self.puedeCrearComponenteSensor,
            puedeCrearConfiguracionRiego=self.puedeCrearConfiguracionRiego,
            puedeCrearSector=self.puedeCrearSector,
            puedeGenerarInformeCruzadoRiegoMedicion=self.puedeGenerarInformeCruzadoRiegoMedicion,
            puedeGenerarInformeEstadoActualSectores=self.puedeGenerarInformeEstadoActualSectores,
            puedeGenerarInformeEstadoHistoricoSectoresFinca=self.puedeGenerarInformeEstadoHistoricoSectoresFinca,
            puedeGenerarInformeEventoPersonalizado=self.puedeGenerarInformeEventoPersonalizado,
            puedeGenerarInformeHeladasHistorico=self.puedeGenerarInformeHeladasHistorico,
            puedeGenerarInformeRiegoEnEjecucion=self.puedeGenerarInformeRiegoEnEjecucion,
            puedeGenerarInformeRiegoPorSectoresHistorico=self.puedeGenerarInformeRiegoPorSectoresHistorico,
            puedeGestionarComponenteSensor=self.puedeGestionarComponenteSensor,
            puedeGestionarCultivoSector=self.puedeGestionarCultivoSector,
            puedeGestionarEventoPersonalizado=self.puedeGestionarEventoPersonalizado,
            puedeGestionarFinca=self.puedeGestionarFinca,
            puedeGestionarSector=self.puedeGestionarSector,
            puedeGestionarSensores=self.puedeGestionarSensores,
            puedeGestionarUsuariosFinca=self.puedeGestionarUsuariosFinca,
            puedeIniciarODetenerRiegoManualmente=self.puedeIniciarODetenerRiegoManualmente,
            puedeModificarConfiguracionRiego=self.puedeModificarConfiguracionRiego
        )


# MODULO FINCA

class ProveedorInformacionClimaticaFinca(models.Model):
    OIDProveedorInformacionClimaticaFinca = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fechaAltaProveedorInfoClimaticaFinca = models.DateTimeField()
    fechaBajaProveedorInfoClimaticaFinca = models.DateTimeField(null=True)
    frecuencia = models.IntegerField(null=True)
    finca = models.ForeignKey("Finca", db_column="OIDFinca", null=True)
    proveedorInformacionClimatica = models.ForeignKey("ProveedorInformacionClimatica",
                                                      db_column="OIDProveedorInformacionClimatica",
                                                      null=True)


class Finca(models.Model):
    OIDFinca = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    idFinca = models.IntegerField(default=1, unique=True, editable=False)
    direccionLegal = models.CharField(max_length=50)
    logoFinca = models.ImageField(null=True)
    nombre = models.CharField(max_length=50)
    tamanio = models.FloatField()
    ubicacion = models.CharField(max_length=50)

    def __str__(self):
        return str(self.idFinca) + "-" + self.nombre

    def save(self, *args, **kwargs):
        """Get last value of Code and Number from database, and increment before save"""
        if Finca.objects.all().__len__() == 0:
            self.idFinca = 1
            super(Finca, self).save(*args, **kwargs)
        else:
            if Finca.objects.get(idFinca=self.idFinca) == self:
                super(Finca, self).save(*args, **kwargs)
            else:
                ultima_finca = Finca.objects.order_by('-idFinca')[0]
                self.idFinca = ultima_finca.idFinca + 1
                super(Finca, self).save(*args, **kwargs)

    def as_json(self):
        return dict(
            direccionLegal=self.direccionLegal,
            idFinca=self.idFinca,
            nombre=self.nombre,
            tamanio=self.tamanio,
            ubicacion=self.ubicacion
            # logoFinca=self.logoFinca
        )


class EstadoFinca(models.Model):
    OIDFinca = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    descripcionEstadoFinca = models.CharField(max_length=100)
    nombreEstadoFinca = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "_Estados finca"

    def __str__(self):
        return "Estado finca: %s" % self.nombreEstadoFinca


class HistoricoEstadoFinca(models.Model):
    OIDHistoricoEstadoFinca = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fechaFinEstadoFinca = models.DateTimeField(null=True)
    fechaInicioEstadoFinca = models.DateTimeField()

    finca = models.ForeignKey(Finca, db_column="OIDFinca", related_name="historicoEstadoFincaList")
    estadoFinca = models.ForeignKey(EstadoFinca, db_column="OIDEstadoFinca")

    class Meta:
        verbose_name_plural = "Historicos estado fincas"

    def __str__(self):
        if self.fechaFinEstadoFinca:
            return "(Finalizado) " + self.finca.nombre + " - estado: " + self.estadoFinca.nombreEstadoFinca + \
                   " - Creado en fecha: " + str(self.fechaInicioEstadoFinca.date()) + \
                   " - hora: " + str(self.fechaInicioEstadoFinca.time())
        else:
            return self.finca.nombre + " - estado: " + self.estadoFinca.nombreEstadoFinca + \
                   " - Creado en fecha: " + str(self.fechaInicioEstadoFinca.date()) + \
                   " - hora: " + str(self.fechaInicioEstadoFinca.time())


class MecanismoRiegoFinca(models.Model):
    OIDMecanismoRiegoFinca = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    direccionIP = models.CharField(max_length=20)
    fechaInstalacion = models.DateTimeField()
    idMecanismoRiegoFinca = models.IntegerField(default=1, unique=True, editable=False)

    finca = models.ForeignKey(Finca, db_column="OIDFinca")
    tipoMecanismoRiego = models.ForeignKey("TipoMecanismoRiego", db_column="OIDTipoMecanismoRiego", null=True)

    def as_json(self):
        return dict(
            direccionIP=self.direccionIP,
            fechaInstalacion=self.fechaInstalacion,
            idMecanismoRiegoFinca=self.idMecanismoRiegoFinca,
            tipoMecanismoRiego=self.tipoMecanismoRiego.nombreMecanismo
            # imagenUsuario=self.imagenUsuario
        )

    def save(self, *args, **kwargs):
        if MecanismoRiegoFinca.objects.all().__len__() == 0:
                self.idMecanismoRiegoFinca = 1
                super(MecanismoRiegoFinca, self).save(*args, **kwargs)
        else:
            if MecanismoRiegoFinca.objects.get(idMecanismoRiegoFinca=self.idMecanismoRiegoFinca) == self:
                super(MecanismoRiegoFinca, self).save(*args, **kwargs)
            else:
                ultimo_mecanismo = MecanismoRiegoFinca.objects.order_by('-idMecanismoRiegoFinca')[0]
                self.idMecanismoRiegoFinca = ultimo_mecanismo.idMecanismoRiegoFinca + 1
                super(MecanismoRiegoFinca, self).save(*args, **kwargs)


class EstadoMecanismoRiegoFinca(models.Model):
    OIDEstadoMecanismoRiegoFinca = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombreEstadoMecanismoRiegoFinca = models.CharField(max_length=20)
    descripcionEstadoMecanismoRiegoFinca = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "_Estados mecanismo riego finca"

    def __str__(self):
        return "Estado mecanismo riego finca: " + self.nombreEstadoMecanismoRiegoFinca


class HistoricoMecanismoRiegoFinca(models.Model):
    OIDHistoricoMecanismoRiegoFinca = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fechaInicioEstadoMecanismoRiegoFinca = models.DateTimeField(null=True)
    fechaFinEstadoMecanismoRiegoFinca = models.DateTimeField(null=True)
    mecanismo_riego_finca = models.ForeignKey(MecanismoRiegoFinca, db_column="OIDMecanismoRiegoFinca",
                                              related_name="historicoMecanismoRiegoFincaList")
    estado_mecanismo_riego_finca = models.ForeignKey(EstadoMecanismoRiegoFinca,
                                                     db_column="OIDEstadoMecanismoRiegoFinca")

    class Meta:
        verbose_name_plural = "Historicos mecanismos riego finca"

    def __str__(self):
        if self.fechaFinEstadoMecanismoRiegoFinca:
            return "(Finalizado) " + " Finca: " + self.mecanismo_riego_finca.finca.nombre + \
                   " - Tipo mecanismo: " + self.mecanismo_riego_finca.tipoMecanismoRiego.nombreMecanismo + \
                   " - estado: " + self.estado_mecanismo_riego_finca.nombreEstadoMecanismoRiegoFinca + \
                   " - Creado en fecha: " + str(self.fechaInicioEstadoMecanismoRiegoFinca.date()) + \
                   " - hora: " + str(self.fechaInicioEstadoMecanismoRiegoFinca.time())
        else:
            return "Finca: " + self.mecanismo_riego_finca.finca.nombre + \
                   " - Tipo mecanismo: " + self.mecanismo_riego_finca.tipoMecanismoRiego.nombreMecanismo + \
                   " - estado: " + self.estado_mecanismo_riego_finca.nombreEstadoMecanismoRiegoFinca + \
                   " - Creado en fecha: " + str(self.fechaInicioEstadoMecanismoRiegoFinca.date()) + \
                   " - hora: " + str(self.fechaInicioEstadoMecanismoRiegoFinca.time())


# MODULO SECTORES

class Sector(models.Model):
    OIDSector = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    idSector = models.IntegerField(default=1, unique=True, editable=False)
    numeroSector = models.IntegerField()
    nombreSector = models.CharField(max_length=30)
    descripcionSector = models.CharField(max_length=100)
    superficie = models.FloatField()

    finca = models.ForeignKey("Finca", db_column="OIDFinca", related_name="sectorList", null=True)

    def save(self, *args, **kwargs):
        """Get last value of Code and Number from database, and increment before save"""
        if Sector.objects.all().__len__() == 0:
            self.idSector = 1
            super(Sector, self).save(*args, **kwargs)
        else:
            if Sector.objects.get(idSector=self.idSector) == self:
                super(Sector, self).save(*args, **kwargs)
            else:
                ultimo_sector = Sector.objects.order_by('-idSector')[0]
                self.idSector = ultimo_sector.idSector + 1
                super(Sector, self).save(*args, **kwargs)

    def __str__(self):
        return "Sector numero: %d" % self.numeroSector

    def as_json(self):
        return dict(
            idSector=self.idSector,
            numeroSector=self.numeroSector,
            nombreSector=self.nombreSector,
            descripcionSector=self.descripcionSector,
            superficieSector=self.superficie
        )


class Cultivo(models.Model):
    OIDCultivo = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    idCultivo = models.IntegerField(default=1, unique=True, editable=False)
    descripcion = models.CharField(max_length=100)
    nombre = models.CharField(max_length=20)
    fechaPlantacion = models.DateTimeField()
    fechaEliminacion = models.DateTimeField(null=True)
    habilitado = models.BooleanField()

    subtipo_cultivo = models.ForeignKey('SubtipoCultivo', db_column="OIDSubtipoCultivo")
    sector = models.ForeignKey(Sector, db_column="OIDSector")

    def save(self, *args, **kwargs):
        """Get last value of Code and Number from database, and increment before save"""
        if Cultivo.objects.all().__len__() == 0:
            self.idCultivo = 1
            super(Cultivo, self).save(*args, **kwargs)
        else:
            if Cultivo.objects.get(idCultivo=self.idCultivo) == self:
                super(Cultivo, self).save(*args, **kwargs)
            else:
                ultimo_cultivo = Cultivo.objects.order_by('-idCultivo')[0]
                self.idCultivo = ultimo_cultivo.idCultivo + 1
                super(Cultivo, self).save(*args, **kwargs)

    def __str__(self):
        return "Nombre cultivo: %s" % self.nombre

    def as_json(self):
        return dict(
            descripcion=self.descripcion,
            idCultivo=self.idCultivo,
            nombre=self.nombre,
            fechaPlantacion=self.fechaPlantacion,
            fechaEliminacion=self.fechaEliminacion,
            habilitado=self.habilitado,
            subtipo=self.subtipo_cultivo.nombreSubtipo,
            tipo=self.subtipo_cultivo.tipo_cultivo.nombreTipoCultivo
        )


class EstadoSector(models.Model):
    OIDEstadoSector = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    descripcionEstadoSector = models.CharField(max_length=100)
    nombreEstadoSector = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = "_Estados sector"

    def __str__(self):
        return "Estado sector: %s" % self.nombreEstadoSector


class HistoricoEstadoSector(models.Model):
    OIDHistoricoEstadoSector = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fechaFinEstadoSector = models.DateTimeField(null=True)
    fechaInicioEstadoSector = models.DateTimeField()

    estado_sector = models.ForeignKey(EstadoSector, db_column="OIDEstadoSector")
    sector = models.ForeignKey(Sector, db_column="OIDSector", related_name="historicoEstadoSectorList")

    class Meta:
        verbose_name_plural = "Historicos estado sectores"

    def __str__(self):
        if self.fechaFinEstadoSector:
            return "(Finalizado) " + self.sector.nombreSector + " - estado: " + \
                   self.estado_sector.nombreEstadoSector + \
                   " - Creado en fecha: " + str(self.fechaInicioEstadoSector.date()) + \
                   " - hora: " + str(self.fechaInicioEstadoSector.time())
        else:
            return self.sector.nombreSector + " - estado: " + \
                   self.estado_sector.nombreEstadoSector + \
                   " - Creado en fecha: " + str(self.fechaInicioEstadoSector.date()) + \
                   " - hora: " + str(self.fechaInicioEstadoSector.time())


class EstadoMecanismoRiegoFincaSector(models.Model):
    OIDEstadoMecanismoRiegoFincaSector = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    descripcionEstadoMecanismoRiegoFincaSector = models.CharField(max_length=100)
    nombreEstadoMecanismoRiegoFincaSector = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = "_Estados mecanismo riego finca sector"

    def __str__(self):
        return "Estado mecanismo riego finca sector: " + self.nombreEstadoMecanismoRiegoFincaSector


class HistoricoMecanismoRiegoFincaSector(models.Model):
    OIDHistoricoMecanismoRiegoFincaSector = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fechaFinEstadoMecanismoRiegoFincaSector = models.DateTimeField(null=True)
    fechaInicioEstadoMecanismoRiegoFincaSector = models.DateTimeField()

    mecanismo_riego_finca_sector = models.ForeignKey('MecanismoRiegoFincaSector',
                                                     db_column="OIDMecanismoRiegoFincaSector",
                                                     related_name="historicoMecanismoRiegoFincaSector")
    estado_mecanismo_riego_finca_sector = models.ForeignKey(EstadoMecanismoRiegoFincaSector,
                                                            db_column="OIDEstadoMecanismoRiegoFincaSector")

    class Meta:
        verbose_name_plural = "Historicos mecanismos riego finca sector"

    def __str__(self):
        if self.fechaFinEstadoMecanismoRiegoFincaSector:
            return "(Finalizado) " + "Finca: " + self.mecanismo_riego_finca_sector.mecanismoRiegoFinca.finca.nombre + \
                   " - Sector: " + self.mecanismo_riego_finca_sector.sector.nombreSector + \
                   " - Tipo mecanismo: " + self.mecanismo_riego_finca_sector.mecanismoRiegoFinca.\
                tipoMecanismoRiego.nombreMecanismo + \
                   " - estado: " + self.estado_mecanismo_riego_finca_sector.nombreEstadoMecanismoRiegoFincaSector + \
                   " - Creado en fecha: " + str(self.fechaInicioEstadoMecanismoRiegoFincaSector.date()) + \
                   " - hora: " + str(self.fechaInicioEstadoMecanismoRiegoFincaSector.time())
        else:
            return "Finca: " + self.mecanismo_riego_finca_sector.mecanismoRiegoFinca.finca.nombre + \
                   " - Sector: " + self.mecanismo_riego_finca_sector.sector.nombreSector + \
                   " - Tipo mecanismo: " + self.mecanismo_riego_finca_sector.mecanismoRiegoFinca.\
                tipoMecanismoRiego.nombreMecanismo + \
                   " - estado: " + self.estado_mecanismo_riego_finca_sector.nombreEstadoMecanismoRiegoFincaSector + \
                   " - Creado en fecha: " + str(self.fechaInicioEstadoMecanismoRiegoFincaSector.date()) + \
                   " - hora: " + str(self.fechaInicioEstadoMecanismoRiegoFincaSector.time())


class AsignacionSensorComponente(models.Model):
    OIDAsignacionSensorComponente = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fechaAsignacion = models.DateTimeField()
    fechaBaja = models.DateTimeField(null=True)
    sensor = models.ForeignKey('Sensor', db_column="OIDSensor", related_name="asignaciones_list")
    componenteSensor = models.ForeignKey('ComponenteSensor',
                                         db_column="OIDComponenteSensor",
                                         related_name="asignaciones_list")


class HistoricoEstadoComponenteSensor(models.Model):
    OIDHistoricoEstadoComponenteSensor = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fechaFinEstadoComponenteSensor = models.DateTimeField(null=True)
    fechaInicioEstadoComponenteSensor = models.DateTimeField()
    componenteSensor = models.ForeignKey('ComponenteSensor',
                                         db_column="OIDComponenteSensor",
                                         related_name="historico_estado_componente_sensor_list")
    estadoComponenteSensor = models.ForeignKey('EstadoComponenteSensor', db_column="OIDEstadoComponenteSensor")

    class Meta:
        verbose_name_plural = "Historicos estado componentes sensor"

    def __str__(self):
        if self.fechaFinEstadoComponenteSensor:
            return "(Finalizado) " + str(self.componenteSensor.idComponenteSensor) + " - estado: " + \
                   self.estadoComponenteSensor.nombreEstado + \
                   " - Creado en fecha: " + str(self.fechaInicioEstadoComponenteSensor.date()) + \
                   " - hora: " + str(self.fechaInicioEstadoComponenteSensor.time())
        else:
            return str(self.componenteSensor.idComponenteSensor) + " - estado: " + \
                   self.estadoComponenteSensor.nombreEstado + \
                   " - Creado en fecha: " + str(self.fechaInicioEstadoComponenteSensor.date()) + \
                   " - hora: " + str(self.fechaInicioEstadoComponenteSensor.time())


class EstadoComponenteSensor(models.Model):
        OIDEstadoComponenteSensor = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        nombreEstado = models.CharField(max_length=20)
        descripcionEstado = models.CharField(max_length=100)

        class Meta:
            verbose_name_plural = "_Estados componente sensor"

        def __str__(self):
            return "Estado componente: " + self.nombreEstado


class ComponenteSensor(models.Model):
    OIDComponenteSensor = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    idComponenteSensor = models.IntegerField(default=1, unique=True, editable=False)
    modelo = models.CharField(max_length=100, null=True)
    descripcion = models.CharField(max_length=200, null=True)
    cantidadMaximaSensores = models.IntegerField(null=True)
    cantidadSensoresAsignados = models.IntegerField(default=0)
    finca = models.ForeignKey(Finca, db_column="OIDFinca", null=True)

    def save(self, *args, **kwargs):
        """Get last value of Code and Number from database, and increment before save"""
        if ComponenteSensor.objects.all().__len__() == 0:
            self.idComponenteSensor = 1
            super(ComponenteSensor, self).save(*args, **kwargs)
        else:
            if ComponenteSensor.objects.get(idComponenteSensor=self.idComponenteSensor) == self:
                super(ComponenteSensor, self).save(*args, **kwargs)
            else:
                ultimo_componente_sensor = ComponenteSensor.objects.order_by('-idComponenteSensor')[0]
                self.idComponenteSensor = ultimo_componente_sensor.idComponenteSensor + 1
                super(ComponenteSensor, self).save(*args, **kwargs)

    def as_json(self):
        ultimo_historico = self.historico_estado_componente_sensor_list.get(fechaFinEstadoComponenteSensor__isnull=True)
        return dict(
            idComponenteSensor=self.idComponenteSensor,
            modelo=self.modelo,
            descripcion=self.descripcion,
            finca=self.finca.idFinca,
            cantidadMaximaSensores=self.cantidadMaximaSensores,
            cantidadSensoresAsignados=self.cantidadSensoresAsignados,
            estado=ultimo_historico.estadoComponenteSensor.nombreEstado
        )

    def __str__(self):
        return "Componente sensor: " + self.modelo + "-" + str(self.idComponenteSensor)


# MODULO CULTIVOS

class TipoCultivo(models.Model):
    OIDTipoCultivo = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombreTipoCultivo = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=100)
    habilitado = models.BooleanField()
    fechaAltaTipoCultivo = models.DateTimeField()
    fechaBajaTipoCultivo = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Tipos de cultivo"

    def save(self, *args, **kwargs):
        if not self.fechaBajaTipoCultivo:
            self.fechaBajaTipoCultivo = None
        super(TipoCultivo, self).save(*args, **kwargs)

    def __str__(self):
        return "Nombre tipo de cultivo: " + self.nombreTipoCultivo


class SubtipoCultivo(models.Model):
    OIDSubtipoCultivo = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombreSubtipo = models.CharField(max_length=20)
    habilitado = models.BooleanField()
    descripcion = models.CharField(max_length=100)
    tipo_cultivo = models.ForeignKey(TipoCultivo, db_column="OIDTipoCultivo")
    fechaAltaSubtipoCultivo = models.DateTimeField()
    fechaBajaSubtipoCultivo = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Subtipos de cultivo"

    def save(self, *args, **kwargs):
        if not self.fechaBajaSubtipoCultivo:
            self.fechaBajaSubtipoCultivo = None
        super(SubtipoCultivo, self).save(*args, **kwargs)

    def __str__(self):
        if self.tipo_cultivo:
            return "Subtipo cultivo: " + self.nombreSubtipo + " - de tipo cultivo: " + \
                   self.tipo_cultivo.nombreTipoCultivo
        else:
            return "Subtipo cultivo: " + self.nombreSubtipo


class CaracteristicaSubtipo(models.Model):
    OIDCaracteristicaSubtipo = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    atributo = models.CharField(max_length=20)
    comentario = models.CharField(max_length=100)
    valor = models.CharField(max_length=20)

    subtipo_cultivo = models.ForeignKey(SubtipoCultivo, db_column="OIDSubtipoCultivo",
                                        related_name="caracteristicaSubtipoList")


# MODULO RIEGO

class TipoMecanismoRiego(models.Model):
    OIDTipoMecanismoRiego = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombreMecanismo = models.CharField(max_length=30, unique=True)
    descripcion = models.CharField(max_length=200, null=True)
    caudalEstandar = models.FloatField(null=True)
    presionEstandar = models.FloatField(null=True)
    eficiencia = models.FloatField(null=True)
    habilitado = models.BooleanField(default=True)
    fechaAltaTipoMecanismoRiego = models.DateTimeField()
    fechaBajaTipoMecanismoRiego = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Tipos de mecanismos de riego"

    def save(self, *args, **kwargs):
        if not self.fechaBajaTipoMecanismoRiego:
            self.fechaBajaTipoMecanismoRiego = None
        super(TipoMecanismoRiego, self).save(*args, **kwargs)

    def __str__(self):
        return "Tipo mecanismo: " + self.nombreMecanismo

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

    OIDTipoConfiguracionRiego = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    idTipoConfiguracion = models.IntegerField(unique=True, default=1)
    nombre = models.CharField(max_length=20, unique=True)

    class Meta:
        verbose_name_plural = "_Tipos de configuracion de riego"


    def __str__(self):
        return "Tipo de configuracion riego: " + self.nombre

    def save(self, *args, **kwargs):
        """Get last value of Code and Number from database, and increment before save"""
        if TipoConfiguracionRiego.objects.all().__len__() == 0:
            self.idTipoConfiguracion = 1
            super(TipoConfiguracionRiego, self).save(*args, **kwargs)
        else:
            if TipoConfiguracionRiego.objects.get(idTipoConfiguracion=self.idTipoConfiguracion) == self:
                super(TipoConfiguracionRiego, self).save(*args, **kwargs)
            else:
                ultimo_tipo_configuracion = TipoConfiguracionRiego.objects.order_by('-idTipoConfiguracion')[0]
                self.idTipoConfiguracion = ultimo_tipo_configuracion.idTipoConfiguracion + 1
                super(TipoConfiguracionRiego, self).save(*args, **kwargs)

    def save(self):
        "Get last value of Code and Number from database, and increment before save"
        if TipoConfiguracionRiego.objects.all().__len__() == 0:
            self.idTipoConfiguracion = 1
            super(TipoConfiguracionRiego, self).save()
        else:
            if TipoConfiguracionRiego.objects.get(idTipoConfiguracion=self.idTipoConfiguracion) == self:
                super(TipoConfiguracionRiego, self).save()
            else:
                ultimoTipoConfiguracion = TipoConfiguracionRiego.objects.order_by('-idTipoConfiguracion')[0]
                self.idTipoConfiguracion = ultimoTipoConfiguracion.idTipoConfiguracion + 1
                super(TipoConfiguracionRiego, self).save()


class ConfiguracionRiego(models.Model):
    OIDConfiguracionRiego = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_configuracion_riego = models.IntegerField(default=1, unique=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)
    duracionMaxima = models.FloatField()
    fechaCreacion = models.DateTimeField()
    fechaFinalizacion = models.DateTimeField(null=True)

    tipoConfiguracionRiego = models.ForeignKey(TipoConfiguracionRiego, db_column="OIDTipoConfiguracionRiego")
    mecanismoRiegoFincaSector = models.ForeignKey('MecanismoRiegoFincaSector',
                                                  db_column="OIDMecanismoRiegoFincaSector",
                                                  null=True)

    def __str__(self):
        return str(self.id_configuracion_riego) + ": " + self.nombre

    def save(self, *args, **kwargs):
        """Crear o incrementar id_configuracion_riego"""
        if ConfiguracionRiego.objects.all().__len__() == 0:
            self.id_configuracion_riego = 1
            super(ConfiguracionRiego, self).save(*args, **kwargs)
        else:
            if ConfiguracionRiego.objects.get(id_configuracion_riego=self.id_configuracion_riego) == self:
                super(ConfiguracionRiego, self).save(*args, **kwargs)
            else:
                ultima_configuracion_riego = ConfiguracionRiego.objects.order_by('-id_configuracion_riego')[0]
                self.id_configuracion_riego = ultima_configuracion_riego.id_configuracion_riego + 1
                super(ConfiguracionRiego, self).save(*args, **kwargs)

    def as_json(self):
        fecha_creacion_date = ""
        fecha_finalizacion_date = ""
        if self.fechaCreacion:
            fecha_creacion_date = self.fechaCreacion.date()
        if self.fechaFinalizacion:
            fecha_finalizacion_date = self.fechaFinalizacion.date()

        ultimo_estado_historico = HistoricoEstadoConfiguracionRiego.objects.get(
            configuracion_riego=self, fechaFinEstadoConfiguracionRiego=None)

        return dict(
            idConfiguracionRiego=self.id_configuracion_riego,
            nombre=self.nombre,
            descripcion=self.descripcion,
            duracionMaxima=self.duracionMaxima,
            fechaCreacion=fecha_creacion_date,
            fechaFinalizacion=fecha_finalizacion_date,
            tipoConfiguracionRiego=self.tipoConfiguracionRiego.nombre,
            mecanismoRiegoFincaSector=self.mecanismoRiegoFincaSector.idMecanismoRiegoFincaSector,
            estado_configuracion=ultimo_estado_historico.estado_configuracion_riego.nombreEstadoConfiguracionRiego
        )


class EstadoConfiguracionRiego(models.Model):
    OIDEstadoConfiguracionRiego = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombreEstadoConfiguracionRiego = models.CharField(max_length=20, unique=True)
    descripcionEstadoConfiguracionRiego = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "_Estados configuracion riego"

    def __str__(self):
        return "Estado configuracion riego: " + self.nombreEstadoConfiguracionRiego


class HistoricoEstadoConfiguracionRiego(models.Model):
    OIDHistoricoEstadoConfiguracionRiego = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fechaFinEstadoConfiguracionRiego = models.DateTimeField(null=True)
    fechaInicioEstadoConfiguracionRiego = models.DateTimeField()

    configuracion_riego = models.ForeignKey(ConfiguracionRiego,
                                            db_column="OIDConfiguracionRiego",
                                            related_name="historicoEstadoConfiguracionRiegoList")
    estado_configuracion_riego = models.ForeignKey(EstadoConfiguracionRiego,
                                                   db_column="OIDEstadoConfiguracionRiego")

    class Meta:
        verbose_name_plural = "Historicos estado configuraciones riego"

    def __str__(self):
        if self.fechaFinEstadoConfiguracionRiego:
            return "(Finalizado) " + self.configuracion_riego.nombre + \
                   " - Finca: " + self.configuracion_riego.mecanismoRiegoFincaSector. \
                       mecanismoRiegoFinca.finca.nombre + \
                   " - Sector: " + self.configuracion_riego.mecanismoRiegoFincaSector.sector.nombreSector + \
                   " - estado: " + self.estado_configuracion_riego.nombreEstadoConfiguracionRiego + \
                   " - Creado en fecha: " + str(self.fechaInicioEstadoConfiguracionRiego.date()) + \
                   " - hora: " + str(self.fechaInicioEstadoConfiguracionRiego.time())
        else:
            return self.configuracion_riego.nombre + \
                   " - Finca: " + \
                   self.configuracion_riego.mecanismoRiegoFincaSector.mecanismoRiegoFinca.finca.nombre + \
                   " - Sector: " + self.configuracion_riego.mecanismoRiegoFincaSector.sector.nombreSector + \
                   " - estado: " + self.estado_configuracion_riego.nombreEstadoConfiguracionRiego + \
                   " - Creado en fecha: " + str(self.fechaInicioEstadoConfiguracionRiego.date()) + \
                   " - hora: " + str(self.fechaInicioEstadoConfiguracionRiego.time())


class EstadoEjecucionRiego(models.Model):
    OIDEstadoEjecucionRiego = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombreEstadoEjecucionRiego = models.CharField(max_length=20, unique=True)
    descripcionEstadoEjecucionRiego = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "_Estados ejecucion riego"

    def __str__(self):
        return "Estado ejecucion riego: " + self.nombreEstadoEjecucionRiego


class MecanismoRiegoFincaSector(models.Model):
    OIDMecanismoRiegoFincaSector = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    idMecanismoRiegoFincaSector = models.IntegerField(default=1, unique=True)
    caudal = models.FloatField()
    presion = models.FloatField()

    mecanismoRiegoFinca = models.ForeignKey(MecanismoRiegoFinca, db_column="OIDMecanismoRiegoFinca",
                                            related_name="mecanismoRiegoSectorList", null=True)
    sector = models.ForeignKey(Sector, db_column="OIDSector", related_name="mecanismoRiegoFincaSector", null=True)

    def __str__(self):
        return self.mecanismoRiegoFinca.tipoMecanismoRiego.nombreMecanismo + "(Finca: " + \
               str(self.mecanismoRiegoFinca.finca.idFinca) + ", sector: " + str(self.sector.idSector) + ")"

    def save(self, *args, **kwargs):
        """Get last value of Code and Number from database, and increment before save"""
        if MecanismoRiegoFincaSector.objects.all().__len__() == 0:
            self.idMecanismoRiegoFincaSector = 1
            super(MecanismoRiegoFincaSector, self).save(*args, **kwargs)
        else:
            if MecanismoRiegoFincaSector.objects.get(idMecanismoRiegoFincaSector=self.idMecanismoRiegoFincaSector) == \
                    self:
                super(MecanismoRiegoFincaSector, self).save(*args, **kwargs)
            else:
                ultimo_mecanismo_finca_riego_sector = \
                    MecanismoRiegoFincaSector.objects.order_by('-idMecanismoRiegoFincaSector')[0]
                self.idMecanismoRiegoFincaSector = ultimo_mecanismo_finca_riego_sector.idMecanismoRiegoFincaSector + 1
                super(MecanismoRiegoFincaSector, self).save(*args, **kwargs)

    def as_json(self):
        return dict(
            idMecanismoRiegoFincaSector=self.idMecanismoRiegoFincaSector,
            caudal=self.caudal,
            presion=self.presion,
            sector=self.sector.numeroSector,
            mecanismoRiegoFinca=self.mecanismoRiegoFinca.idMecanismoRiegoFinca,
            nombreTipoMecanismo=self.mecanismoRiegoFinca.tipoMecanismoRiego.nombreMecanismo,
            idFinca=self.mecanismoRiegoFinca.finca.idFinca
        )


class EjecucionRiego(models.Model):
    oid_ejecucion_riego = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    detalle = models.CharField(max_length=100)
    duracion_parcial = models.FloatField(default=0)
    fecha_hora_ultima_pausa = models.DateTimeField(null=True)
    fecha_hora_ultimo_reinicio = models.DateTimeField(null=True)
    fecha_hora_finalizacion = models.DateTimeField(null=True)
    fecha_hora_final_programada = models.DateTimeField(null=True)
    fecha_hora_inicio = models.DateTimeField()
    fecha_hora_inicio_programada = models.DateTimeField(null=True)

    configuracion_riego = models.ForeignKey(ConfiguracionRiego, db_column="OIDConfiguracionRiego", null=True)
    estado_ejecucion_riego = models.ForeignKey(EstadoEjecucionRiego, db_column="OIDEstadoEjecucionRiego")
    mecanismo_riego_finca_sector = models.ForeignKey(MecanismoRiegoFincaSector,
                                                     db_column="OIDMecanismoRiegoFincaSector",
                                                     related_name="ejecucionRiegoList")

    def __str__(self):
        return "Mecanismo riego finca sensor: " + \
               str(self.mecanismo_riego_finca_sector.idMecanismoRiegoFincaSector) + " detalle: " + self.detalle

    def as_json(self):
        # Se calcula duracion
        estado_pausado = EstadoEjecucionRiego.objects.get(nombreEstadoEjecucionRiego="pausado")

        if self.estado_ejecucion_riego == estado_pausado:
            duracion_total = self.duracion_parcial

        else:
            if self.fecha_hora_finalizacion:
                if self.fecha_hora_ultimo_reinicio:
                    duracion = (self.fecha_hora_finalizacion - self.fecha_hora_ultimo_reinicio).seconds
                else:
                    duracion = (self.fecha_hora_finalizacion - self.fecha_hora_inicio).seconds

            else:
                if self.fecha_hora_ultimo_reinicio:
                    duracion = (datetime.now(pytz.utc) - self.fecha_hora_ultimo_reinicio).seconds
                else:
                    duracion = (datetime.now(pytz.utc) - self.fecha_hora_inicio).seconds

            duracion_total = duracion + self.duracion_parcial

        # Se calcula cantidad de agua utilizada
        cantidad_agua_utilizada = self.mecanismo_riego_finca_sector.caudal * (duracion_total / 60.0)

        # Si existe, se define id configuracion riego
        id_configuracion_riego = None
        if self.configuracion_riego:
            id_configuracion_riego = self.configuracion_riego.id_configuracion_riego

        return dict(
            mecanismoRiegoFincaSector=self.mecanismo_riego_finca_sector.idMecanismoRiegoFincaSector,
            configuracion_riego=id_configuracion_riego,
            estado_ejecucion_riego=self.estado_ejecucion_riego.nombreEstadoEjecucionRiego,
            cantidadAguaUtilizadaLitros=cantidad_agua_utilizada,
            detalle=self.detalle,
            duracionActualMinutos=duracion_total/60.0,
            duracionActualSegundos=duracion_total,
            fechaHoraFinalizacion=self.fecha_hora_finalizacion,
            fechaHoraFinalProgramada=self.fecha_hora_final_programada,
            fechaHoraInicio=self.fecha_hora_inicio,
            fechaHoraInicioProgramada=self.fecha_hora_inicio_programada
        )


class CriterioRiego(models.Model):
    OIDCriterioRiego = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_criterio_riego = models.IntegerField(default=1, unique=True, editable=False)
    fecha_creacion_criterio = models.DateTimeField()
    fecha_eliminacion_criterio = models.DateTimeField(null=True)
    nombre = models.CharField(max_length=50, null=True)
    descripcion = models.CharField(max_length=100, null=True)

    configuracionRiegoInicial = models.ForeignKey(ConfiguracionRiego,
                                                  on_delete=models.CASCADE,
                                                  db_column="OIDConfiguracionRiegoInicial",
                                                  related_name="criterioRiegoInicial",
                                                  null=True)
    configuracionRiegoFinal = models.ForeignKey(ConfiguracionRiego,
                                                on_delete=models.CASCADE,
                                                db_column="OIDConfiguracionRiegoFinal",
                                                related_name="criterioRiegoFinal",
                                                null=True)

    objects = InheritanceManager()

    def __str__(self):
        if self.configuracionRiegoInicial and self.configuracionRiegoFinal:
            return "id criterio riego: " + str(self.id_criterio_riego) + \
                   " - Configuracion riego inicial de: " + self.configuracionRiegoInicial.nombre + \
                   " - Configuracion riego final de: " + self.configuracionRiegoFinal.nombre
        elif self.configuracionRiegoInicial:
            return "id criterio riego: " + str(self.id_criterio_riego) + \
                   " - Configuracion riego inicial de: " + self.configuracionRiegoInicial.nombre
        elif self.configuracionRiegoFinal:
            return "id criterio riego: " + str(self.id_criterio_riego) + \
                   " - Configuracion riego final de: " + self.configuracionRiegoFinal.nombre
        else:
            return "id criterio riego: " + str(self.id_criterio_riego)

    def save(self, *args, **kwargs):
        """Crear o incrementar id_criterio_riego"""
        if CriterioRiego.objects.all().__len__() == 0:
            self.id_criterio_riego = 1
            super(CriterioRiego, self).save(*args, **kwargs)
        else:
            if CriterioRiego.objects.get_subclass(id_criterio_riego=self.id_criterio_riego) == self:
                super(CriterioRiego, self).save(*args, **kwargs)
            else:
                ultimo_criterio_riego = CriterioRiego.objects.order_by('-id_criterio_riego')[0]
                self.id_criterio_riego = ultimo_criterio_riego.id_criterio_riego + 1
                super(CriterioRiego, self).save(*args, **kwargs)


class CriterioRiegoPorMedicion(CriterioRiego):
    valor = models.FloatField(default=0)
    operador = models.IntegerField(default=0)
    tipo_medicion = models.ForeignKey('TipoMedicion', db_column="OIDTipoMedicion",
                                      related_name="criterios_riego_medicion_list", null=True)

    def as_json(self):
        fecha_creacion_date = ""
        if self.fecha_creacion_criterio:
            fecha_creacion_date = self.fecha_creacion_criterio.date()

        if self.operador == 0:
            operador_string = 'Menor o igual'
        elif self.operador == 1:
            operador_string = 'Mayor o igual'
        else:
            operador_string = 'Operador incorrecto'

        return dict(
            id_criterio_riego=self.id_criterio_riego,
            tipo_criterio_riego="criterio_riego_medicion",
            nombre=self.nombre,
            descripcion=self.descripcion,
            fechaCreacionCriterio=fecha_creacion_date,
            valor=self.valor,
            operador=operador_string,
            tipoMedicion=self.tipo_medicion.nombreTipoMedicion,
            unidadMedicion=self.tipo_medicion.unidadMedicion
        )


class CriterioRiegoVolumenAgua(CriterioRiego):
    volumen = models.FloatField()

    def as_json(self):
        fecha_creacion_date = ""
        if self.fecha_creacion_criterio:
            fecha_creacion_date = self.fecha_creacion_criterio.date()

        return dict(
            id_criterio_riego=self.id_criterio_riego,
            nombre=self.nombre,
            tipo_criterio_riego="criterio_riego_volumen_agua",
            descripcion=self.descripcion,
            fechaCreacionCriterio=fecha_creacion_date,
            volumen=self.volumen
        )


class CriterioRiegoPorHora(CriterioRiego):
    hora = models.DateTimeField()
    numeroDia = models.IntegerField()

    def as_json(self):
        fecha_creacion_date = ""
        if self.fecha_creacion_criterio:
            fecha_creacion_date = self.fecha_creacion_criterio.date()

        hora_argentina = self.hora.astimezone(pytz.timezone('America/Argentina/Buenos_Aires'))

        return dict(
            id_criterio_riego=self.id_criterio_riego,
            nombre=self.nombre,
            tipo_criterio_riego="criterio_riego_hora",
            descripcion=self.descripcion,
            fechaCreacionCriterio=fecha_creacion_date,
            hora=hora_argentina.strftime('%H:%M'),
            numeroDia=self.numeroDia
        )


# MODULO SENSORES

class TipoMedicion(models.Model):
    OIDTipoMedicion = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    idTipoMedicion = models.IntegerField(default=1, unique=True, editable=False)
    nombreTipoMedicion = models.CharField(max_length=20)
    unidadMedicion = models.CharField(max_length=20)
    habilitado = models.BooleanField()
    fechaAltaTipoMedicion = models.DateTimeField()
    fechaBajaTipoMedicion = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "_Tipos de mediciones"

    def save(self, *args, **kwargs):
        """Get last value of Code and Number from database, and increment before save"""
        if TipoMedicion.objects.all().__len__() == 0:
            self.idTipoMedicion = 1
            super(TipoMedicion, self).save(*args, **kwargs)
        else:
            if TipoMedicion.objects.get(idTipoMedicion=self.idTipoMedicion) == self:
                super(TipoMedicion, self).save(*args, **kwargs)
            else:
                ultimo_tipo_medicion = TipoMedicion.objects.order_by('-idTipoMedicion')[0]
                self.idTipoMedicion = ultimo_tipo_medicion.idTipoMedicion + 1
                super(TipoMedicion, self).save(*args, **kwargs)

    def as_json(self):
        return dict(
            idTipoMedicion=self.idTipoMedicion,
            nombreTipoMedicion=self.nombreTipoMedicion,
            unidadMedicion=self.unidadMedicion,
            habilitado=self.habilitado,
            fechaAltaTipoMedicion=self.fechaAltaTipoMedicion,
            fechaBajaTipoMedicion=self.fechaBajaTipoMedicion
        )

    def __str__(self):
        return "Tipo medicion: " + self.nombreTipoMedicion


class Sensor(models.Model):
    OIDSensor = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    idSensor = models.IntegerField(default=1, unique=True, editable=False)
    fechaAltaSensor = models.DateTimeField()
    fechaBajaSensor = models.DateTimeField(null=True)
    habilitado = models.BooleanField()
    modelo = models.CharField(max_length=20)
    tipoMedicion = models.ForeignKey('TipoMedicion', db_column="OIDTipoMedicion", null=True)
    finca = models.ForeignKey('Finca', db_column="OIDFinca", null=True)

    def save(self, *args, **kwargs):
        """Get last value of Code and Number from database, and increment before save"""
        if Sensor.objects.all().__len__() == 0:
            self.idSensor = 1
            super(Sensor, self).save(*args, **kwargs)
        else:
            if Sensor.objects.get(idSensor=self.idSensor) == self:
                super(Sensor, self).save(*args, **kwargs)
            else:
                ultimo_sensor = Sensor.objects.order_by('-idSensor')[0]
                self.idSensor = ultimo_sensor.idSensor + 1
                super(Sensor, self).save(*args, **kwargs)

    def as_json(self):
        return dict(
            idSensor=str(self.idSensor),
            fechaAltaSensor=self.fechaAltaSensor,
            fechaBajaSensor=self.fechaBajaSensor,
            habilitado=str(self.habilitado),
            modelo=str(self.modelo),
            tipoMedicion=self.tipoMedicion.nombreTipoMedicion
        )


class ComponenteSensorSector(models.Model):
    OIDComponenteSensorSector = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    idComponenteSensorSector = models.IntegerField(default=1, unique=True, editable=False)
    habilitado = models.BooleanField()

    sector = models.ForeignKey(Sector, db_column="OIDSector", null=True)
    componente_sensor = models.ForeignKey(ComponenteSensor, db_column="OIDComponenteSensor",
                                          related_name="componenteSensorSectorList", null=True)

    def save(self, *args, **kwargs):
        """Get last value of Code and Number from database, and increment before save"""
        if ComponenteSensorSector.objects.all().__len__() == 0:
            self.idComponenteSensorSector = 1
            super(ComponenteSensorSector, self).save(*args, **kwargs)
        else:
            if ComponenteSensorSector.objects.get(idComponenteSensorSector=self.idComponenteSensorSector) == self:
                super(ComponenteSensorSector, self).save(*args, **kwargs)
            else:
                ultimo_componente_sensor_sector = \
                    ComponenteSensorSector.objects.order_by('-idComponenteSensorSector')[0]
                self.idComponenteSensorSector = ultimo_componente_sensor_sector.idComponenteSensorSector + 1
                super(ComponenteSensorSector, self).save(*args, **kwargs)


class HistoricoEstadoComponenteSensorSector(models.Model):
    OIDHistoricoEstadoComponenteSensorSector = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fechaAltaComponenteSensorSector = models.DateTimeField()
    fechaBajaComponenteSensorSector = models.DateTimeField(null=True)
    componenteSensorSector = models.ForeignKey('ComponenteSensorSector',
                                               db_column="OIDComponenteSensorSector",
                                               related_name="historicoEstadoComponenteSensorSector")
    estadoComponenteSensorSector = models.ForeignKey('EstadoComponenteSensorSector',
                                                     db_column="OIDEstadoComponenteSensorSector")

    class Meta:
        verbose_name_plural = "Historicos estado componentes sensor sector"

    def __str__(self):
        if self.fechaBajaComponenteSensorSector:
            return "(Finalizado) " + str(self.componenteSensorSector.idComponenteSensorSector) + \
                   " - Finca: " + self.componenteSensorSector.sector.finca.nombre + \
                   " - Sector: " + self.componenteSensorSector.sector.nombreSector + \
                   " - estado: " + self.estadoComponenteSensorSector.nombreEstadoComponenteSensorSector + \
                   " - Creado en fecha: " + str(self.fechaAltaComponenteSensorSector.date()) + \
                   " - hora: " + str(self.fechaAltaComponenteSensorSector.time())
        else:
            return str(self.componenteSensorSector.idComponenteSensorSector) + \
                   " - Finca: " + self.componenteSensorSector.sector.finca.nombre + \
                   " - Sector: " + self.componenteSensorSector.sector.nombreSector + \
                   " - estado: " + self.estadoComponenteSensorSector.nombreEstadoComponenteSensorSector + \
                   " - Creado en fecha: " + str(self.fechaAltaComponenteSensorSector.date()) + \
                   " - hora: " + str(self.fechaAltaComponenteSensorSector.time())


class EstadoComponenteSensorSector(models.Model):
    OIDEstadoComponenteSensorSector = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombreEstadoComponenteSensorSector = models.CharField(max_length=20)
    descripcionEstadoComponenteSensorSector = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "_Estados componente sensor sector"

    def __str__(self):
        return "Estado componente sensor sector: " + self.nombreEstadoComponenteSensorSector


class MedicionCabecera(models.Model):
    OIDMedicionCabecera = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fechaYHora = models.DateTimeField()
    nroMedicion = models.IntegerField(unique=True, default=1)
    componenteSensorSector = models.ForeignKey("ComponenteSensorSector", db_column="OIDComponenteSensorSector",
                                               related_name="medicionCabeceraList", null=True)

    def save(self, *args, **kwargs):
        """Get last value of Code and Number from database, and increment before save"""
        if MedicionCabecera.objects.all().__len__() == 0:
            self.nroMedicion = 1
            super(MedicionCabecera, self).save(*args, **kwargs)
        else:
            if MedicionCabecera.objects.get(nroMedicion=self.nroMedicion) == self:
                super(MedicionCabecera, self).save(*args, **kwargs)
            else:
                ultima_medicion_cabecera = MedicionCabecera.objects.order_by('-nroMedicion')[0]
                self.nroMedicion = ultima_medicion_cabecera.nroMedicion + 1
                super(MedicionCabecera, self).save(*args, **kwargs)

    def as_json(self):
        return dict(
            nro_medicion=self.nroMedicion,
            fecha_y_hora=self.fechaYHora,
            lista_mediciones_detalle=[medicion.as_json() for medicion in self.medicionDetalleList.all()]
        )


class MedicionDetalle(models.Model):
    OIDMedicionDetalle = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nroRenglon = models.IntegerField()
    valor = models.FloatField()
    medicionCabecera = models.ForeignKey(MedicionCabecera, db_column="OIDMedicionCabecera",
                                         related_name="medicionDetalleList")
    tipoMedicion = models.ForeignKey("TipoMedicion", db_column="OIDTipoMedicion", null=True)

    def as_json(self):
        return dict(
            nro_renglon=self.nroRenglon,
            valor=self.valor,
            tipo_medicion=self.tipoMedicion.nombreTipoMedicion
        )


# MODULO EVENTOS

class MedicionEvento(models.Model):
    OIDMedicionEvento = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # idMedicionEvento = models.IntegerField(default=1, unique=True, editable=False)
    valorMaximo = models.FloatField()
    valorMinimo = models.FloatField()
    # class Meta:
    #     ordering = ['valorMinimo']
    #     abstract = True# CON ESTO HACEMOS Q LA CLASE SEA ABSTRACTA

    configuracionEventoPersonalizado = models.ForeignKey('ConfiguracionEventoPersonalizado',
                                                         db_column="OIDConfiguracionEventoPersonalizado",
                                                         related_name="medicionEventoList")
    objects = InheritanceManager()

    # def save(self, *args, **kwargs):
    #     """Crear o incrementar id_criterio_riego"""
    #     if MedicionEvento.objects.all().__len__() == 0:
    #         self.idMedicionEvento = 1
    #         super(MedicionEvento, self).save(*args, **kwargs)
    #     else:
    #         if MedicionEvento.objects.get_subclass(idMedicionEvento=self.idMedicionEvento) == self:
    #             super(MedicionEvento, self).save(*args, **kwargs)
    #         else:
    #             ultimaMedicionEvento = MedicionEvento.objects.order_by('-idMedicionEvento')[0]
    #             self.idMedicionEvento = ultimaMedicionEvento.idMedicionEvento+ 1
    #             super(MedicionEvento, self).save(*args, **kwargs)


class MedicionFuenteInterna(MedicionEvento):
    # RECIBE COMO PARAMETRO A LA CLASE MEDICION EVENTO PORQUE HEREDA DE ELLA
    # class Meta(MedicionEvento.Meta):
    #     db_table = "MedicionFuenteInterna"
    tipoMedicion = models.ForeignKey('TipoMedicion', db_column="OIDTipoMedicion")

    def as_json(self):
        return dict(
            valor_maximo=self.valorMaximo,
            valor_minimo=self.valorMinimo,
            tipo_medicion=self.tipoMedicion.nombreTipoMedicion,
            unidad_medicion=self.tipoMedicion.unidadMedicion
        )


class ConfiguracionEventoPersonalizado(models.Model):
    OIDConfiguracionEventoPersonalizado = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    idConfiguracion = models.IntegerField(unique=True, default=1, editable=False)
    nombre = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=100)
    notificacionActivada = models.BooleanField()
    fechaAltaConfiguracionEventoPersonalizado = models.DateTimeField()
    fechaBajaConfiguracionEventoPersonalizado = models.DateTimeField(null=True)
    fechaHoraCreacion = models.DateTimeField()
    activado = models.BooleanField(default=False)

    sectorList = models.ManyToManyField(Sector)

    def save(self, *args, **kwargs):
        """Get last value of Code and Number from database, and increment before save"""
        if ConfiguracionEventoPersonalizado.objects.all().__len__() == 0:
            self.idConfiguracion = 1
            super(ConfiguracionEventoPersonalizado, self).save(*args, **kwargs)
        else:
            if ConfiguracionEventoPersonalizado.objects.get(idConfiguracion=self.idConfiguracion) == self:
                super(ConfiguracionEventoPersonalizado, self).save(*args, **kwargs)
            else:
                ultima_configuracion_evento_personalizado = \
                    ConfiguracionEventoPersonalizado.objects.order_by('-idConfiguracion')[0]
                self.idConfiguracion = ultima_configuracion_evento_personalizado.idConfiguracion + 1
                super(ConfiguracionEventoPersonalizado, self).save(*args, **kwargs)

    def __str__(self):
        return "Evento: " + self.nombre


class EventoPersonalizado(models.Model):
    OIDEventoPersonalizado = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nroEvento = models.IntegerField(default=1, unique=True)
    fechaHora = models.DateTimeField()
    sector = models.ForeignKey(Sector, db_column="OIDSector", null=True)
    configuracion_evento_personalizado = models.ForeignKey(ConfiguracionEventoPersonalizado,
                                                           db_column="OIDConfiguracionEventoPersonalizado")

    def save(self, *args, **kwargs):
        """Get last value of Code and Number from database, and increment before save"""
        if EventoPersonalizado.objects.all().__len__() == 0:
            self.nroEvento = 1
            super(EventoPersonalizado, self).save(*args, **kwargs)
        else:
            if EventoPersonalizado.objects.get(nroEvento=self.nroEvento) == self:
                super(EventoPersonalizado, self).save(*args, **kwargs)
            else:
                ultimo_evento_personalizado = EventoPersonalizado.objects.order_by('-nroEvento')[0]
                self.nroEvento = ultimo_evento_personalizado.nroEvento + 1
                super(EventoPersonalizado, self).save(*args, **kwargs)

    def as_json(self):
        return dict(
            nroEvento=self.nroEvento,
            fechaHora=self.fechaHora,
            numeroSector=self.sector.numeroSector
        )


# MODULO INFORMACION EXTERNA

class TipoMedicionClimatica(models.Model):
    OIDTipoMedicionClimatica = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    idTipoMedicionClimatica = models.IntegerField(unique=True, default=1, editable=False)
    nombreTipoMedicionClimatica = models.CharField(unique=True, max_length=30)
    unidadMedicion = models.CharField(max_length=20, null=True)
    habilitada = models.BooleanField()
    fechaAltaTipoMedicionClimatica = models.DateTimeField()
    fechaBajaTipoMedicionClimatica = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "_Tipos de mediciones climaticas"

    def save(self, *args, **kwargs):
        """Get last value of Code and Number from database, and increment before save"""
        if TipoMedicionClimatica.objects.all().__len__() == 0:
            self.idTipoMedicionClimatica = 1
            super(TipoMedicionClimatica, self).save(*args, **kwargs)
        else:
            if TipoMedicionClimatica.objects.get(idTipoMedicionClimatica=self.idTipoMedicionClimatica) == self:
                super(TipoMedicionClimatica, self).save(*args, **kwargs)
            else:
                ultimo_tipo_medicion_climatica = TipoMedicionClimatica.objects.order_by('-idTipoMedicionClimatica')[0]
                self.idTipoMedicionClimatica = ultimo_tipo_medicion_climatica.idTipoMedicionClimatica + 1
                super(TipoMedicionClimatica, self).save(*args, **kwargs)

    def as_json(self):
        return dict(
            idTipoMedicionClimatica=self.idTipoMedicionClimatica,
            nombreTipoMedicionClimatica=self.nombreTipoMedicionClimatica,
            unidadMedicion=self.unidadMedicion,
            fechaAltaTipoMedicionClimatica=self.fechaAltaTipoMedicionClimatica,
            fechaBajaTipoMedicionClimatica=self.fechaBajaTipoMedicionClimatica,
            habilitada=self.habilitada
        )

    def __str__(self):
        return "Tipo de medicion: " + self.nombreTipoMedicionClimatica


class ProveedorInformacionClimatica(models.Model):
    OIDProveedorInformacionClimatica = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    nombreProveedor = models.CharField(max_length=20, unique=True)
    habilitado = models.BooleanField()
    urlAPI = models.CharField(max_length=150, null=True)
    apiKey = models.CharField(max_length=150, null=True)
    frecuenciaMaxPosible = models.IntegerField(null=True)
    tipoMedicionClimatica = models.ManyToManyField(TipoMedicionClimatica)
    fechaAltaProveedorInfoClimatica = models.DateTimeField()
    fechaBajaProveedorInfoClimatica = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "_Proveedores informacion climatica"

    def save(self, *args, **kwargs):
        if not self.fechaBajaProveedorInfoClimatica:
            self.fechaBajaProveedorInfoClimatica = None
        super(ProveedorInformacionClimatica, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombreProveedor

    def as_json(self):
        self.lista_tipo_medicion_json = []
        for tipo_medicion in self.tipoMedicionClimatica.all():
            self.lista_tipo_medicion_json.append(tipo_medicion.as_json())

        return dict(
            nombreProveedor=self.nombreProveedor,
            habilitado=self.habilitado,
            listatipoMedicion=self.lista_tipo_medicion_json,
            frecuenciaMaxPosible=self.frecuenciaMaxPosible,
            urlAPI=self.urlAPI
        )


class MedicionEstadoExterno(MedicionEvento):
    # HERENCIA
    tipoMedicion = models.ForeignKey(TipoMedicionClimatica, db_column="OIDTipoMedicionClimatica")
    # class Meta(MedicionEvento.Meta):
    #     db_table = "MedicionEstadoExterno"

    def as_json(self):
        return dict(
            valor_maximo=self.valorMaximo,
            valor_minimo=self.valorMinimo,
            tipo_medicion=self.tipoMedicion.nombreTipoMedicionClimatica,
            unidad_medicion=self.tipoMedicion.unidadMedicion

        )


class MedicionInformacionClimaticaCabecera(models.Model):
    OIDMedicionInformacionClimaticaCabecera = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    nroMedicion = models.IntegerField(unique=True, default=1, editable=False)
    fechaHora = models.DateTimeField()

    proveedor_informacion_climatica_externa = models.ForeignKey(ProveedorInformacionClimaticaFinca,
                                                                db_column="OIDProveedorInformacionClimaticaFinca",
                                                                related_name="medicionInformacionClimaticaCabeceraList")

    def save(self, *args, **kwargs):
        """Get last value of Code and Number from database, and increment before save"""
        if MedicionInformacionClimaticaCabecera.objects.all().__len__() == 0:
            self.nroMedicion = 1
            super(MedicionInformacionClimaticaCabecera, self).save(*args, **kwargs)
        else:
            if MedicionInformacionClimaticaCabecera.objects.get(nroMedicion=self.nroMedicion) == self:
                super(MedicionInformacionClimaticaCabecera, self).save(*args, **kwargs)
            else:
                ultima_medicion_cabecera = \
                    MedicionInformacionClimaticaCabecera.objects.order_by('-nroMedicion')[0]
                self.nroMedicion = ultima_medicion_cabecera.nroMedicion + 1
                super(MedicionInformacionClimaticaCabecera, self).save(*args, **kwargs)

    def as_json(self):
        return dict(
            nroMedicion=self.nroMedicion,
            fechaHora=self.fechaHora,
            proveedorInformacion=self.proveedor_informacion_climatica_externa.proveedorInformacionClimatica.
            nombreProveedor,
            mediciones_detalles=[medicion.as_json() for medicion in self.medicionInformacionClimaticaDetalle.all()]
        )


class MedicionInformacionClimaticaDetalle(models.Model):
    OIDMedicionInformacionClimaticaDetalle = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    nroRenglon = models.IntegerField()
    valor = models.FloatField()

    medicion_informacion_climatica_cabecera = models.ForeignKey(MedicionInformacionClimaticaCabecera,
                                                                db_column="OIDMedicionInformacionClimaticaCabecera",
                                                                related_name="medicionInformacionClimaticaDetalle")
    tipo_medicion_climatica = models.ForeignKey(TipoMedicionClimatica, db_column="OIDTipoMedicionClimatica")

    def as_json(self):
        return dict(
            nroRenglon=self.nroRenglon,
            valor=self.valor,
            tipoMedicionClimatica=self.tipo_medicion_climatica.nombreTipoMedicionClimatica
        )
