# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-10 16:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('riegoInteligente', '0025_auto_20170909_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rol',
            name='nombreRol',
            field=models.CharField(max_length=30),
        ),
    ]