from datetime import datetime, date
from couchdb import schema

from django.db.models import permalink
from django.conf import settings
from django.core.urlresolvers import reverse

from comfy.apps.utils.slugify import slugify

db = settings.COUCHDB

class Post(schema.Document):
	"""
	Blog post model.
	"""
	type = schema.TextField(default='Post')
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
	
	# License
	# license = schema.DictField(schema.Schema.build(
	# 	name = schema.TextField(),
	# 	organization = schema.TextField(defualt=None),
	# 	abbreviation = schema.TextField(default=None),
	# 	url = schema.TextField(default=None),
	# 	logo = schema.TextField(default=None),
	# 	description = schema.TextField(default=None)
	# ))
	
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
		return ('post_detail', None, {
			'year':		self.published.year,
			'month':	self.published.month,
			'day':		self.published.day,
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
	
	@classmethod
	def all_months(cls):
		return [datetime(row.key[0], row.key[1], 1) for row in
			db.view('_view/blog/months', group=True)]
	
	@classmethod
	def by_month(cls, **options):
		return cls.view(db, '_view/blog/by_month', **options)
	
	@classmethod
	def by_slug(cls, **options):
		return cls.view(db, '_view/blog/by_slug', **options)
	
	@classmethod
	def by_tag(cls, **options):
		return cls.view(db, '_view/blog/by_tag', **options)
	
	@classmethod
	def by_time(cls, **options):
		return cls.view(db, '_view/blog/by_time', **options)
	
	@classmethod
	def by_update(cls, **options):
		return cls.view(db, '_view/blog/by_update', **options)
