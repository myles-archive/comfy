from couchdb import schema

class Tag(schema.Document):
	tags = schema.ListField(schema.TextField())
	
	def store(self, db, update_timestamp=True):
		schema.Document.store(self, db)
