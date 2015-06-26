# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_folder_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='slug',
            field=models.SlugField(max_length=55),
        ),
    ]
