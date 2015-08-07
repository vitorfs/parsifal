# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0017_auto_20150710_1636'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='data_extraction_strategy',
        ),
        migrations.RemoveField(
            model_name='review',
            name='quality_assessment_strategy',
        ),
        migrations.RemoveField(
            model_name='review',
            name='study_selection_strategy',
        ),
    ]
