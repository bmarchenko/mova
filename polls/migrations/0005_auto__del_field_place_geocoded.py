# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Place.geocoded'
        db.delete_column(u'polls_place', 'geocoded')


    def backwards(self, orm):
        # Adding field 'Place.geocoded'
        db.add_column(u'polls_place', 'geocoded',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    models = {
        u'polls.map': {
            'Meta': {'object_name': 'Map'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'polls.place': {
            'Meta': {'object_name': 'Place'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'color': ('django.db.models.fields.IntegerField', [], {}),
            'geometry': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'map_geo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['polls.Map']", 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['polls.Region']"}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "'title'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'polls.poll': {
            'Meta': {'object_name': 'Poll'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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