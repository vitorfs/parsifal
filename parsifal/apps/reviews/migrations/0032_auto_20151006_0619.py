# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0031_article_selection_criteria'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customarticlestatus',
            name='review',
        ),
        migrations.DeleteModel(
            name='CustomArticleStatus',
        ),
    ]
