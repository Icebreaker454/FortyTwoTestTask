# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'WebRequest.priority'
        db.add_column(u'personal_info_webrequest', 'priority',
                      self.gf('django.db.models.fields.SmallIntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'WebRequest.priority'
        db.delete_column(u'personal_info_webrequest', 'priority')


    models = {
        u'personal_info.modellog': {
            'Meta': {'object_name': 'ModelLog'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'model_id': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True'})
        },
        u'personal_info.person': {
            'Meta': {'object_name': 'Person'},
            'bio': ('django.db.models.fields.TextField', [], {}),
            'birth_date': ('django.db.models.fields.DateField', [], {}),
            'contacts_email': ('django.db.models.fields.EmailField', [], {'max_length': '128'}),
            'contacts_jabber_id': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'contacts_other': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'contacts_skype_id': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'personal_info.webrequest': {
            'Meta': {'object_name': 'WebRequest'},
            'get': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'path': ('django.db.models.fields.TextField', [], {}),
            'post': ('django.db.models.fields.TextField', [], {}),
            'priority': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'remote_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['personal_info']