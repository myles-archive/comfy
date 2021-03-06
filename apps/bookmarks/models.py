from datetime import datetime, date
from couchdb import schema

from django.db.models import permalink
from django.conf import settings

from comfy.contrib.utils.slugify import slugify
from comfy.contrib.utils.schema import URLField, SlugField
from comfy.apps.bookmarks.signals import bookmark_stored

db = settings.COUCHDB

class Bookmark(schema.Document):
	type = schema.TextField(default='Bookmark')
	title = schema.TextField()
	slug = SlugField()
	url = URLField()
	via = schema.DictField(schema.Schema.build(
		title = schema.TextField(),
		url = URLField(),
	))
	author = schema.DictField(schema.Schema.build(
		name = schema.TextField(),
		email = schema.TextField(),
	))
	body = schema.TextField(default=None)
	tags = schema.ListField(schema.TextField())
	
	published = schema.DateField()
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
		user_agent = schema.TextField(),
		ip_address = schema.TextField(),
		is_spam = schema.BooleanField(default=False),
	)))
	
	# Ping
	allow_pings = schema.BooleanField(default=True)
	pings = schema.ListField(schema.DictField(schema.Schema.build(
		uri = schema.TextField(),
		title = schema.TextField(),
		excerpt = schema.TextField(default=False),
		author = schema.TextField(),
		time = schema.DateTimeField(),
	)))
	
	def get_absolute_url(self):
		return self.url
	
	@permalink
	def get_internal_url(self):
		return ('bookmark_detail', None, {
			'bookmark_id':	self.id,
		})
	
	def store(self, update_timestamp=True):
		if not self.slug:
			self.slug = slugify(self.title)
		if not self.created:
			self.created = datetime.now()
		if not self.published:
			self.published = date.today()
		if update_timestamp or not self.modified:
			self.modified = datetime.now()
		schema.Document.store(self, db)
		bookmark_stored.send(sender=self)
	
	@classmethod
	def by_time(cls, **options):
		return cls.view(db, '_view/bookmarks/by_time', **options)
