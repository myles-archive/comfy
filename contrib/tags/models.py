from couchdb import schema

from django.conf import settings

db = settings.COUCHDB

class Tag(schema.Document):
	tags = schema.ListField(schema.TextField())
	
	def store(self):
		schema.Document.store(self, db)
	
	@classmethod
	def all_tags(cls):
		return [{'key': row.key, 'value': row.value} for row in
			db.view('_view/tags/tags', group=True)]
	
	@classmethod
	def by_tag(cls, **options):
		return cls.view(db, '_view/tags/by_tag', **options)
