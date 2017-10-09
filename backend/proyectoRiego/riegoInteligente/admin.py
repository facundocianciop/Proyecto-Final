# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import *


class FincaAdmin(admin.ModelAdmin):
    list_display = ('fincas_pendientes',)
    def fincas_pendientes(self):
        return '<a href="%s">%s</a>' %('http://127.0.0.1:8000/riegoInteligente/aprobarFinca/',
                                       'Fincas en estado Pendiente')
    fincas_pendientes.allow_tags = True


admin.site.register(DatosUsuario)
admin.site.register(SesionUsuario)
admin.site.register(TipoSesion)
admin.site.register(Finca)
admin.site.register(TipoCultivo)
admin.site.register(SubtipoCultivo)
admin.site.register(TipoMecanismoRiego)
admin.site.register(TipoMedicion)
admin.site.register(ProveedorInformacionClimatica)
admin.site.register(TipoMedicionClimatica)
admin.site.register(TipoConfiguracionRiego)
admin.site.register(Rol)
admin.site.register(ConjuntoPermisos)


# ABM de Estados: no estan como CU. Decidir si dejarlos. Los estados deberian ser fijos
admin.site.register(EstadoUsuario)
admin.site.register(EstadoFinca)
admin.site.register(HistoricoEstadoFinca)
admin.site.register(EstadoMecanismoRiegoFinca)
admin.site.register(EstadoSector)
admin.site.register(EstadoMecanismoRiegoFincaSector)
admin.site.register(EstadoConfiguracionRiego)
admin.site.register(EstadoEjecucionRiego)
admin.site.register(EstadoComponenteSensorSector)
