# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-29 02:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('userinfo_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.UserInfo')),
            ],
            bases=('app.userinfo',),
        ),
        migrations.RenameField(
            model_name='productos',
            old_name='imgReferencia',
            new_name='img_referencia',
        ),
        migrations.RenameField(
            model_name='vendedor',
            old_name='archivoFotoPerfil',
            new_name='archivo_foto_perfil',
        ),
        migrations.RenameField(
            model_name='vendedor',
            old_name='nombreFotoPerfil',
            new_name='nombre_visible',
        ),
        migrations.RemoveField(
            model_name='vendedor',
            name='user',
        ),
        migrations.AddField(
            model_name='vendedor',
            name='efectivo',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='vendedor',
            name='tarj_cred',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='vendedor',
            name='tarj_deb',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='vendedor',
            name='tarj_junaeb',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='vendedor',
            name='userinfo_ptr',
            field=models.OneToOneField(auto_created=True, default=None, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.UserInfo'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vendedorambulante',
            name='check_in',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='favoritos',
            name='alumno',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.Alumno'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='tipo',
            field=models.CharField(max_length=10),
        ),
    ]
