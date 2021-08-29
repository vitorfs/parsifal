# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0033_auto_20151117_0752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchsession',
            name='search_string',
            field=models.TextField(max_length=10000),
        ),
    ]
