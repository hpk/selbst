# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'PersonLocation.at_home'
        db.add_column('location_personlocation', 'at_home', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'PersonLocation.at_home'
        db.delete_column('location_personlocation', 'at_home')


    models = {
        'location.personlocation': {
            'Meta': {'object_name': 'PersonLocation'},
            'accuracy': ('django.db.models.fields.FloatField', [], {}),
            'altitude': ('django.db.models.fields.FloatField', [], {}),
            'at_home': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'device_udid': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'heading': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'reported_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'speed': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['location']
