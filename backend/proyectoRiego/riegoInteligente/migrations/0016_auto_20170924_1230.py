# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-24 15:30
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('riegoInteligente', '0015_auto_20170924_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mecanismoriegofincasector',
            name='OIDMecanismoRiegoFincaSector',
            field=models.UUIDField(default=uuid.UUID('51849154-0faa-4813-b888-9334d124d791'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='tipomedicion',
            name='idTipoMedicion',
            field=models.IntegerField(default=1, unique=True),
        ),
    ]