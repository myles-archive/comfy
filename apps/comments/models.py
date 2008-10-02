from datetime import datetime
from couchdb import schema

from django.db.models import permalink
from django.conf import settings

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
		return ('comment_redirect', None, {
			'document_id':	self.id,
		})
	
	def store(self):
		schema.Document.store(self, db)
