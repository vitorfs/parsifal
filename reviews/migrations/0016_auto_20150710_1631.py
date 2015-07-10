# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0015_auto_20150710_1504'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articlefile',
            name='article',
        ),
        migrations.RemoveField(
            model_name='articlefile',
            name='review',
        ),
        migrations.RemoveField(
            model_name='articlefile',
            name='user',
        ),
        migrations.DeleteModel(
            name='ArticleFile',
        ),
    ]
