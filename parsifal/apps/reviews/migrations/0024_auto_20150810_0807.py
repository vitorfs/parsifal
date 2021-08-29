# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0023_auto_20150806_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='research_questions', to='reviews.Review'),
        ),
    ]
