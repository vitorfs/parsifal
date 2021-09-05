# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_auto_20150626_1649'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='key',
        ),
        migrations.AlterField(
            model_name='document',
            name='month',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
    ]
