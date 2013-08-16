# -*- coding: utf-8 -*-
import datetime
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
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')()),
            ('objective', self.gf('django.db.models.fields.TextField')(max_length=1000, null=True)),
        ))
        db.send_create_signal(u'reviews', ['Review'])

        # Adding M2M table for field co_authors on 'Review'
        m2m_table_name = db.shorten_name(u'reviews_review_co_authors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('review', models.ForeignKey(orm[u'reviews.review'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['review_id', 'user_id'])

        # Adding M2M table for field sources on 'Review'
        m2m_table_name = db.shorten_name(u'reviews_review_sources')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('review', models.ForeignKey(orm[u'reviews.review'], null=False)),
            ('source', models.ForeignKey(orm[u'reviews.source'], null=False))
        ))
        db.create_unique(m2m_table_name, ['review_id', 'source_id'])

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

        # Adding model 'Article'
        db.create_table(u'reviews_article', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('review', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reviews.Review'])),
            ('bibtex_key', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('journal', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('year', self.gf('django.db.models.fields.CharField')(max_length=4, null=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reviews.Source'], null=True)),
            ('pages', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('volume', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=500, null=True)),
            ('abstract', self.gf('django.db.models.fields.TextField')(max_length=4000, null=True)),
            ('document_type', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('author_keywords', self.gf('django.db.models.fields.CharField')(max_length=500, null=True)),
            ('note', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
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


    def backwards(self, orm):
        # Deleting model 'Source'
        db.delete_table(u'reviews_source')

        # Deleting model 'Review'
        db.delete_table(u'reviews_review')

        # Removing M2M table for field co_authors on 'Review'
        db.delete_table(db.shorten_name(u'reviews_review_co_authors'))

        # Removing M2M table for field sources on 'Review'
        db.delete_table(db.shorten_name(u'reviews_review_sources'))

        # Deleting model 'Question'
        db.delete_table(u'reviews_question')

        # Deleting model 'SelectionCriteria'
        db.delete_table(u'reviews_selectioncriteria')

        # Deleting model 'Article'
        db.delete_table(u'reviews_article')

        # Deleting model 'Keyword'
        db.delete_table(u'reviews_keyword')


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
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
            'abstract': ('django.db.models.fields.TextField', [], {'max_length': '4000', 'null': 'True'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True'}),
            'author_keywords': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True'}),
            'bibtex_key': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'document_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'journal': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'pages': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'review': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reviews.Review']"}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reviews.Source']", 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'volume': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True'})
        },
        u'reviews.keyword': {
            'Meta': {'object_name': 'Keyword'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'review': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reviews.Review']"}),
            'synonym_of': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reviews.Keyword']", 'null': 'True'})
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
            'co_authors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'co+'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'objective': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True'}),
            'sources': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['reviews.Source']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'reviews.selectioncriteria': {
            'Meta': {'object_name': 'SelectionCriteria'},
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