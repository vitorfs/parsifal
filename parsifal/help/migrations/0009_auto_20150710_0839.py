# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('help', '0008_auto_20150710_0829'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Media',
        ),
        migrations.AlterField(
            model_name='article',
            name='medias',
            field=models.ManyToManyField(to='core.Media', blank=True),
        ),
    ]
