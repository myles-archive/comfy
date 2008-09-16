from datetime import datetime, date
from couchdb import schema
from django.db.models import permalink
from django.conf import settings

db = settings.DB

class Post(schema.Document):
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
	
	# Ping
	allow_pings = schema.BooleanField(default=True)
	pings = schema.ListField(schema.DictField(schema.Schema.build(
		uri = schema.TextField(),
		title = schema.TextField(),
		excerpt = schema.TextField(default=False),
		author = schema.TextField(),
		time = schema.DateTimeField(),
	)))
	
	def __unicode__(self):
		return u"%s" % self.title
	
	@permalink
	def get_absolute_url(self):
		return ('blog_detail', None, {
			'year':		self.published.year,
			'month':	self.published.month,
			'day':		self.published.day,
			'slug':		self.slug,
		})
	
	def store(self, db, update_timestamp=True):
		if not self.created:
			self.created = datetime.now()
		if not self.published:
			self.published = date.now()
		if update_timestamp or not self.modified:
			self.modified = datetime.now()
		schema.Document.store(self, db)
	
	@classmethod
	def all_months(cls):
		return [datetime(row.key[0], row.key[1], 1) for row in
			db.view('_view/posts/months', group=True)]
	
	@classmethod
	def by_month(cls, **options):
		return cls.view(db, '_view/posts/by_month', **options)
	
	@classmethod
	def by_slug(cls, **options):
		return cls.view(db, '_view/posts/by_slug', **options)
	
	@classmethod
	def by_tag(cls, **options):
		return cls.view(db, '_view/posts/by_tag', **options)
	
	@classmethod
	def by_time(cls, **options):
		return cls.view(db, '_view/posts/by_time', **options)
	
	@classmethod
	def by_update(cls, **options):
		return cls.view(db, '_view/posts/by_update', **options)
