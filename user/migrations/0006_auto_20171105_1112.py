# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-05 11:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20171105_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documents',
            name='author',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='documents',
            name='publisher',
            field=models.CharField(default='', max_length=300),
        ),
    ]
