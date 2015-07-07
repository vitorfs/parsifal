# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_profile_mendeley_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='mendeley_token',
            field=models.CharField(max_length=2000, null=True, blank=True),
        ),
    ]
