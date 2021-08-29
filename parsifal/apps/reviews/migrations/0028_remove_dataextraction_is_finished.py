# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0027_dataextraction_is_finished'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataextraction',
            name='is_finished',
        ),
    ]
