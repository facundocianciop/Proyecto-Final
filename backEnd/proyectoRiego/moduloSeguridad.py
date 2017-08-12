import uuid
from django.db import models
from . import moduloFinca
class Usuario(models.Model):
    OIDUsuario = models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    usuario=models.CharField(max_length=30)
    nombre=models.CharField(max_length=30)
    apellido=models.CharField(max_length=30)
    cuit=models.CharField(max_length=15)
    dni=nombre=models.IntegerField(max_length=10)
    domicilio=models.CharField(max_length=50)
    email=models.CharField(max_length=30)
    fechaNacimiento=models.DateField()
    imagenUsuario=models.ImageField()
    #LAS RELACIONES CON OTRAS CLASES LAS SEPARE UN RENGLON
    OIDEstadoUsuario=models.ForeignKey(EstadoUsuario)

class Contrasenia(models.Model):
    OIDContrasenia = models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    #contrasenia= HAY Q VER COMO HACER ESTO
    fechaAltaContrasenia=models.DateField()
    fechaBajaContrasenia=models.DateField()

    OIDUsuario=models.ForeignKey(Usuario,db_column="OIDUsuario",related_name="contrasenia")

class EstadoUsuario(models.Model):
    OIDEstadoUsuario = models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    descripcionEstadoUsuario=models.CharField(max_length=100)
    nombreEstadoUsuario=models.CharField(max_length=100)

class HistoricoEstadoUsuario(models.Model):
    OIDHistoricoEstadoUsuario =models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    fechaFinEstadoUsuario=models.DateField()
    fechaInicioEstadoUsuario=models.DateField()

    usuario=models.ForeignKey(Usuario,db_column="OIDUsuario",related_name="historico_estado_usuario")
    estadoUsuario=models.ForeignKey(EstadoUsuario,db_column="OIDEstadoUsuario")

class Sesion(models.Model):
    OIDSesion = models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    fechaYHoraFin=models.DateField()
    fechaYHoraInicio=models.DateField()
    idSesion=models.IntegerField(max_lenght=30)

    usuario=models.ForeignKey(Usuario,db_column="OIDUsuario",related_name="sesion")
    tipoSesion=models.ForeignKey(TipoSesion,db_column="OIDTipoSesion")

class TipoSesion(models.Model):
    OIDTipoSesion = models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    idTipo=models.IntegerField(max_length=2)
    nombre=models.CharField(max_length=15)

class Rol(models.Model):
    OIDRol = models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    nombreRol=models.CharField(max_length=10)
    fechaAltaRol=models.DateField()
    fechaBajaRol=models.DateField()

class UsuarioFinca(models.Model):
    OIDUsuarioFinca=models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    fechaAltaUsuarioFinca=models.DateField()
    fechaBajaUsuarioFinca=models.DateField()

    finca=models.ForeignKey(moduloFinca.Finca,db_column="OIDFinca")
    usuario=models.ForeignKey(Usuario,db_column="OIDUsuario")

class RolUsuarioFinca:
    OIDRolUsuarioFinca=models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    fechaAltaUsuarioFinca=models.DateField()
    fechaBajaUsuarioFinca=models.DateField()

    rol=models.ForeignKey(Rol,db_column="OIDRol")
    usuarioFinca=models.ForeignKey(UsuarioFinca,db_column="OIDUsuarioFinca",related_name="rol_usuario_finca")

class ConjuntoPermisos:
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

    rol_=models.ForeignKey(Rol,db_column="OIDRol",related_name="conjunto_permisos")
