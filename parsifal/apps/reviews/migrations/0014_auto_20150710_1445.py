# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0011_auto_20150706_0957'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0013_auto_20150708_1511'),
    ]

    operations = [
        migrations.CreateModel(
            name='Study',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default='U', max_length=1, choices=[('U', 'Unclassified'), ('R', 'Rejected'), ('A', 'Accepted'), ('D', 'Duplicated')])),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Document')),
            ],
        ),
        migrations.CreateModel(
            name='StudySelection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('has_finished', models.BooleanField(default=False)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.Review')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='study',
            name='study_selection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.StudySelection'),
        ),
    ]
