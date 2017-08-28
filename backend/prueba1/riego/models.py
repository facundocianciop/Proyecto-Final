from django.db import models
import uuid
#MODULO FINCA
class ProveedorInformacionClimaticaFinca(models.Model):
    OIDProveedorInformacionClimaticaFinca = models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    fechaAltaProveedorInfoClimaticaFinca=models.DateField()
    fechaBajaProveedorInfoClimaticaFinca=models.DateField()
    frecuencia=models.IntegerField()
    finca=models.ForeignKey("Finca",db_column="OIDFinca",null=True)
class Finca(models.Model):
    OIDFinca=models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    direccionLegal=models.CharField(max_length=50)
    idFinca=models.IntegerField()
    logoFinca=models.ImageField(null=True)
    nombre=models.CharField(max_length=50)
    tamanio=models.FloatField()
    ubicacion=models.CharField(max_length=50)


class EstadoFinca(models.Model):
    OIDFinca = models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    descripcionEstadoFinca=models.CharField(max_length=100)
    nombreEstadoFinca=models.CharField(max_length=15)

class HistoricoEstadoFinca(models.Model):
    OIDHistoricoEstadoFinca = models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    fechaFinEstadoFinca=models.DateField()
    fechaInicioEstadoFinca=models.DateField()

    finca=models.ForeignKey(Finca,db_column="OIDFinca",related_name="historicoEstadoFinca")
    estado_finca=models.ForeignKey(EstadoFinca,db_column="OIDEstadoFinca")


class MecanismoRiegoFinca(models.Model):
    OIDMecanismoRiegoFinca = models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    direccionIP=models.CharField(max_length=20)
    fechaInstalacion=models.DateField()
    idFincaMecanismoRiego=models.IntegerField()

    finca=models.ForeignKey(Finca,db_column="OIDFinca")

class EstadoMecanismoRiegoFinca(models.Model):
    OIDEstadoMecanismoRiegoFinca = models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    nombreEstadoMecanismoRiegoFincaSector=models.CharField(max_length=20)
    descripcionEstadoMecanismoRiegoFincaSector=models.CharField(max_length=100)

class HistoricoMecanismoRiegoFinca(models.Model):
    OIDHistoricoMecanismoRiegoFinca =models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    mecanismo_riego_finca=models.ForeignKey(MecanismoRiegoFinca,db_column="OIDMecanismoRiegoFinca",related_name="historicoMecanismoRiegoFinca")
    estado_mecanismo_riego_finca=models.ForeignKey(EstadoMecanismoRiegoFinca,db_column="OIDEstadoMecanismoRiegoFinca")




    #MODULO SEGURIDAD
class EstadoUsuario(models.Model):
    OIDEstadoUsuario = models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    descripcionEstadoUsuario=models.CharField(max_length=100)
    nombreEstadoUsuario=models.CharField(max_length=100)

class Usuario(models.Model):
    OIDUsuario = models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    usuario=models.CharField(max_length=30)
    nombre=models.CharField(max_length=30)
    apellido=models.CharField(max_length=30)
    cuit=models.CharField(max_length=15)
    dni=models.IntegerField()
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



class HistoricoEstadoUsuario(models.Model):
    OIDHistoricoEstadoUsuario =models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    fechaFinEstadoUsuario=models.DateField()
    fechaInicioEstadoUsuario=models.DateField()

    usuario=models.ForeignKey(Usuario,db_column="OIDUsuario",related_name="historicoEstadoUsuario")
    estadoUsuario=models.ForeignKey(EstadoUsuario,db_column="OIDEstadoUsuario")
class TipoSesion(models.Model):
    OIDTipoSesion = models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    idTipo=models.IntegerField()
    nombre=models.CharField(max_length=15)

class Sesion(models.Model):
    OIDSesion = models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    fechaYHoraFin=models.DateField()
    fechaYHoraInicio=models.DateField()
    idSesion=models.CharField(max_length=30)

    usuario=models.ForeignKey(Usuario,db_column="OIDUsuario",related_name="sesion")
    tipoSesion=models.ForeignKey(TipoSesion,db_column="OIDTipoSesion")



class Rol(models.Model):
    OIDRol = models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    nombreRol=models.CharField(max_length=10)
    fechaAltaRol=models.DateField()
    fechaBajaRol=models.DateField()

