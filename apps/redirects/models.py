from couchdb import schema

from django.db.models import permalink

class Document(schema.Document):
	type = schema.TextField()
	
	@permalink
	def get_absolute_url(self):
		return ('redirect', None, {
			'document_id':	self._id,
		})
