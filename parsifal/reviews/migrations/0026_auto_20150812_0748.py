# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0025_customarticlestatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customarticlestatus',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='custom_article_status', to='reviews.Review'),
        ),
    ]
