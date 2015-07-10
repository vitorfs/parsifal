# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('help', '0005_category_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField(max_length=500, null=True, blank=True)),
                ('media_type', models.CharField(max_length=5, choices=[('image', 'Image'), ('video', 'Video')])),
                ('content', models.FileField(upload_to='help/')),
                ('content_type', models.CharField(max_length=255, null=True, blank=True)),
                ('width', models.IntegerField(default=0)),
                ('height', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Media',
                'verbose_name_plural': 'Medias',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='description',
            field=models.TextField(max_length=500, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='article',
            name='references',
            field=models.TextField(max_length=2000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.TextField(max_length=4000, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='article',
            name='medias',
            field=models.ManyToManyField(to='help.Media'),
        ),
    ]
