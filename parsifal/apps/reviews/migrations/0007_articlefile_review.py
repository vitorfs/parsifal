# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_articlefile'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlefile',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, default=1, to='reviews.Review'),
            preserve_default=False,
        ),
    ]
