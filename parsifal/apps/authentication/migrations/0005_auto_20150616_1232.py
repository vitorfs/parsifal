# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_profile_mendeley_session'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='mendeley_session',
            field=models.CharField(max_length=4000, null=True, blank=True),
        ),
    ]
