# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0014_auto_20150710_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='study',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.Source', null=True),
        ),
        migrations.AlterField(
            model_name='study',
            name='study_selection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='studies', to='reviews.StudySelection'),
        ),
    ]
