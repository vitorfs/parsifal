# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20150615_1856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='description',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together=set([('name', 'author')]),
        ),
    ]
