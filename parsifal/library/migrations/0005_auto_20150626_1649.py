# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_auto_20150626_0841'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='folder',
            options={'ordering': ('name',), 'verbose_name': 'Folder', 'verbose_name_plural': 'Folders'},
        ),
        migrations.RemoveField(
            model_name='document',
            name='annote',
        ),
        migrations.AlterField(
            model_name='document',
            name='author',
            field=models.TextField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='bibtexkey',
            field=models.CharField(max_length=50, null=True, verbose_name=b'Bibtex key', blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='crossref',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Cross-referenced', blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='doi',
            field=models.CharField(max_length=50, null=True, verbose_name=b'DOI', blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='entry_type',
            field=models.CharField(blank=True, max_length=13, null=True, verbose_name=b'Document type', choices=[('article', 'Article'), ('book', 'Book'), ('booklet', 'Booklet'), ('conference', 'Conference'), ('inbook', 'Inbook'), ('incollection', 'Incollection'), ('inproceedings', 'Inproceedings'), ('manual', 'Manual'), ('mastersthesis', "Master's Thesis"), ('misc', 'Misc'), ('phdthesis', 'Ph.D. Thesis'), ('proceedings', 'Proceedings'), ('techreport', 'Tech Report'), ('unpublished', 'Unpublished')]),
        ),
        migrations.AlterField(
            model_name='document',
            name='howpublished',
            field=models.CharField(max_length=255, null=True, verbose_name=b'How it was published', blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='isbn',
            field=models.CharField(max_length=30, null=True, verbose_name=b'ISBN', blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='issn',
            field=models.CharField(max_length=30, null=True, verbose_name=b'ISSN', blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='keywords',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='url',
            field=models.CharField(max_length=255, null=True, verbose_name=b'URL', blank=True),
        ),
    ]
