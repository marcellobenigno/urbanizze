# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-02-27 23:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0010_delete_zonacreator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='terreno',
            name='number_pav',
            field=models.PositiveIntegerField(verbose_name='número de pavimentações'),
        ),
    ]