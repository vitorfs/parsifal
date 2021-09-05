# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0016_auto_20150710_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='last_update',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
