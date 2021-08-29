# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('help', '0006_auto_20150710_0819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='content',
            field=models.FileField(null=True, upload_to='help/', blank=True),
        ),
    ]
