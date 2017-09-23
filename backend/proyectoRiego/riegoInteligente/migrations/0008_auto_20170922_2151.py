# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-23 00:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('riegoInteligente', '0007_auto_20170922_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mecanismoriegofincasector',
            name='OIDMecanismoRiegoFincaSector',
            field=models.UUIDField(default=uuid.UUID('6df3ce7f-f435-408c-aa2f-028ece5c04bf'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='mecanismoriegofincasector',
            name='sector',
            field=models.ForeignKey(db_column=b'OIDSector', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mecanismoRiegoFincaSector', to='riegoInteligente.Sector'),
        ),
    ]
