# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import *

admin.site.register(DatosUsuario)
admin.site.register(Finca)
admin.site.register(TipoCultivo)
admin.site.register(SubtipoCultivo)
admin.site.register(TipoMecanismoRiego)
admin.site.register(TipoMedicion)
admin.site.register(ProveedorInformacionClimatica)
admin.site.register(TipoMedicionClimatica)
admin.site.register(Rol)


#ABM de Estados: no estan como CU. Decidir si dejarlos. Los estados deberian ser fijos
admin.site.register(EstadoUsuario)
admin.site.register(EstadoFinca)
admin.site.register(EstadoMecanismoRiegoFinca)
admin.site.register(EstadoSector)
admin.site.register(EstadoMecanismoRiegoFincaSector)
admin.site.register(EstadoConfiguracionRiego)
admin.site.register(EstadoEjecucionRiego)
admin.site.register(EstadoComponenteSensorSector)