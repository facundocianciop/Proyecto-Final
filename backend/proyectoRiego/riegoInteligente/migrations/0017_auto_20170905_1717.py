# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-05 20:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('riegoInteligente', '0016_auto_20170905_1707'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicoestadofinca',
            old_name='estado_finca',
            new_name='estadoFinca',
        ),
    ]