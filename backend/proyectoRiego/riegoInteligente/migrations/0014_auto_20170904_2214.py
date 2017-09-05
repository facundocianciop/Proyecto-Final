# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-05 01:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('riegoInteligente', '0013_proveedorinformacionclimaticafinca_proveedorinformacionclimatica'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicoestadofinca',
            name='finca',
            field=models.ForeignKey(db_column=b'OIDFinca', on_delete=django.db.models.deletion.CASCADE, related_name='historicoEstadoFincaList', to='riegoInteligente.Finca'),
        ),
    ]
