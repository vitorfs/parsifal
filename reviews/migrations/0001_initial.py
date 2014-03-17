# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Source'
        db.create_table(u'reviews_source', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('is_default', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'reviews', ['Source'])

        # Adding model 'Review'
        db.create_table(u'reviews_review', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')()),
            ('objective', self.gf('django.db.models.fields.TextField')(max_length=1000)),
            ('status', self.gf('django.db.models.fields.CharField')(default='U', max_length=1)),
            ('quality_assessment_cutoff_score', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('study_selection_strategy', self.gf('django.db.models.fields.CharField')(default='S', max_length=1)),
            ('quality_assessment_strategy', self.gf('django.db.models.fields.CharField')(default='S', max_length=1)),
            ('data_extraction_strategy', self.gf('django.db.models.fields.CharField')(default='S', max_length=1)),
        ))
        db.send_create_signal(u'reviews', ['Review'])

        # Adding M2M table for field sources on 'Review'
        m2m_table_name = db.shorten_name(u'reviews_review_sources')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('review', models.ForeignKey(orm[u'reviews.review'], null=False)),
            ('source', models.ForeignKey(orm[u'reviews.source'], null=False))
        ))
        db.create_unique(m2m_table_name, ['review_id', 'source_id'])

        # Adding M2M table for field co_authors on 'Review'
        m2m_table_name = db.shorten_name(u'reviews_review_co_authors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('review', models.ForeignKey(orm[u'reviews.review'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['review_id', 'user_id'])

        # Adding model 'Question'
        db.create_table(u'reviews_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('review', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reviews.Review'])),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('population', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('intervention', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('comparison', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('outcome', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('question_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'reviews', ['Question'])

        # Adding model 'SelectionCriteria'
        db.create_table(u'reviews_selectioncriteria', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('review', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reviews.Review'])),
            ('criteria_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'reviews', ['SelectionCriteria'])

        # Adding model 'SearchSession'
        db.create_table(u'reviews_searchsession', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('review', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reviews.Review'])),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reviews.Source'], null=True)),
            ('search_string', self.gf('django.db.models.fields.TextField')(max_length=2000)),
        ))
        db.send_create_signal(u'reviews', ['SearchSession'])

        # Adding model 'Article'
        db.create_table(u'reviews_article', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('review', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reviews.Review'])),
            ('bibtex_key', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
            ('journal', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
            ('year', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reviews.Source'], null=True)),
            ('pages', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('volume', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
            ('abstract', self.gf('django.db.models.fields.TextField')(max_length=4000, blank=True)),
            ('document_type', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('author_keywords', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
            ('note', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
            ('search_session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reviews.SearchSession'], null=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='U', max_length=1)),
        ))
        db.send_create_signal(u'reviews', ['Article'])

        # Adding model 'Keyword'
        db.create_table(u'reviews_keyword', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('review', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reviews.Review'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('synonym_of', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reviews.Keyword'], null=True)),
        ))
        db.send_create_signal(u'reviews', ['Keyword'])

        # Adding model 'QualityAnswer'
        db.create_table(u'reviews_qualityanswer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('review', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reviews.Review'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('weight', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'reviews', ['QualityAnswer'])

        # Adding model 'QualityQuestion'
        db.create_table(u'reviews_qualityquestion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('review', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reviews.Review'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'reviews', ['QualityQuestion'])

        # Adding model 'QualityAssessment'
        db.create_table(u'reviews_qualityassessment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reviews.Article'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reviews.QualityQuestion'])),
            ('answer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reviews.QualityAnswer'], null=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'reviews', ['QualityAssessment'])

        # Adding model 'DataExtractionField'
        db.create_table(u'reviews_dataextractionfield', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('review', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reviews.Review'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('field_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'reviews', ['DataExtractionField'])

        # Adding model 'DataExtractionLookup'
        db.create_table(u'reviews_dataextractionlookup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('field', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reviews.DataExtractionField'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'reviews', ['DataExtractionLookup'])

        # Adding model 'DataExtraction'
        db.create_table(u'reviews_dataextraction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reviews.Article'])),
            ('field', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reviews.DataExtractionField'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'reviews', ['DataExtraction'])

        # Adding M2M table for field select_values on 'DataExtraction'
        m2m_table_name = db.shorten_name(u'reviews_dataextraction_select_values')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dataextraction', models.ForeignKey(orm[u'reviews.dataextraction'], null=False)),
            ('dataextractionlookup', models.ForeignKey(orm[u'reviews.dataextractionlookup'], null=False))
        ))
        db.create_unique(m2m_table_name, ['dataextraction_id', 'dataextractionlookup_id'])


    def backwards(self, orm):
        # Deleting model 'Source'
        db.delete_table(u'reviews_source')

        # Deleting model 'Review'
        db.delete_table(u'reviews_review')

        # Removing M2M table for field sources on 'Review'
        db.delete_table(db.shorten_name(u'reviews_review_sources'))

        # Removing M2M table for field co_authors on 'Review'
        db.delete_table(db.shorten_name(u'reviews_review_co_authors'))

        # Deleting model 'Question'
        db.delete_table(u'reviews_question')

        # Deleting model 'SelectionCriteria'
        db.delete_table(u'reviews_selectioncriteria')

        # Deleting model 'SearchSession'
        db.delete_table(u'reviews_searchsession')

        # Deleting model 'Article'
        db.delete_table(u'reviews_article')

        # Deleting model 'Keyword'
        db.delete_table(u'reviews_keyword')

        # Deleting model 'QualityAnswer'
        db.delete_table(u'reviews_qualityanswer')

        # Deleting model 'QualityQuestion'
        db.delete_table(u'reviews_qualityquestion')

        # Deleting model 'QualityAssessment'
        db.delete_table(u'reviews_qualityassessment')

        # Deleting model 'DataExtractionField'
        db.delete_table(u'reviews_dataextractionfield')

        # Deleting model 'DataExtractionLookup'
        db.delete_table(u'reviews_dataextractionlookup')

        # Deleting model 'DataExtraction'
        db.delete_table(u'reviews_dataextraction')

        # Removing M2M table for field select_values on 'DataExtraction'
        db.delete_table(db.shorten_name(u'reviews_dataextraction_select_values'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'reviews.article': {
            'Meta': {'object_name': 'Article'},
            'abstract': ('django.db.models.fields.TextField', [], {'max_length': '4000', 'blank': 'True'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'author_keywords': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'bibtex_key': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'document_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'journal': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'pages': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'review': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reviews.Review']"}),
            'search_session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reviews.SearchSession']", 'null': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reviews.Source']", 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'U'", 'max_length': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'volume': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        u'reviews.dataextraction': {
            'Meta': {'object_name': 'DataExtraction'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reviews.Article']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'field': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reviews.DataExtractionField']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'select_values': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['reviews.DataExtractionLookup']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'reviews.dataextractionfield': {
            'Meta': {'object_name': 'DataExtractionField'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'field_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'review': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reviews.Review']"})
        },
        u'reviews.dataextractionlookup': {
            'Meta': {'ordering': "('value',)", 'object_name': 'DataExtractionLookup'},
            'field': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reviews.DataExtractionField']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'reviews.keyword': {
            'Meta': {'ordering': "('description',)", 'object_name': 'Keyword'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'review': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reviews.Review']"}),
            'synonym_of': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reviews.Keyword']", 'null': 'True'})
        },
        u'reviews.qualityanswer': {
            'Meta': {'ordering': "('-weight',)", 'object_name': 'QualityAnswer'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'review': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reviews.Review']"}),
            'weight': ('django.db.models.fields.FloatField', [], {})
        },
        u'reviews.qualityassessment': {
            'Meta': {'object_name': 'QualityAssessment'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reviews.QualityAnswer']", 'null': 'True'}),
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reviews.Article']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reviews.QualityQuestion']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'})
        },
        u'reviews.qualityquestion': {
            'Meta': {'object_name': 'QualityQuestion'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'review': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reviews.Review']"})
        },
        u'reviews.question': {
            'Meta': {'object_name': 'Question'},
            'comparison': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intervention': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'outcome': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'population': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'question_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'review': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reviews.Review']"})
        },
        u'reviews.review': {
            'Meta': {'object_name': 'Review'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'co_authors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'co_authors'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data_extraction_strategy': ('django.db.models.fields.CharField', [], {'default': "'S'", 'max_length': '1'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'objective': ('django.db.models.fields.TextField', [], {'max_length': '1000'}),
            'quality_assessment_cutoff_score': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'quality_assessment_strategy': ('django.db.models.fields.CharField', [], {'default': "'S'", 'max_length': '1'}),
            'sources': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['reviews.Source']", 'symmetrical': 'False'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'U'", 'max_length': '1'}),
            'study_selection_strategy': ('django.db.models.fields.CharField', [], {'default': "'S'", 'max_length': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'reviews.searchsession': {
            'Meta': {'object_name': 'SearchSession'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'review': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reviews.Review']"}),
            'search_string': ('django.db.models.fields.TextField', [], {'max_length': '2000'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reviews.Source']", 'null': 'True'})
        },
        u'reviews.selectioncriteria': {
            'Meta': {'ordering': "('description',)", 'object_name': 'SelectionCriteria'},
            'criteria_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'review': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reviews.Review']"})
        },
        u'reviews.source': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Source'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['reviews']