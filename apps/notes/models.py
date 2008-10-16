from datetime import datetime, date
from couchdb import schema
from django.db.models import permalink
from django.conf import settings

db = settings.COUCHDB

class Note(schema.Document):
	type = schema.TextField(default='Note')
	body = schema.TextField()
	created = schema.DateTimeField()
	updated = schema.DateTimeField()
	published = schema.DateField()
	tags = schema.ListField(schema.TextField())
	private = schema.BooleanField(default=False)
	
	author = schema.DictField(schema.Schema.build(
		name = schema.TextField(),
		email = schema.TextField(),
	))
	
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
		return ('note_detail', None, {
			'note_id':		self.id,
		})
	
	@permalink
	def get_edit_url(self):
		return ('note_update', None, {
			'note_id':		self.id,
		})
	
	@permalink
	def get_delete_url(self):
		return ('note_delete', None, {
			'note_id':		self.id,
		})
	
	def store(self, update_timestamp=True):
		if not self.created:
			self.created = datetime.now()
		if not self.published:
			self.published = date.now()
		if update_timestamp or not self.modified:
			self.modified = datetime.now()
		schema.Document.store(self, db)
	
	@classmethod
	def by_time(cls, **options):
		return cls.view(db, '_view/notes/by_time', **options)
	
	@classmethod
	def by_tag(cls, **options):
		return cls.view(db, '_view/notes/by_tag', **options)
