# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0006_auto_20150627_1007'),
    ]

    operations = [
        migrations.AddField(
            model_name='folder',
            name='documents',
            field=models.ManyToManyField(to='library.Document'),
        ),
    ]
