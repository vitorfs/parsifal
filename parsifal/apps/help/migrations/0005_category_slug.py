# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('help', '0004_auto_20150624_0637'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=255, null=True),
        ),
    ]
