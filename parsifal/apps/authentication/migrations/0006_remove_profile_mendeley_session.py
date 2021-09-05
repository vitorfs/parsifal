# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_auto_20150616_1232'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='mendeley_session',
        ),
    ]