class UsuarioFinca(models.Model):
    OIDUsuarioFinca=models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    fechaAltaUsuarioFinca=models.DateField()
    fechaBajaUsuarioFinca=models.DateField()

    finca=models.ForeignKey(Finca,db_column="OIDFinca")
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

    rol_=models.ForeignKey(Rol,db_column="OIDRol",related_name="conjuntoPermisos")

#MODULO CULTIVOS
class TipoCultivo(models.Model):
    OIDTipoCultivo = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    idTipo = models.IntegerField(unique=True)
    nombreTipoCultivo = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=100)
    habilitado = models.BooleanField()
    fechaAltaTipoCultivo = models.DateField()
    fechaBajaTipoCultivo = models.DateField()
class SubtipoCultivo(models.Model):
    OIDSubtipoCultivo = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    idSubtipo = models.IntegerField(unique=True)
    nombreSubtipo = models.CharField(max_length=20)
    habilitado = models.BooleanField()
    descripcion = models.CharField(max_length=100)
    fechaAltaSubtipoCultivo = models.DateField()
    fechaBajaSubtipoCultivo = models.DateField()

    tipo_cultivo = models.ForeignKey(TipoCultivo, db_column="OIDTipoCultivo")





class CaracteristicaSubtipo(models.Model):
    OIDCaracteristicaSubtipo = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    atributo = models.CharField(max_length=20)
    comentario = models.CharField(max_length=100)
    valor = models.CharField(max_length=20)

    subtipo_cultivo = models.ForeignKey(SubtipoCultivo, db_column="OIDSubtipoCultivo",
                                            related_name="caracteristicaSubtipoList")

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
    fechaAltaConfiguracionEventoPersonalizado = models.DateField()
    fechaBajaConfiguracionEventoPersonalizado = models.DateField()
    fechaHoraCreacion = models.DateField()

    usuario_finca = models.ForeignKey(UsuarioFinca, db_column="OIDUsuarioFinca",
                                              related_name="usuarioFinca")
class EventoPersonalizado(models.Model):
    OIDEventoPersonalizado = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nroEvento = models.IntegerField(unique=True)
    fechaHora = models.DateField()

    configuracion_evento_personalizado = models.ForeignKey(ConfiguracionEventoPersonalizado,
                                                                   db_column="OIDConfiguracionEventoPersonalizado")
#MODULO RIEGO
class TipoConfiguracionRiego(models.Model):
    OIDTipoConfiguracionRiego=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    idTipoConfiguracion=models.IntegerField(unique=True)
    nombre=models.CharField(max_length=20,unique=True)
class ConfiguracionRiego(models.Model):
    OIDConfiguracionRiego=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    nombre=models.CharField(max_length=20)
    descripcion=models.CharField(max_length=100)
    duracionMaxima=models.FloatField()
    fechaCreacion=models.DateField()
    fechaFinalizacion=models.DateField()

    tipoConfiguracionRiego=models.ForeignKey(TipoConfiguracionRiego,db_column="OIDTipoConfiguracionRiego")
    mecanismoRiegoFincaSector=models.ForeignKey('MecanismoRiegoFincaSector',db_column="OIDMecanismoRiegoFincaSector",null=True)




class EstadoConfiguracionRiego(models.Model):
    OIDEstadoConfiguracionRiego=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    nombreEstadoConfiguracionRiego=models.CharField(max_length=20,unique=True)
    descripcionEstadoConfiguracionRiego=models.CharField(max_length=100)

class HistoricoEstadoConfiguracionRiego(models.Model):
    OIDHistoricoEstadoConfiguracionRiego=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    fechaFinEstadoConfiguracionRiego=models.DateField()
    fechaInicioEstadoConfiguracionRiego=models.DateField()

    configuracion_riego=models.ForeignKey(ConfiguracionRiego,db_column="OIDConfiguracionRiego",related_name="historicoEstadoConfiguracionRiegoList")
    estado_configuracion_riego=models.ForeignKey(EstadoConfiguracionRiego,db_column="OIDEstadoConfiguracionRiego")

