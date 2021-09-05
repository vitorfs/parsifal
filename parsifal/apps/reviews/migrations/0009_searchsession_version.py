# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0008_auto_20150618_0836'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchsession',
            name='version',
            field=models.IntegerField(default=1),
        ),
    ]
