# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Thermostat.mode'
        db.add_column('climatecontrol_thermostat', 'mode', self.gf('django.db.models.fields.CharField')(default='heat', max_length='4'), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Thermostat.mode'
        db.delete_column('climatecontrol_thermostat', 'mode')


    models = {
        'climatecontrol.recurringweeklysetpoint': {
            'Meta': {'object_name': 'RecurringWeeklySetpoint', '_ormbases': ['climatecontrol.TemperatureSetpoint']},
            'day_of_week': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'hour': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'minute': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'temperaturesetpoint_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['climatecontrol.TemperatureSetpoint']", 'unique': 'True', 'primary_key': 'True'})
        },
        'climatecontrol.scheduledholdsetpoint': {
            'Meta': {'object_name': 'ScheduledHoldSetpoint', '_ormbases': ['climatecontrol.TemperatureSetpoint']},
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'temperaturesetpoint_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['climatecontrol.TemperatureSetpoint']", 'unique': 'True', 'primary_key': 'True'})
        },
        'climatecontrol.temperaturesetpoint': {
            'Meta': {'object_name': 'TemperatureSetpoint'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mode': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'setpoint': ('django.db.models.fields.FloatField', [], {}),
            'thermostat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['climatecontrol.Thermostat']", 'null': 'True', 'blank': 'True'})
        },
        'climatecontrol.thermostat': {
            'Meta': {'object_name': 'Thermostat'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'last_recurring_setpoint': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'thermostat_recurring_setpoint'", 'null': 'True', 'to': "orm['climatecontrol.RecurringWeeklySetpoint']"}),
            'last_scheduled_setpoint': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'thermostat_scheduled_setpoint'", 'null': 'True', 'to': "orm['climatecontrol.ScheduledHoldSetpoint']"}),
            'mode': ('django.db.models.fields.CharField', [], {'max_length': "'4'"})
        },
        'climatecontrol.thermostattemperaturesensor': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'ThermostatTemperatureSensor', '_ormbases': ['core.Sensor']},
            'sensor_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Sensor']", 'unique': 'True', 'primary_key': 'True'}),
            'thermostat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['climatecontrol.Thermostat']"})
        },
        'core.room': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Room'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'core.sensor': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Sensor'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Room']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['climatecontrol']
