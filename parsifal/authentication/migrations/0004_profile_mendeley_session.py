# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20150615_2138'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='mendeley_session',
            field=models.CharField(max_length=2000, null=True, blank=True),
        ),
    ]
