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
        ))
        db.send_create_signal(u'reviews', ['Source'])

        # Adding model 'Question'
        db.create_table(u'reviews_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('population', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('intervention', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('comparison', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('outcome', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('question_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'reviews', ['Question'])

        # Adding field 'Review.objective'
        db.add_column(u'reviews_review', 'objective',
                      self.gf('django.db.models.fields.TextField')(max_length=1000, null=True),
                      keep_default=False)

        # Adding M2M table for field questions on 'Review'
        m2m_table_name = db.shorten_name(u'reviews_review_questions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('review', models.ForeignKey(orm[u'reviews.review'], null=False)),
            ('question', models.ForeignKey(orm[u'reviews.question'], null=False))
        ))
        db.create_unique(m2m_table_name, ['review_id', 'question_id'])

        # Adding M2M table for field sources on 'Review'
        m2m_table_name = db.shorten_name(u'reviews_review_sources')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('review', models.ForeignKey(orm[u'reviews.review'], null=False)),
            ('source', models.ForeignKey(orm[u'reviews.source'], null=False))
        ))
        db.create_unique(m2m_table_name, ['review_id', 'source_id'])


    def backwards(self, orm):
        # Deleting model 'Source'
        db.delete_table(u'reviews_source')

        # Deleting model 'Question'
        db.delete_table(u'reviews_question')

        # Deleting field 'Review.objective'
        db.delete_column(u'reviews_review', 'objective')

        # Removing M2M table for field questions on 'Review'
        db.delete_table(db.shorten_name(u'reviews_review_questions'))

        # Removing M2M table for field sources on 'Review'
        db.delete_table(db.shorten_name(u'reviews_review_sources'))


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
        u'reviews.question': {
            'Meta': {'object_name': 'Question'},
            'comparison': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intervention': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'outcome': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'population': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'question_type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'reviews.review': {
            'Meta': {'object_name': 'Review'},
            'co_authors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'co+'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {}),
            'objective': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True'}),
            'questions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['reviews.Question']", 'symmetrical': 'False'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'sources': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['reviews.Source']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'reviews.source': {
            'Meta': {'object_name': 'Source'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['reviews']