class EstadoEjecucionRiego(models.Model):
    OIDEstadoEjecucionRiego=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    nombreEstadoEjecucionRiego=models.CharField(max_length=20,unique=True)
    descripcionEstadoEjecucionRiego=models.CharField(max_length=100)
class MecanismoRiegoFincaSector(models.Model):
    OIDMecanismoRiegoFincaSector=models.UUIDField( primary_key=True, editable=False)
    caudal=models.FloatField()
    presion=models.FloatField()
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
    mecanismo_riego_finca_sector=models.ForeignKey(MecanismoRiegoFincaSector,db_column="OIDMecanismoRiegoFincaSector",related_name="ejecucionRiegoList")



class CriterioRiego(models.Model):
    OIDCriterioRiego=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    fechaCreacionCriterio=models.DateField()
    # class Meta:
    #     abstract=True
    #ESTO ES LO MAS IMPORTANTE HAY Q VER COMO IMPLEMENTAMOS LOS CRITERIOS INICIALES Y FINALES
    #COMO LAS RELACIONES SE MANEJAN AL REVES LO Q YO HICE FUE Q APUNTARA DOS VECSE A LA CONFIGURACION DE RIEGO
    #Y Q LA OTRA TENGA DOS ATRIBUTOS Q PARA LOS CRITERIOS INICIALES Y PARA LOS FINALES(LOS Q ESTAN EN EL related_name)
    # configuracionRiegoInicial = models.ForeignKey(ConfiguracionRiego, db_column="OIDConfiguracionRiegoInicial",
    #                                               related_name="criterioRiegoInicioList")
    configuracionRiegoInicial = models.OneToOneField(ConfiguracionRiego,on_delete=models.CASCADE,db_column="OIDConfiguracionRiegoInicial",related_name="criterioRiegoInicial",null=True)
    configuracionRiegoFinal = models.ForeignKey(ConfiguracionRiego, db_column="OIDConfiguracionRiegoFinal",
                                                related_name="criterioRiegoFinal",null=True)

class CriterioRiegoPorMedicion(CriterioRiego):
    valor=models.FloatField()
    # class Meta(CriterioRiego.Meta):
    #     db_table="CriterioRiegoPorMedicion"
    # configuracionRiegoInicial=models.ForeignKey(ConfiguracionRiego,db_column="OIDConfiguracionRiegoInicial",related_name="%(class)scriterioRiegoInicioList")
    # configuracionRiegoFinal = models.ForeignKey(ConfiguracionRiego, db_column="OIDConfiguracionRiegoFinal", related_name="%(class)scriterioRiegoFinal")

class CriterioRiegoVolumenAgua(CriterioRiego):
    volumen=models.FloatField()
    # class Meta(CriterioRiego.Meta):
    #     db_table="CriterioRiegoVolumenAgua"
    # configuracionRiegoInicial=models.ForeignKey(ConfiguracionRiego,db_column="OIDConfiguracionRiegoInicial",related_name="%(class)scriterioRiegoInicioList")
    # configuracionRiegoFinal = models.ForeignKey(ConfiguracionRiego, db_column="OIDConfiguracionRiegoFinal", related_name="%(class)scriterioRiegoFinal")

class CriterioRiegoPorHora(CriterioRiego):
    hora=models.DateField()
    numeroDia=models.IntegerField()
    # class Meta(CriterioRiego.Meta):
    #     db_table = "CriterioRiegoPorHora"
    # configuracionRiegoInicial=models.ForeignKey(ConfiguracionRiego,db_column="OIDConfiguracionRiegoInicial",related_name="%(class)scriterioRiegoInicioList")
    # configuracionRiegoFinal = models.ForeignKey(ConfiguracionRiego, db_column="OIDConfiguracionRiegoFinal", related_name="%(class)scriterioRiegoFinal")

#MODULO SECTORES
class Sector(models.Model):
    OIDSector=models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False)
    numeroSector=models.IntegerField()
    nombreSector=models.CharField(max_length=20)
    descripcionSector=models.CharField(max_length=100)
    superficie=models.FloatField()

    def __str__(self):
        return ("Este es el sector %d")%self.numeroSector
