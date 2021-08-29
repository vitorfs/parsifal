# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_articlefile_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlefile',
            name='article_file',
            field=models.FileField(upload_to=b'library/'),
        ),
    ]
