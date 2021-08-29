# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0029_article_finished_data_extraction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataextraction',
            name='value',
            field=models.TextField(null=True, blank=True),
        ),
    ]
