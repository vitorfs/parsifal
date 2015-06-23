# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('help', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='parent',
            field=models.ForeignKey(blank=True, to='help.Article', null=True),
        ),
    ]
