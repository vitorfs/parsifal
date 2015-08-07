# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0021_auto_20150722_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyword',
            name='related_to',
            field=models.CharField(blank=True, max_length=1, choices=[('P', 'Population'), ('I', 'Intervention'), ('C', 'Comparison'), ('O', 'Outcome')]),
        ),
    ]
