from datetime import datetime, date
from couchdb import schema
from django.db.models import permalink
from django.conf import settings

db = settings.COUCHDB

class FlatPage(schema.Document):
	type = schema.TextField(default='FlatPage')
	url = schema.TextField()
	title = schema.TextField()
	content = schema.TextField()
	template_name = schema.TextField()
	registration_required = schema.BooleanField(default=False)
	
	created = schema.DateTimeField()
	modified = schema.DateTimeField()
	
	# Comments
	allow_comments = schema.BooleanField(default=True)
	comments = schema.ListField(schema.DictField(schema.Schema.build(
		author = schema.DictField(schema.Schema.build(
			name = schema.TextField(),
			email = schema.TextField(),
			url = schema.TextField(),
		)),
		comment = schema.TextField(),
		time = schema.DateTimeField(),
	)))
	
	def store(self, update_timestamp=True):
		if not self.created:
			self.created = datetime.now()
		if update_timestamp or not self.modified:
			self.modified = datetime.now()
		schema.Document.store(self, db)
	
	def get_absolute_url(self):
		return self.url
	
	@classmethod
	def by_url(cls, **options):
		return cls.view(db, '_view/flatpages/by_url', **options)
