# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0025_customarticlestatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customarticlestatus',
            name='review',
            field=models.ForeignKey(related_name='custom_article_status', to='reviews.Review'),
        ),
    ]
