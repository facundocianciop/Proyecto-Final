# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-12 04:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('riegoInteligente', '0029_sesioncustom'),
    ]

    operations = [
        migrations.AddField(
            model_name='sesioncustom',
            name='tipoSesion',
            field=models.ForeignKey(db_column=b'OIDTipoSesion', null=True, on_delete=django.db.models.deletion.CASCADE, to='riegoInteligente.TipoSesion'),
        ),
    ]
