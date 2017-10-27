# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-27 20:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('riegoInteligente', '0004_auto_20171022_1158'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tipomedicion',
            options={'verbose_name_plural': '_Tipos de mediciones'},
        ),
        migrations.AlterModelOptions(
            name='tipomedicionclimatica',
            options={'verbose_name_plural': '_Tipos de mediciones climaticas'},
        ),
        migrations.AddField(
            model_name='criterioriegopormedicion',
            name='operador',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='proveedorinformacionclimatica',
            name='apiKey',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='criterioriegopormedicion',
            name='valor',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='medicioninformacionclimaticacabecera',
            name='nroMedicion',
            field=models.IntegerField(default=1, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='proveedorinformacionclimatica',
            name='urlAPI',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
