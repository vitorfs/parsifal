# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0010_auto_20150623_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='comments',
            field=models.TextField(max_length=2000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='document_type',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
