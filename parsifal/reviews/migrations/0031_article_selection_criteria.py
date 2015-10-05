# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0030_auto_20150909_1749'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='selection_criteria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='reviews.SelectionCriteria', null=True),
        ),
    ]
