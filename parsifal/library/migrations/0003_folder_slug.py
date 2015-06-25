# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_auto_20150625_2141'),
    ]

    operations = [
        migrations.AddField(
            model_name='folder',
            name='slug',
            field=models.SlugField(default=1),
            preserve_default=False,
        ),
    ]
