# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-24 15:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('riegoInteligente', '0014_auto_20170923_1948'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sensor',
            name='finca',
        ),
        migrations.AlterField(
            model_name='mecanismoriegofincasector',
            name='OIDMecanismoRiegoFincaSector',
            field=models.UUIDField(default=uuid.UUID('c2f2ec47-0025-4af9-ad5b-b07b59d9f125'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='componente_sensor',
            field=models.ForeignKey(db_column=b'OIDComponenteSensor', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sensor', to='riegoInteligente.ComponenteSensor'),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='idSensor',
            field=models.IntegerField(default=1, unique=True),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='sensorTipoInterna',
            field=models.ForeignKey(db_column=b'OIDTipoMedicion', null=True, on_delete=django.db.models.deletion.CASCADE, to='riegoInteligente.TipoMedicion'),
        ),
    ]
