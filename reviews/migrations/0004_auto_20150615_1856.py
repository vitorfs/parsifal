# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20150612_1222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='description',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together=set([]),
        ),
    ]
