# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0022_auto_20150804_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyword',
            name='review',
            field=models.ForeignKey(related_name='keywords', to='reviews.Review'),
        ),
    ]
