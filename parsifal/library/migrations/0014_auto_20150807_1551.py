# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0023_auto_20150806_1438'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library', '0013_auto_20150710_1614'),
    ]

    operations = [
        migrations.CreateModel(
            name='SharedFolder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('slug', models.SlugField(max_length=55)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(related_name='shared_folders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Shared Folder',
                'verbose_name_plural': 'Shared Folders',
            },
        ),
        migrations.AddField(
            model_name='document',
            name='review',
            field=models.ForeignKey(related_name='documents', to='reviews.Review', null=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='user',
            field=models.ForeignKey(related_name='documents', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='shared_folder',
            field=models.ForeignKey(related_name='documents', to='library.SharedFolder', null=True),
        ),
    ]
