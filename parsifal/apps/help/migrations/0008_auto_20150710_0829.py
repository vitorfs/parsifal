# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('help', '0007_auto_20150710_0827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='medias',
            field=models.ManyToManyField(to='help.Media', blank=True),
        ),
    ]
