# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class RiegointeligenteConfig(AppConfig):
    name = 'riegoInteligente'

    def ready(self):
        from riegoInteligente.views.supportClases.procesosBackground.procesos_background import *
        comprobar_incio_riego_criterio_hora()