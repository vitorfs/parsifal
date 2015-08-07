# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20150611_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='description',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
    ]
