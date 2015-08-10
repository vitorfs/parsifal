# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0023_auto_20150806_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='review',
            field=models.ForeignKey(related_name='research_questions', to='reviews.Review'),
        ),
    ]
