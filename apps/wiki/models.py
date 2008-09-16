from datetime import datetime, date
from couchdb import schema
from django.db.models import permalink
from django.conf import settings

db = settings.DB

class Document(schema.Document):
	type = schema.TextField(default='Wiki')
	title = schema.TextField()
	author = schema.DictField(schema.Schema.build(
		name = schema.TextField(),
		email = schema.TextField(),
	))
	body = schema.TextField()
	tags = schema.ListField(schema.TextField())
	
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
	
	def __unicode__(self):
		return u"%s" % self.title
	
	@permalink
	def get_absolute_url(self):
		return ('wiki_detail', None, {
			'title':	self.title,
		})
	
	def store(self, db, update_timestamp=True):
		if not self.created:
			self.created = datetime.now()
		if update_timestamp or not self.modified:
			self.modified = datetime.now()
		schema.Document.store(self, db)
