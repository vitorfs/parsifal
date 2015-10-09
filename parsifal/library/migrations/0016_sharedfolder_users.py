# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library', '0015_auto_20151009_1543'),
    ]

    operations = [
        migrations.AddField(
            model_name='sharedfolder',
            name='users',
            field=models.ManyToManyField(related_name='shared_folders', through='library.Collaborator', to=settings.AUTH_USER_MODEL),
        ),
    ]
