# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Person'
        db.delete_table(u'personal_info_person')

        # Deleting model 'WebRequest'
        db.delete_table(u'personal_info_webrequest')

        # Adding model 'Person'
        db.create_table(u'personal_info_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('birth_date', self.gf('django.db.models.fields.DateField')()),
            ('bio', self.gf('django.db.models.fields.TextField')()),
            ('contacts_email', self.gf('django.db.models.fields.EmailField')(max_length=128)),
            ('contacts_jabber_id', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('contacts_skype_id', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('contacts_other', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'personal_info', ['Person'])

        # Adding model 'WebRequest'
        db.create_table(u'personal_info_webrequest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('path', self.gf('django.db.models.fields.TextField')()),
            ('get', self.gf('django.db.models.fields.TextField')()),
            ('post', self.gf('django.db.models.fields.TextField')()),
            ('remote_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=7)),
        ))
        db.send_create_signal(u'personal_info', ['WebRequest'])


    def backwards(self, orm):
        # Deleting model 'Person'
        db.delete_table(u'personal_info_person')

        # Deleting model 'WebRequest'
        db.delete_table(u'personal_info_webrequest')


    models = {
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
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'personal_info.webrequest': {
            'Meta': {'object_name': 'WebRequest'},
            'get': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'path': ('django.db.models.fields.TextField', [], {}),
            'post': ('django.db.models.fields.TextField', [], {}),
            'remote_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['personal_info']