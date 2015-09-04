# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0026_auto_20150812_0748'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataextraction',
            name='is_finished',
            field=models.BooleanField(default=False),
        ),
    ]
