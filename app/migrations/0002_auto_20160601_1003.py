# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-01 13:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foto', models.CharField(blank=True, max_length=300, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('classe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Classe')),
                ('pessoa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Pessoa')),
            ],
        ),
        migrations.AddField(
            model_name='aluno',
            name='foto',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
