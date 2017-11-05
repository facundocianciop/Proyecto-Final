# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib.admin import AdminSite

from models import *
from riegoInteligente.views import views_administrador


class SmartFarmingAdminSite(AdminSite):
    site_header = 'Smart Farming'
    site_title = 'Administracion Smart Farming'

    def get_urls(self):
        urls = super(SmartFarmingAdminSite, self).get_urls()
        my_urls = [
            url(r'^riegoInteligente/fincasPorAprobar/', self.admin_view(views_administrador.fincas_por_aprobar),
                name='fincasPorAprobar'),
            url(r'^riegoInteligente/aprobarFinca/(?P<idFinca>[0-9]+)/$', self.admin_view(views_administrador.aprobar_finca),
                name='aprobarFinca'),
            url(r'^riegoInteligente/noAprobarFinca/(?P<idFinca>[0-9]+)/$', self.admin_view(views_administrador.no_aprobar_finca),
                name='noAprobarFinca'),
        ]
        return my_urls + urls


admin_site = SmartFarmingAdminSite(name='admin')


admin_site.register(User)

admin_site.register(DatosUsuario)
admin_site.register(SesionUsuario)
admin_site.register(Finca)
admin_site.register(Rol)
admin_site.register(ConjuntoPermisos)
admin_site.register(ProveedorInformacionClimatica)

admin_site.register(ConfiguracionEventoPersonalizado)
admin_site.register(MedicionEstadoExterno)
admin_site.register(MedicionFuenteInterna)

admin_site.register(TipoSesion)
admin_site.register(TipoCultivo)
admin_site.register(SubtipoCultivo)
admin_site.register(TipoMecanismoRiego)
admin_site.register(TipoMedicion)
admin_site.register(TipoMedicionClimatica)
admin_site.register(TipoConfiguracionRiego)

# Historicos
admin_site.register(HistoricoEstadoUsuario)
admin_site.register(HistoricoEstadoFinca)
admin_site.register(HistoricoMecanismoRiegoFinca)
admin_site.register(HistoricoEstadoSector)
admin_site.register(HistoricoMecanismoRiegoFincaSector)
admin_site.register(HistoricoEstadoComponenteSensor)
admin_site.register(HistoricoEstadoConfiguracionRiego)
admin_site.register(HistoricoEstadoComponenteSensorSector)


# ABM de Estados: no estan como CU. Decidir si dejarlos. Los estados deberian ser fijos
admin_site.register(EstadoUsuario)
admin_site.register(EstadoFinca)
admin_site.register(EstadoMecanismoRiegoFinca)
admin_site.register(EstadoSector)
admin_site.register(EstadoMecanismoRiegoFincaSector)
admin_site.register(EstadoConfiguracionRiego)
admin_site.register(EstadoEjecucionRiego)
admin_site.register(EstadoComponenteSensor)
admin_site.register(EstadoComponenteSensorSector)
