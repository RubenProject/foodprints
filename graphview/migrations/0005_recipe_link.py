# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-21 02:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graphview', '0004_auto_20161205_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='link',
            field=models.CharField(default=b'empty', max_length=500),
        ),
    ]
