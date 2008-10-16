from couchdb import schema

from django.db.models import permalink
from django.conf import settings

from comfy.contrib.utils.slugify import slugify

db = settings.COUCHDB

class Presentation(schema.Document):
	type = schema.TextField(default='Presentation')
	title = schema.TextField()
	slug = schema.TextField()
	author = schema.DictField(schema.Schema.build(
		name = schema.TextField(),
		email = schema.TextField(),
	))
	body = schema.TextField(default=None)
	tags = schema.ListField(schema.TextField())
	
	published = schema.DateField()
	created = schema.DateTimeField()
	modified = schema.DateTimeField()
	
	slides = schema.ListField(schema.DictField(schema.Schema.build(
		title = schema.TextField(default=None),
		body = schema.TextField(),
		notes = schema.TextField(),
	)))
	
	external_resources = schema.ListField(schema.DictField(schema.Schema.build(
		title = schema.TextField(default=None),
		url = schema.TextField(),
	)))
	
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
	
	@permalink
	def get_absolute_url(self):
		return ('presentation_detail', None, {
			'slug':		self.slug,
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
