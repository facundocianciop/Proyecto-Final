# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-21 20:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('riegoInteligente', '0002_auto_20171020_0036'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='conjuntopermisos',
            options={'verbose_name_plural': 'Conjuntos de permisos'},
        ),
        migrations.AlterModelOptions(
            name='datosusuario',
            options={'verbose_name_plural': 'Datos de usuarios'},
        ),
        migrations.AlterModelOptions(
            name='estadocomponentesensor',
            options={'verbose_name_plural': '_Estados componente sensor'},
        ),
        migrations.AlterModelOptions(
            name='estadocomponentesensorsector',
            options={'verbose_name_plural': '_Estados componente sensor sector'},
        ),
        migrations.AlterModelOptions(
            name='estadoconfiguracionriego',
            options={'verbose_name_plural': '_Estados configuracion riego'},
        ),
        migrations.AlterModelOptions(
            name='estadoejecucionriego',
            options={'verbose_name_plural': '_Estados ejecucion riego'},
        ),
        migrations.AlterModelOptions(
            name='estadofinca',
            options={'verbose_name_plural': '_Estados finca'},
        ),
        migrations.AlterModelOptions(
            name='estadomecanismoriegofinca',
            options={'verbose_name_plural': '_Estados mecanismo riego finca'},
        ),
        migrations.AlterModelOptions(
            name='estadomecanismoriegofincasector',
            options={'verbose_name_plural': '_Estados mecanismo riego finca sector'},
        ),
        migrations.AlterModelOptions(
            name='estadosector',
            options={'verbose_name_plural': '_Estados sector'},
        ),
        migrations.AlterModelOptions(
            name='estadousuario',
            options={'verbose_name_plural': '_Estados usuario'},
        ),
        migrations.AlterModelOptions(
            name='historicoestadocomponentesensor',
            options={'verbose_name_plural': 'Historicos estado componentes sensor'},
        ),
        migrations.AlterModelOptions(
            name='historicoestadocomponentesensorsector',
            options={'verbose_name_plural': 'Historicos estado componentes sensor sector'},
        ),
        migrations.AlterModelOptions(
            name='historicoestadoconfiguracionriego',
            options={'verbose_name_plural': 'Historicos estado configuraciones riego'},
        ),
        migrations.AlterModelOptions(
            name='historicoestadofinca',
            options={'verbose_name_plural': 'Historicos estado fincas'},
        ),
        migrations.AlterModelOptions(
            name='historicoestadosector',
            options={'verbose_name_plural': 'Historicos estado sectores'},
        ),
        migrations.AlterModelOptions(
            name='historicoestadousuario',
            options={'verbose_name_plural': 'Historicos estado usuarios'},
        ),
        migrations.AlterModelOptions(
            name='historicomecanismoriegofinca',
            options={'verbose_name_plural': 'Historicos mecanismos riego finca'},
        ),
        migrations.AlterModelOptions(
            name='historicomecanismoriegofincasector',
            options={'verbose_name_plural': 'Historicos mecanismos riego finca sector'},
        ),
        migrations.AlterModelOptions(
            name='proveedorinformacionclimatica',
            options={'verbose_name_plural': '_Proveedores informacion climatica'},
        ),
        migrations.AlterModelOptions(
            name='rol',
            options={'verbose_name_plural': 'Roles'},
        ),
        migrations.AlterModelOptions(
            name='sesionusuario',
            options={'verbose_name_plural': 'Sesiones usuarios'},
        ),
        migrations.AlterModelOptions(
            name='subtipocultivo',
            options={'verbose_name_plural': 'Subtipos de cultivo'},
        ),
        migrations.AlterModelOptions(
            name='tipoconfiguracionriego',
            options={'verbose_name_plural': '_Tipos de configuracion de riego'},
        ),
        migrations.AlterModelOptions(
            name='tipocultivo',
            options={'verbose_name_plural': 'Tipos de cultivo'},
        ),
        migrations.AlterModelOptions(
            name='tipomecanismoriego',
            options={'verbose_name_plural': 'Tipos de mecanismos de riego'},
        ),
        migrations.AlterModelOptions(
            name='tipomedicion',
            options={'verbose_name_plural': 'Tipos de mediciones'},
        ),
        migrations.AlterModelOptions(
            name='tipomedicionclimatica',
            options={'verbose_name_plural': 'Tipos de mediciones climaticas'},
        ),
        migrations.AlterModelOptions(
            name='tiposesion',
            options={'verbose_name_plural': '_Tipos de sesion'},
        ),
        migrations.AlterField(
            model_name='configuracioneventopersonalizado',
            name='sectorList',
            field=models.ManyToManyField(to='riegoInteligente.Sector'),
        ),
        migrations.AlterField(
            model_name='usuariofinca',
            name='configuracionEventoPersonalizadoList',
            field=models.ManyToManyField(to='riegoInteligente.ConfiguracionEventoPersonalizado'),
        ),
    ]
