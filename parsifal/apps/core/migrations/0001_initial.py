# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField(max_length=500, null=True, blank=True)),
                ('media_type', models.CharField(max_length=5, choices=[('image', 'Image'), ('video', 'Video')])),
                ('content', models.FileField(null=True, upload_to='site/', blank=True)),
                ('content_type', models.CharField(max_length=255, null=True, blank=True)),
                ('width', models.IntegerField(default=0)),
                ('height', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Media',
                'verbose_name_plural': 'Medias',
            },
        ),
    ]
