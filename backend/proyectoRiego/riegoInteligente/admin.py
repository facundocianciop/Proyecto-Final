# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import *


admin.site.register(DatosUsuario)
admin.site.register(SesionUsuario)
admin.site.register(Finca)
admin.site.register(Rol)
admin.site.register(ConjuntoPermisos)
admin.site.register(ProveedorInformacionClimatica)

admin.site.register(ConfiguracionEventoPersonalizado)
admin.site.register(MedicionEstadoExterno)
admin.site.register(MedicionFuenteInterna)

admin.site.register(TipoSesion)
admin.site.register(TipoCultivo)
admin.site.register(SubtipoCultivo)
admin.site.register(TipoMecanismoRiego)
admin.site.register(TipoMedicion)
admin.site.register(TipoMedicionClimatica)
admin.site.register(TipoConfiguracionRiego)

# Historicos
admin.site.register(HistoricoEstadoUsuario)
admin.site.register(HistoricoEstadoFinca)
admin.site.register(HistoricoMecanismoRiegoFinca)
admin.site.register(HistoricoEstadoSector)
admin.site.register(HistoricoMecanismoRiegoFincaSector)
admin.site.register(HistoricoEstadoComponenteSensor)
admin.site.register(HistoricoEstadoConfiguracionRiego)
admin.site.register(HistoricoEstadoComponenteSensorSector)


# ABM de Estados: no estan como CU. Decidir si dejarlos. Los estados deberian ser fijos
admin.site.register(EstadoUsuario)
admin.site.register(EstadoFinca)
admin.site.register(EstadoMecanismoRiegoFinca)
admin.site.register(EstadoSector)
admin.site.register(EstadoMecanismoRiegoFincaSector)
admin.site.register(EstadoConfiguracionRiego)
admin.site.register(EstadoEjecucionRiego)
admin.site.register(EstadoComponenteSensor)
admin.site.register(EstadoComponenteSensorSector)
