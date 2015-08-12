# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0024_auto_20150810_0807'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomArticleStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('review', models.ForeignKey(to='reviews.Review')),
            ],
            options={
                'verbose_name': 'Custom Article Status',
                'verbose_name_plural': 'Custom Article Status',
            },
        ),
    ]
