# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0020_searchresult'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyword',
            name='related_to',
            field=models.CharField(blank=True, max_length=1, choices=[('', 'Select...'), ('P', 'Population'), ('I', 'Intervention'), ('C', 'Comparison'), ('O', 'Outcome')]),
        ),
        migrations.AlterField(
            model_name='keyword',
            name='synonym_of',
            field=models.ForeignKey(related_name='synonyms', to='reviews.Keyword', null=True),
        ),
    ]
