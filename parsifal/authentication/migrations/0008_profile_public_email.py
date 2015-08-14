# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_profile_dropbox_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='public_email',
            field=models.EmailField(max_length=254, null=True, blank=True),
        ),
    ]
