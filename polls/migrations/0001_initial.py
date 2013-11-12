# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Map'
        db.create_table(u'polls_map', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal(u'polls', ['Map'])

        # Adding model 'Region'
        db.create_table(u'polls_region', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal(u'polls', ['Region'])

        # Adding model 'Place'
        db.create_table(u'polls_place', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('owner', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique_with=(), max_length=50, populate_from=None)),
            ('color', self.gf('django.db.models.fields.IntegerField')()),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['polls.Region'])),
            ('created_at', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
            ('map_geo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['polls.Map'], null=True, blank=True)),
            ('geocoded', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'polls', ['Place'])

        # Adding model 'Profile'
        db.create_table(u'polls_profile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gender', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('phone', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'polls', ['Profile'])

        # Adding model 'Poll'
        db.create_table(u'polls_poll', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['polls.Place'])),
            ('service', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('menu', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('bill', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('check', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('feedback_book', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['polls.Profile'])),
        ))
        db.send_create_signal(u'polls', ['Poll'])


    def backwards(self, orm):
        # Deleting model 'Map'
        db.delete_table(u'polls_map')

        # Deleting model 'Region'
        db.delete_table(u'polls_region')

        # Deleting model 'Place'
        db.delete_table(u'polls_place')

        # Deleting model 'Profile'
        db.delete_table(u'polls_profile')

        # Deleting model 'Poll'
        db.delete_table(u'polls_poll')


    models = {
        u'polls.map': {
            'Meta': {'object_name': 'Map'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'polls.place': {
            'Meta': {'object_name': 'Place'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'color': ('django.db.models.fields.IntegerField', [], {}),
            'created_at': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'geocoded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'geometry': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'map_geo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['polls.Map']", 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['polls.Region']"}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': 'None'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'polls.poll': {
            'Meta': {'object_name': 'Poll'},
            'bill': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'check': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'feedback_book': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'menu': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['polls.Place']"}),
            'service': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['polls.Profile']"})
        },
        u'polls.profile': {
            'Meta': {'object_name': 'Profile'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'gender': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'phone': ('django.db.models.fields.IntegerField', [], {})
        },
        u'polls.region': {
            'Meta': {'object_name': 'Region'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['polls']