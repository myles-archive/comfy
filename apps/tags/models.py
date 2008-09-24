from couchdb import schema

class Tag(schema.Document):
	tags = schema.ListField(schema.TextField())
	
	def store(self, db):
		schema.Document.store(self, db)
	
	@classmethod
	def by_tag(cls, **options):
		return cls.view(db, '_view/tags/by_tag', **options)
