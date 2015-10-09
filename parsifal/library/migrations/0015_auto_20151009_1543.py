# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library', '0014_auto_20150807_1551'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collaborator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('joined_at', models.DateTimeField(auto_now_add=True)),
                ('is_owner', models.BooleanField(default=False)),
                ('access', models.CharField(default=b'R', max_length=1, choices=[(b'R', b'Read'), (b'W', b'Write'), (b'A', b'Admin')])),
            ],
            options={
                'verbose_name': 'Collaborator',
                'verbose_name_plural': 'Collaborators',
            },
        ),
        migrations.RemoveField(
            model_name='sharedfolder',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='sharedfolder',
            name='users',
        ),
        migrations.AlterField(
            model_name='folder',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='folder',
            name='slug',
            field=models.SlugField(max_length=255),
        ),
        migrations.AlterField(
            model_name='sharedfolder',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='sharedfolder',
            name='slug',
            field=models.SlugField(max_length=255),
        ),
        migrations.AlterUniqueTogether(
            name='folder',
            unique_together=set([('name', 'user')]),
        ),
        migrations.AddField(
            model_name='collaborator',
            name='shared_folder',
            field=models.ForeignKey(to='library.SharedFolder'),
        ),
        migrations.AddField(
            model_name='collaborator',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
