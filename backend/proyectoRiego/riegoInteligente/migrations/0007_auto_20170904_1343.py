# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-04 16:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('riegoInteligente', '0006_auto_20170903_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sesion',
            name='fechaYHoraFin',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='sesion',
            name='idSesion',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='sesion',
            name='usuario',
            field=models.ForeignKey(db_column=b'OIDUsuario', on_delete=django.db.models.deletion.CASCADE, related_name='sesionList', to='riegoInteligente.Usuario'),
        ),
    ]