class Cultivo(models.Model):
    OIDCultivo = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    descripcion = models.CharField(max_length=100)
    nombre = models.CharField(max_length=20)
    fechaPlantacion = models.DateField()
    fechaEliminacion = models.DateField()
    habilitado = models.BooleanField()

    subtipo_cultivo = models.ForeignKey(SubtipoCultivo, db_column="OIDSubtipoCultivo")
    sector= models.ForeignKey(Sector, db_column="OIDSector")
    def __str__(self):
        return ("Este es el cultivo %s")%self.nombre


class EstadoSector(models.Model):
    OIDEstadoSector=models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False)
    descripcionEstadoSector=models.CharField(max_length=100)
    nombreEstadoSector=models.CharField(max_length=20)

    def __str__(self):
        return ("Este es el estado %s") % self.nombreEstadoSector

class HistoricoEstadoSector(models.Model):
    OIDHistoricoEstadoSector=models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    fechaFinEstadoSector=models.DateField()
    fechaInicioEstadoSector=models.DateField()

    estado_sector=models.ForeignKey(EstadoSector,db_column="OIDEstadoSector")
    sector=models.ForeignKey(Sector,db_column="OIDSector",related_name="historicoEstadoSector")




class EstadoMecanismoRiegoFincaSector(models.Model):
    OIDEstadoMecanismoRiegoFincaSector=models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    descripcionEstadoMecanismoRiegoFincaSector=models.CharField(max_length=100)
    nombreEstadoMecanismoRiegoFincaSector=models.CharField(max_length=20)

class HistoricoMecanismoRiegoFincaSector(models.Model):
    OIDHistoricoMecanismoRiegoFincaSector=models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    fechaFinEstadoMecanismoRiegoFincaSector=models.DateField()
    fechaInicioEstadoMecanismoRiegoFincaSector=models.DateField()

    mecanismo_riego_finca_sector=models.ForeignKey(MecanismoRiegoFincaSector,db_column="OIDMecanismoRiegoFincaSector",related_name="historicoMecanismoRiegoFincaSector")
    estado_mecanismo_riego_finca_sector=models.ForeignKey(EstadoMecanismoRiegoFincaSector,db_column="OIDEstadoMecanismoRiegoFincaSector")


class ComponenteSensor(models.Model):
    OIDComponenteSensor=models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    numeroComponente=models.IntegerField()
    habilitado=models.BooleanField()
    fechaAltaComponenteSensor=models.DateField()
    fechaBajaComponenteSensor=models.DateField()
#MODULO SENSORES
class TipoMedicion(models.Model):
    OIDTipoMedicion=models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    idTipoMedicion=models.IntegerField()
    nombreTipoMedicion=models.CharField(max_length=20)
    unidadMedicion = models.CharField(max_length=20)
    habilitado=models.BooleanField()
    fechaAltaTipoMedicion=models.DateField()
    fechaBajaTipoMedicion=models.DateField()
class Sensor(models.Model):
    OIDSensor=models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    idSensor=models.IntegerField()
    fechaAltaSensor=models.DateField()
    fechaBajaSensor=models.DateField()
    habilitado=models.BooleanField()
    modelo=models.CharField(max_length=20)

    componente_sensor=models.ForeignKey(ComponenteSensor,db_column="OIDComponenteSensor",related_name="sensor")
    sensorTipoInterna=models.ForeignKey('riego.TipoMedicion',db_column="OIDTipoMedicion")
    finca=models.ForeignKey(Finca,db_column="OIDFinca")





class ComponenteSensorSector(models.Model):
    OIDComponenteSensorSector=models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    idComponenteSensores=models.IntegerField()

    componente_sensor=models.ForeignKey(Sector,db_column="OIDSector")
class HistoricoComponenteSensorSector(models.Model):
    OIDHistoricoComponenteSensorSector=models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    fechaAltaComponenteSensorSector=models.DateField()
    fechaBajaComponenteSensorSecto=models.DateField()
    componenteSensorSector=models.ForeignKey(ComponenteSensorSector,db_column="OIDComponenteSensorSector",related_name="historicoComponenteSensorSector")

class EstadoComponenteSensorSector(models.Model):
    models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombreEstadoSensorSector=models.CharField(max_length=20)
    descripcionEstadoSensorSector=models.CharField(max_length=100)



class MedicionCabecera(models.Model):
    OIDMedicionCabecera=models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    fechaYHora=models.DateField()
    nroMedicion=models.IntegerField()

