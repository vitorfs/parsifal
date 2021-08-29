# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0007_folder_documents'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='note',
            field=models.CharField(max_length=2000, null=True, blank=True),
        ),
    ]
