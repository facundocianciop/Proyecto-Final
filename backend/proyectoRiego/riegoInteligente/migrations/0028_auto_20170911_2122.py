# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-12 00:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('riegoInteligente', '0027_auto_20170910_1444'),
    ]

    operations = [
        migrations.RenameField(
            model_name='estadomecanismoriegofinca',
            old_name='descripcionEstadoMecanismoRiegoFincaSector',
            new_name='descripcionEstadoMecanismoRiegoFinca',
        ),
        migrations.RenameField(
            model_name='estadomecanismoriegofinca',
            old_name='nombreEstadoMecanismoRiegoFincaSector',
            new_name='nombreEstadoMecanismoRiegoFinca',
        ),
        migrations.AddField(
            model_name='historicomecanismoriegofinca',
            name='fechaFinEstadoMecanismoRiegoFinca',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='historicomecanismoriegofinca',
            name='fechaInicioEstadoMecanismoRiegoFinca',
            field=models.DateTimeField(null=True),
        ),
    ]
