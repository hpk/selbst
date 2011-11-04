# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Thermostat'
        db.create_table('climatecontrol_thermostat', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
        ))
        db.send_create_signal('climatecontrol', ['Thermostat'])

        # Adding model 'ThermostatTemperatureSensor'
        db.create_table('climatecontrol_thermostattemperaturesensor', (
            ('sensor_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.Sensor'], unique=True, primary_key=True)),
            ('thermostat', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['climatecontrol.Thermostat'])),
        ))
        db.send_create_signal('climatecontrol', ['ThermostatTemperatureSensor'])

        # Adding model 'TemperatureSetpoint'
        db.create_table('climatecontrol_temperaturesetpoint', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('thermostat', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['climatecontrol.Thermostat'], null=True, blank=True)),
            ('setpoint', self.gf('django.db.models.fields.FloatField')()),
            ('mode', self.gf('django.db.models.fields.CharField')(default='auto', max_length=4)),
        ))
        db.send_create_signal('climatecontrol', ['TemperatureSetpoint'])

        # Adding model 'RecurringWeeklySetpoint'
        db.create_table('climatecontrol_recurringweeklysetpoint', (
            ('temperaturesetpoint_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['climatecontrol.TemperatureSetpoint'], unique=True, primary_key=True)),
            ('day_of_week', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('hour', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('minute', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('climatecontrol', ['RecurringWeeklySetpoint'])

        # Adding model 'ScheduledHoldSetpoint'
        db.create_table('climatecontrol_scheduledholdsetpoint', (
            ('temperaturesetpoint_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['climatecontrol.TemperatureSetpoint'], unique=True, primary_key=True)),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('climatecontrol', ['ScheduledHoldSetpoint'])


    def backwards(self, orm):
        
        # Deleting model 'Thermostat'
        db.delete_table('climatecontrol_thermostat')

        # Deleting model 'ThermostatTemperatureSensor'
        db.delete_table('climatecontrol_thermostattemperaturesensor')

        # Deleting model 'TemperatureSetpoint'
        db.delete_table('climatecontrol_temperaturesetpoint')

        # Deleting model 'RecurringWeeklySetpoint'
        db.delete_table('climatecontrol_recurringweeklysetpoint')

        # Deleting model 'ScheduledHoldSetpoint'
        db.delete_table('climatecontrol_scheduledholdsetpoint')


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
            'mode': ('django.db.models.fields.CharField', [], {'default': "'auto'", 'max_length': '4'}),
            'setpoint': ('django.db.models.fields.FloatField', [], {}),
            'thermostat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['climatecontrol.Thermostat']", 'null': 'True', 'blank': 'True'})
        },
        'climatecontrol.thermostat': {
            'Meta': {'object_name': 'Thermostat'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'})
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
