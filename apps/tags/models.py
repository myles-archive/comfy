from couchdb import schema

from django.comf import settings

db = settings.COUCHDB

class Tag(schema.Document):
	tags = schema.ListField(schema.TextField())
	
	def store(self):
		schema.Document.store(self, db)
	
	@classmethod
	def by_tag(cls, **options):
		return cls.view(db, '_view/tags/by_tag', **options)
