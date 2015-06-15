# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bibtex_key', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=1000, blank=True)),
                ('journal', models.CharField(max_length=1000, blank=True)),
                ('year', models.CharField(max_length=10, blank=True)),
                ('pages', models.CharField(max_length=20, blank=True)),
                ('volume', models.CharField(max_length=100, blank=True)),
                ('author', models.CharField(max_length=1000, blank=True)),
                ('abstract', models.TextField(max_length=4000, blank=True)),
                ('document_type', models.CharField(max_length=100, blank=True)),
                ('status', models.CharField(default=b'U', max_length=1, choices=[(b'U', b'Unclassified'), (b'R', b'Rejected'), (b'A', b'Accepted'), (b'D', b'Duplicated')])),
                ('comments', models.TextField(max_length=4000, blank=True)),
            ],
            options={
                'verbose_name': 'Article',
                'verbose_name_plural': 'Articles',
            },
        ),
        migrations.CreateModel(
            name='DataExtraction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=1000, blank=True)),
                ('article', models.ForeignKey(to='reviews.Article')),
            ],
        ),
        migrations.CreateModel(
            name='DataExtractionField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=255)),
                ('field_type', models.CharField(max_length=1, choices=[(b'B', b'Boolean Field'), (b'S', b'String Field'), (b'F', b'Float Field'), (b'I', b'Integer Field'), (b'D', b'Date Field'), (b'O', b'Select One Field'), (b'M', b'Select Many Field')])),
            ],
        ),
        migrations.CreateModel(
            name='DataExtractionLookup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=1000)),
                ('field', models.ForeignKey(to='reviews.DataExtractionField')),
            ],
            options={
                'ordering': ('value',),
                'verbose_name': 'Lookup Value',
                'verbose_name_plural': 'Lookup Values',
            },
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=200)),
                ('related_to', models.CharField(blank=True, max_length=1, choices=[(b'P', b'Population'), (b'I', b'Intervention'), (b'C', b'Comparison'), (b'O', b'Outcome')])),
            ],
            options={
                'ordering': ('description',),
                'verbose_name': 'Keyword',
                'verbose_name_plural': 'Keywords',
            },
        ),
        migrations.CreateModel(
            name='QualityAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=255)),
                ('weight', models.FloatField()),
            ],
            options={
                'ordering': ('-weight',),
                'verbose_name': 'Quality Assessment Answer',
                'verbose_name_plural': 'Quality Assessment Answers',
            },
        ),
        migrations.CreateModel(
            name='QualityAssessment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.ForeignKey(to='reviews.QualityAnswer', null=True)),
                ('article', models.ForeignKey(to='reviews.Article')),
            ],
        ),
        migrations.CreateModel(
            name='QualityQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Quality Assessment Question',
                'verbose_name_plural': 'Quality Assessment Questions',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.CharField(max_length=500)),
                ('parent_question', models.ForeignKey(related_name='+', to='reviews.Question', null=True)),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.SlugField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=500)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField()),
                ('objective', models.TextField(max_length=1000)),
                ('status', models.CharField(default=b'U', max_length=1, choices=[(b'U', b'Unpublished'), (b'P', b'Published')])),
                ('quality_assessment_cutoff_score', models.FloatField(default=0.0)),
                ('study_selection_strategy', models.CharField(default=b'S', max_length=1, choices=[(b'S', b'Single Form'), (b'M', b'Multiple Forms')])),
                ('quality_assessment_strategy', models.CharField(default=b'S', max_length=1, choices=[(b'S', b'Single Form'), (b'M', b'Multiple Forms')])),
                ('data_extraction_strategy', models.CharField(default=b'S', max_length=1, choices=[(b'S', b'Single Form'), (b'M', b'Multiple Forms')])),
                ('population', models.CharField(max_length=200, blank=True)),
                ('intervention', models.CharField(max_length=200, blank=True)),
                ('comparison', models.CharField(max_length=200, blank=True)),
                ('outcome', models.CharField(max_length=200, blank=True)),
                ('context', models.CharField(max_length=200, blank=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('co_authors', models.ManyToManyField(related_name='co_authors', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Review',
                'verbose_name_plural': 'Reviews',
            },
        ),
        migrations.CreateModel(
            name='SearchSession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('search_string', models.TextField(max_length=2000)),
                ('review', models.ForeignKey(to='reviews.Review')),
            ],
        ),
        migrations.CreateModel(
            name='SelectionCriteria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('criteria_type', models.CharField(max_length=1, choices=[(b'I', b'Inclusion'), (b'E', b'Exclusion')])),
                ('description', models.CharField(max_length=200)),
                ('review', models.ForeignKey(to='reviews.Review')),
            ],
            options={
                'ordering': ('description',),
                'verbose_name': 'Selection Criteria',
                'verbose_name_plural': 'Selection Criterias',
            },
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=200)),
                ('is_default', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Source',
                'verbose_name_plural': 'Sources',
            },
        ),
        migrations.AddField(
            model_name='searchsession',
            name='source',
            field=models.ForeignKey(to='reviews.Source', null=True),
        ),
        migrations.AddField(
            model_name='review',
            name='sources',
            field=models.ManyToManyField(to='reviews.Source'),
        ),
        migrations.AddField(
            model_name='question',
            name='review',
            field=models.ForeignKey(to='reviews.Review'),
        ),
        migrations.AddField(
            model_name='qualityquestion',
            name='review',
            field=models.ForeignKey(to='reviews.Review'),
        ),
        migrations.AddField(
            model_name='qualityassessment',
            name='question',
            field=models.ForeignKey(to='reviews.QualityQuestion'),
        ),
        migrations.AddField(
            model_name='qualityassessment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='qualityanswer',
            name='review',
            field=models.ForeignKey(to='reviews.Review'),
        ),
        migrations.AddField(
            model_name='keyword',
            name='review',
            field=models.ForeignKey(to='reviews.Review'),
        ),
        migrations.AddField(
            model_name='keyword',
            name='synonym_of',
            field=models.ForeignKey(to='reviews.Keyword', null=True),
        ),
        migrations.AddField(
            model_name='dataextractionfield',
            name='review',
            field=models.ForeignKey(to='reviews.Review'),
        ),
        migrations.AddField(
            model_name='dataextraction',
            name='field',
            field=models.ForeignKey(to='reviews.DataExtractionField'),
        ),
        migrations.AddField(
            model_name='dataextraction',
            name='select_values',
            field=models.ManyToManyField(to='reviews.DataExtractionLookup'),
        ),
        migrations.AddField(
            model_name='dataextraction',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='review',
            field=models.ForeignKey(to='reviews.Review'),
        ),
        migrations.AddField(
            model_name='article',
            name='source',
            field=models.ForeignKey(to='reviews.Source', null=True),
        ),
    ]
