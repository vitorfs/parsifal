# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='mendeley_token',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
