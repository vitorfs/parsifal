# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0028_remove_dataextraction_is_finished'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='finished_data_extraction',
            field=models.BooleanField(default=False),
        ),
    ]
