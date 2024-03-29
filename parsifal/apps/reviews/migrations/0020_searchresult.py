# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import parsifal.apps.reviews.models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0013_auto_20150710_1614'),
        ('reviews', '0019_study_comments'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('imported_file', models.FileField(null=True, upload_to=parsifal.apps.reviews.models.search_result_file_upload_to)),
                ('documents', models.ManyToManyField(to='library.Document')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.Review')),
                ('search_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.SearchSession', null=True)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.Source')),
            ],
        ),
    ]
