# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-07 04:22
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('riegoInteligente', '0020_auto_20170905_1736'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoMecanismoRiego',
            fields=[
                ('OIDTipoMecanismoRiego', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
        ),
    ]
