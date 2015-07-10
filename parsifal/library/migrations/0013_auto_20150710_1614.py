# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0012_auto_20150710_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentfile',
            name='document_file',
            field=models.FileField(upload_to='library/'),
        ),
    ]
