# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0018_auto_20150710_1649'),
    ]

    operations = [
        migrations.AddField(
            model_name='study',
            name='comments',
            field=models.TextField(max_length=2000, null=True, blank=True),
        ),
    ]
