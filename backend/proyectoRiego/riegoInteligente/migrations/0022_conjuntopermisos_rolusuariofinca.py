# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-07 17:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('riegoInteligente', '0021_tipomecanismoriego'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConjuntoPermisos',
            fields=[
                ('OIDConjuntoPermisos', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('puedeAsignarComponenteSensor', models.BooleanField()),
                ('puedeAsignarCultivo', models.BooleanField()),
                ('puedeAsignarMecRiegoAFinca', models.BooleanField()),
                ('puedeAsignarMecRiegoASector', models.BooleanField()),
                ('puedeConfigurarObtencionInfoExterna', models.BooleanField()),
                ('puedeCrearComponenteSensor', models.BooleanField()),
                ('puedeCrearConfiguracionRiego', models.BooleanField()),
                ('puedeCrearSector', models.BooleanField()),
                ('puedeGenerarInformeCruzadoRiegoMedicion', models.BooleanField()),
                ('puedeGenerarInformeEstadoActualSectores', models.BooleanField()),
                ('puedeGenerarInformeEstadoHistoricoSectoresFinca', models.BooleanField()),
                ('puedeGenerarInformeEventoPersonalizado', models.BooleanField()),
                ('puedeGenerarInformeHeladasHistorico', models.BooleanField()),
                ('puedeGenerarInformeRiegoEnEjecucion', models.BooleanField()),
                ('puedeGenerarInformeRiegoPorSectoresHistorico', models.BooleanField()),
                ('puedeGestionarComponenteSensor', models.BooleanField()),
                ('puedeGestionarCultivoSector', models.BooleanField()),
                ('puedeGestionarEventoPersonalizado', models.BooleanField()),
                ('puedeGestionarFinca', models.BooleanField()),
                ('puedeGestionarSector', models.BooleanField()),
                ('puedeGestionarSensores', models.BooleanField()),
                ('puedeGestionarUsuariosFinca', models.BooleanField()),
                ('puedeIniciarODetenerRiegoManualmente', models.BooleanField()),
                ('puedeModificarConfiguracionRiego', models.BooleanField()),
                ('rol', models.ForeignKey(db_column=b'OIDRol', on_delete=django.db.models.deletion.CASCADE, related_name='conjuntoPermisos', to='riegoInteligente.Rol')),
            ],
        ),
        migrations.CreateModel(
            name='RolUsuarioFinca',
            fields=[
                ('OIDRolUsuarioFinca', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('fechaAltaUsuarioFinca', models.DateField()),
                ('fechaBajaUsuarioFinca', models.DateField(null=True)),
                ('rol', models.ForeignKey(db_column=b'OIDRol', on_delete=django.db.models.deletion.CASCADE, to='riegoInteligente.Rol')),
                ('usuarioFinca', models.ForeignKey(db_column=b'OIDUsuarioFinca', on_delete=django.db.models.deletion.CASCADE, related_name='rolUsuarioFincaList', to='riegoInteligente.UsuarioFinca')),
            ],
        ),
    ]