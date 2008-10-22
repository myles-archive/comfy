from datetime import datetime
from couchdb import schema

from django.db.models import permalink
from django.conf import settings

from comfy.contrib.comments.signals import comment_stored

db = settings.COUCHDB

class Comment(schema.Document):
	"""
	This is the generic comment model.
	It shouldn't be used allown.
	"""
	allow_comments = schema.BooleanField(default=True)
	comments = schema.ListField(schema.DictField(schema.Schema.build(
		author = schema.DictField(schema.Schema.build(
			name = schema.TextField(),
			email = schema.TextField(),
			url = schema.TextField(),
		)),
		comment = schema.TextField(),
		time = schema.DateTimeField(),
		user_agent = schema.TextField(),
		ip_address = schema.TextField(),
		is_spam = schema.BooleanField(default=False),
	)))
	
	@permalink
	def get_absolute_url(self):
		return ('redirect', None, {
			'document_id':	self.id,
		})
	
	def store(self):
		schema.Document.store(self, db)
		comment_stored.send(sender=self)

class Ping(schema.Document):
	allow_pings = schema.BooleanField(default=True)
	pings = schema.ListField(schema.DictField(schema.Schema.build(
		uri = schema.TextField(),
		title = schema.TextField(),
		excerpt = schema.TextField(default=False),
		author = schema.TextField(),
		time = schema.DateTimeField(),
	)))
	
	@permalink
	def get_absolute_url(self):
		return ('redirect', None, {
			'document_id':	self.id,
		})
	
	def store(self):
		schema.Document.store(self, db)
		ping_stored.send(sender=self)
