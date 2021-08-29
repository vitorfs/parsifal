# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0016_sharedfolder_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='slug',
            field=models.SlugField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='sharedfolder',
            name='slug',
            field=models.SlugField(max_length=255, null=True, blank=True),
        ),
    ]
