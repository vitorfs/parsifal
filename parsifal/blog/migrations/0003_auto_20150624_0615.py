# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20150623_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='summary',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='entry',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='entry',
            name='last_update',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 24, 6, 15, 21, 297726, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