class MedicionDetalle(models.Model):
    OIDMedicionDetalle=models.UUIDField( primary_key=True,default=uuid.uuid4, editable=False)
    nroRenglon=models.IntegerField()
    valor=models.FloatField()
    medicionCabecera=models.ForeignKey(MedicionCabecera,db_column="OIDMedicionCabecera",related_name="medicionDetalle")

#MODULO INFORMACION EXTERNA
class MetodoProveedorInformacionClimatica(models.Model):
    OIDMetodoProveedorInformacionClimatica=models.UUIDField(default=uuid.uuid4,primary_key=True)
    nombreMetodo=models.CharField(max_length=40)
    tipoMetodo=models.CharField(max_length=10,unique=True)
    proveedor_informacion_climatica=models.ForeignKey('ProveedorInformacionClimatica',db_column="OIDProveedorInformacionClimatica",related_name="metodoProveedorInformacionClimaticaList")

class TipoMedicionClimatica(models.Model):
    OIDTipoMedicionClimatica=models.UUIDField(default=uuid.uuid4,primary_key=True)
    idTipoMedicionClimatica=models.IntegerField(unique=True)
    nombreTipoMedicionClimatica=models.IntegerField(unique=True)
    tipoDato=models.CharField(max_length=10)
    fechaAltaTipoMedicionClimatica=models.DateField()
    fechaBajaTipoMedicionClimatica=models.DateField()
    habilitada=models.BooleanField()

    metodo_proveedor_informacion_climatica=models.ForeignKey(MetodoProveedorInformacionClimatica,db_column="OIDMetodoProveedorInformacionClimatica",related_name="tipoMedicionClimatica")


class ProveedorInformacionClimatica(models.Model):
    OIDProveedorInformacionClimatica=models.UUIDField(default=uuid.uuid4,primary_key=True)
    nombreProveedor=models.CharField(max_length=20,unique=True)
    habilitado=models.BooleanField()
    urlAPI=models.CharField(max_length=100)
    frecuenciaMaxPosible=models.IntegerField()
    fechaAltaProveedorInfoClimatica=models.DateField()
    fechaBajaProveedorInfoClimatica=models.DateField()

    tipo_medicion_climatica=models.ManyToManyField(TipoMedicionClimatica)


class MedicionEstadoExterno(MedicionEvento):
    #HERENCIA
    tipo_medicion_climatica=models.ForeignKey(TipoMedicionClimatica,db_column="OIDTipoMedicionClimatica")
    # class Meta(MedicionEvento.Meta):
    #     db_table = "MedicionEstadoExterno"



class Parametro(models.Model):
    OIDParametro=models.UUIDField(default=uuid.uuid4,primary_key=True)
    nombre=models.CharField(max_length=20)
    tipo=models.CharField(max_length=20)
    descripcion=models.CharField(max_length=100)

    metodo_proveedor_informacion_climatica=models.ForeignKey(MetodoProveedorInformacionClimatica,db_column="OIDMetodoProveedorInformacionClimatica",related_name="parametro_list")

class MedicionInformacionClimaticaCabecera(models.Model):
    OIDMedicionInformacionClimaticaCabecera=models.UUIDField(default=uuid.uuid4,primary_key=True)
    nroMedicion=models.IntegerField(unique=True)
    fechaHora=models.DateField()

    proveedor_informacion_climatica_externa=models.ForeignKey(ProveedorInformacionClimaticaFinca,db_column="OIDProveedorInformacionClimaticaFinca",related_name="medicionInformacionClimaticaCabeceraList")

class MedicionInformacionClimaticaDetalle(models.Model):
    OIDMedicionInformacionClimaticaDetalle=models.UUIDField(default=uuid.uuid4,primary_key=True)
    nroRenglon=models.IntegerField()
    valor=models.FloatField()

    medicion_informacion_climatica_cabecera=models.ForeignKey(MedicionInformacionClimaticaCabecera,db_column="OIDMedicionInformacionClimaticaCabecera",related_name="medicionInformacionClimaticaDetalle")
    tipo_medicion_climatica=models.ForeignKey(TipoMedicionClimatica,db_column="OIDTipoMedicionClimatica")