# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-13 02:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('riegoInteligente', '0031_auto_20170912_2348'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SesionCustom',
            new_name='Sesion',
        ),
    ]
