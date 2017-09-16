# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-13 02:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('riegoInteligente', '0030_sesioncustom_tiposesion'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatosUsuario',
            fields=[
                ('OIDDatosUsuario', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('cuit', models.CharField(max_length=15, null=True)),
                ('dni', models.IntegerField(null=True)),
                ('domicilio', models.CharField(max_length=50, null=True)),
                ('fechaNacimiento', models.DateTimeField(null=True)),
                ('imagenUsuario', models.ImageField(null=True, upload_to=b'')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='contrasenia',
            name='OIDUsuario',
        ),
        migrations.RemoveField(
            model_name='sesion',
            name='tipoSesion',
        ),
        migrations.RemoveField(
            model_name='sesion',
            name='usuario',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='user',
        ),
        migrations.AddField(
            model_name='sesioncustom',
            name='fechaYHoraInicio',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='sesioncustom',
            name='horaUltimoAcceso',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='historicoestadousuario',
            name='usuario',
            field=models.ForeignKey(db_column=b'OIDUsuario', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='historicoEstadoUsuarioList', to='riegoInteligente.DatosUsuario'),
        ),
        migrations.AlterField(
            model_name='usuariofinca',
            name='usuario',
            field=models.ForeignKey(db_column=b'OIDUsuario', on_delete=django.db.models.deletion.CASCADE, related_name='usuarioFincaList', to='riegoInteligente.DatosUsuario'),
        ),
        migrations.DeleteModel(
            name='Contrasenia',
        ),
        migrations.DeleteModel(
            name='Sesion',
        ),
        migrations.DeleteModel(
            name='Usuario',
        ),
    ]
