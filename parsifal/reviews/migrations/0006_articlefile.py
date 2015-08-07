# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0005_auto_20150615_1857'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('size', models.IntegerField(default=0)),
                ('article_file', models.FileField(upload_to=b'')),
                ('article', models.ForeignKey(to='reviews.Article')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
