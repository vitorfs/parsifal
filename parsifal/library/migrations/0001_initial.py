# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import parsifal.library.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bibtexkey', models.CharField(max_length=50)),
                ('entry_type', models.CharField(max_length=13, choices=[('article', 'Article'), ('book', 'Book'), ('booklet', 'Booklet'), ('conference', 'Conference'), ('inbook', 'Inbook'), ('incollection', 'Incollection'), ('inproceedings', 'Inproceedings'), ('manual', 'Manual'), ('mastersthesis', "Master's Thesis"), ('misc', 'Misc'), ('phdthesis', 'Ph.D. Thesis'), ('proceedings', 'Proceedings'), ('techreport', 'Tech Report'), ('unpublished', 'Unpublished')])),
                ('address', models.CharField(max_length=255, null=True, blank=True)),
                ('annote', models.CharField(max_length=255, null=True, blank=True)),
                ('author', models.CharField(max_length=255, null=True, blank=True)),
                ('booktitle', models.CharField(max_length=255, null=True, blank=True)),
                ('chapter', models.CharField(max_length=255, null=True, blank=True)),
                ('crossref', models.CharField(max_length=255, null=True, blank=True)),
                ('edition', models.CharField(max_length=255, null=True, blank=True)),
                ('editor', models.CharField(max_length=255, null=True, blank=True)),
                ('howpublished', models.CharField(max_length=255, null=True, blank=True)),
                ('institution', models.CharField(max_length=255, null=True, blank=True)),
                ('journal', models.CharField(max_length=255, null=True, blank=True)),
                ('key', models.CharField(max_length=255, null=True, blank=True)),
                ('month', models.CharField(max_length=255, null=True, blank=True)),
                ('note', models.CharField(max_length=255, null=True, blank=True)),
                ('number', models.CharField(max_length=255, null=True, blank=True)),
                ('organization', models.CharField(max_length=255, null=True, blank=True)),
                ('pages', models.CharField(max_length=255, null=True, blank=True)),
                ('publisher', models.CharField(max_length=255, null=True, blank=True)),
                ('school', models.CharField(max_length=255, null=True, blank=True)),
                ('series', models.CharField(max_length=255, null=True, blank=True)),
                ('title', models.CharField(max_length=255, null=True, blank=True)),
                ('publication_type', models.CharField(max_length=255, null=True, blank=True)),
                ('volume', models.CharField(max_length=255, null=True, blank=True)),
                ('year', models.CharField(max_length=10, null=True, blank=True)),
                ('abstract', models.TextField(max_length=4000, null=True, blank=True)),
                ('coden', models.CharField(max_length=255, null=True, blank=True)),
                ('doi', models.CharField(max_length=50, null=True, blank=True)),
                ('isbn', models.CharField(max_length=30, null=True, blank=True)),
                ('issn', models.CharField(max_length=30, null=True, blank=True)),
                ('keywords', models.CharField(max_length=255, null=True, blank=True)),
                ('language', models.CharField(max_length=255, null=True, blank=True)),
                ('url', models.CharField(max_length=255, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Document',
                'verbose_name_plural': 'Documents',
            },
        ),
        migrations.CreateModel(
            name='DocumentFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('document_file', models.FileField(upload_to=parsifal.library.models.document_file_upload_to)),
                ('filename', models.CharField(max_length=255)),
                ('size', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('document', models.ForeignKey(to='library.Document')),
            ],
            options={
                'verbose_name': 'Document File',
                'verbose_name_plural': 'Document Files',
            },
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Folder',
                'verbose_name_plural': 'Folders',
            },
        ),
    ]
