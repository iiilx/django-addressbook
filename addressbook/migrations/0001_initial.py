# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ContactGroup'
        db.create_table('addressbook_contactgroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length='40')),
        ))
        db.send_create_signal('addressbook', ['ContactGroup'])

        # Adding unique constraint on 'ContactGroup', fields ['user', 'name']
        db.create_unique('addressbook_contactgroup', ['user_id', 'name'])

        # Adding model 'Contact'
        db.create_table('addressbook_contact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['addressbook.ContactGroup'])),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length='40')),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length='40')),
            ('middle_name', self.gf('django.db.models.fields.CharField')(max_length='40', blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length='40', blank=True)),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length='50', blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('addressbook', ['Contact'])

        # Adding model 'Address'
        db.create_table('addressbook_address', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['addressbook.Contact'])),
            ('street', self.gf('django.db.models.fields.CharField')(max_length='50')),
            ('city', self.gf('django.db.models.fields.CharField')(max_length='40')),
            ('state', self.gf('django.contrib.localflavor.us.models.USStateField')(max_length=2)),
            ('zip', self.gf('django.db.models.fields.CharField')(max_length='10')),
            ('type', self.gf('django.db.models.fields.CharField')(max_length='5')),
        ))
        db.send_create_signal('addressbook', ['Address'])

        # Adding model 'PhoneNumber'
        db.create_table('addressbook_phonenumber', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['addressbook.Contact'])),
            ('phone', self.gf('django.contrib.localflavor.us.models.PhoneNumberField')(max_length=20)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length='4')),
        ))
        db.send_create_signal('addressbook', ['PhoneNumber'])

        # Adding model 'Email'
        db.create_table('addressbook_email', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['addressbook.Contact'])),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length='8')),
        ))
        db.send_create_signal('addressbook', ['Email'])


    def backwards(self, orm):
        # Removing unique constraint on 'ContactGroup', fields ['user', 'name']
        db.delete_unique('addressbook_contactgroup', ['user_id', 'name'])

        # Deleting model 'ContactGroup'
        db.delete_table('addressbook_contactgroup')

        # Deleting model 'Contact'
        db.delete_table('addressbook_contact')

        # Deleting model 'Address'
        db.delete_table('addressbook_address')

        # Deleting model 'PhoneNumber'
        db.delete_table('addressbook_phonenumber')

        # Deleting model 'Email'
        db.delete_table('addressbook_email')


    models = {
        'addressbook.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': "'40'"}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['addressbook.Contact']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.contrib.localflavor.us.models.USStateField', [], {'max_length': '2'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': "'50'"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': "'5'"}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': "'10'"})
        },
        'addressbook.contact': {
            'Meta': {'object_name': 'Contact'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': "'40'"}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['addressbook.ContactGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': "'40'"}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': "'40'", 'blank': 'True'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': "'50'", 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': "'40'", 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'addressbook.contactgroup': {
            'Meta': {'unique_together': "(('user', 'name'),)", 'object_name': 'ContactGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': "'40'"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'addressbook.email': {
            'Meta': {'object_name': 'Email'},
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['addressbook.Contact']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': "'8'"})
        },
        'addressbook.phonenumber': {
            'Meta': {'object_name': 'PhoneNumber'},
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['addressbook.Contact']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'max_length': '20'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': "'4'"})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['addressbook']