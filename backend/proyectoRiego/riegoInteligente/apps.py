# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class RiegointeligenteConfig(AppConfig):
    name = 'riegoInteligente'

    def ready(self):
        from riegoInteligente.views.supportClases.procesos_background import obtener_mediciones_climaticas

        obtener_mediciones_climaticas()
