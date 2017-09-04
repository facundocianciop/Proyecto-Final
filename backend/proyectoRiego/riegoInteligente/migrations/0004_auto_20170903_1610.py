# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-03 19:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('riegoInteligente', '0003_auto_20170903_1545'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='OIDEstadoUsuario',
        ),
        migrations.AlterField(
            model_name='historicoestadousuario',
            name='usuario',
            field=models.ForeignKey(db_column=b'OIDUsuario', on_delete=django.db.models.deletion.CASCADE, related_name='historicoEstadoUsuarioList', to='riegoInteligente.Usuario'),
        ),
    ]
