# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'PersonLocation'
        db.create_table('location_personlocation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('device_udid', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('reported_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('altitude', self.gf('django.db.models.fields.FloatField')()),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('accuracy', self.gf('django.db.models.fields.FloatField')()),
            ('speed', self.gf('django.db.models.fields.FloatField')()),
            ('heading', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('location', ['PersonLocation'])


    def backwards(self, orm):
        
        # Deleting model 'PersonLocation'
        db.delete_table('location_personlocation')


    models = {
        'location.personlocation': {
            'Meta': {'object_name': 'PersonLocation'},
            'accuracy': ('django.db.models.fields.FloatField', [], {}),
            'altitude': ('django.db.models.fields.FloatField', [], {}),
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
