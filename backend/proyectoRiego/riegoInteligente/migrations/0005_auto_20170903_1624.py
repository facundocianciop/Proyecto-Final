# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-03 19:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('riegoInteligente', '0004_auto_20170903_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicoestadousuario',
            name='usuario',
            field=models.ForeignKey(db_column=b'OIDUsuario', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='historicoEstadoUsuarioList', to='riegoInteligente.Usuario'),
        ),
    ]
