# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0009_auto_20150706_0952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='keywords',
            field=models.CharField(max_length=2000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='publisher',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='url',
            field=models.CharField(max_length=500, null=True, verbose_name=b'URL', blank=True),
        ),
    ]
