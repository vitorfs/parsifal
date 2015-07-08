# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0012_auto_20150708_1234'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dataextractionfield',
            options={'ordering': ('order',), 'verbose_name': 'Data Extraction Field', 'verbose_name_plural': 'Data Extraction Fields'},
        ),
        migrations.AlterModelOptions(
            name='qualityquestion',
            options={'ordering': ('order',), 'verbose_name': 'Quality Assessment Question', 'verbose_name_plural': 'Quality Assessment Questions'},
        ),
        migrations.AddField(
            model_name='dataextractionfield',
            name='order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='qualityquestion',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]
