# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-26 22:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0007_codurbanismo'),
    ]

    operations = [
        migrations.AddField(
            model_name='zona',
            name='extenso',
            field=models.CharField(default='Zona Residencial 1', max_length=100),
            preserve_default=False,
        ),
    ]