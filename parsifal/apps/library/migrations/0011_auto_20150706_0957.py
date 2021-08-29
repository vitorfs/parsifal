# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0010_auto_20150706_0954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='address',
            field=models.CharField(max_length=2000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='author',
            field=models.TextField(max_length=1000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='bibtexkey',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Bibtex key', blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='booktitle',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='chapter',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='coden',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='crossref',
            field=models.CharField(max_length=1000, null=True, verbose_name=b'Cross-referenced', blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='doi',
            field=models.CharField(max_length=255, null=True, verbose_name=b'DOI', blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='edition',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='editor',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='howpublished',
            field=models.CharField(max_length=1000, null=True, verbose_name=b'How it was published', blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='institution',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='isbn',
            field=models.CharField(max_length=255, null=True, verbose_name=b'ISBN', blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='issn',
            field=models.CharField(max_length=255, null=True, verbose_name=b'ISSN', blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='journal',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='language',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='month',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='number',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='organization',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='publication_type',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='publisher',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='school',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='series',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='title',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='url',
            field=models.CharField(max_length=1000, null=True, verbose_name=b'URL', blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='volume',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='year',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
