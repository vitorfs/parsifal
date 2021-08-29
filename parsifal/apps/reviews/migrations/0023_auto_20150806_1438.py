# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0022_auto_20150804_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyword',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='keywords', to='reviews.Review'),
        ),
    ]
