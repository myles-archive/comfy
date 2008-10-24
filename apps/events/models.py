from datetime import datetime, date, time
from couchdb import schema

from django.db.models import permalink
from django.conf import settings

from comfy.contrib.utils.slugify import slugify
from comfy.contrib.utils.schema import URLField, SlugField
from comfy.apps.events.signals import event_stored

db = settings.COUCHDB

class Event(schema.Document):
	type = schema.TextField(default='Event')
	title = schema.TextField()
	slug = SlugField()
	
	start_date = schema.DateField(default=date.today())
	start_time = schema.TimeField()
	end_date = schema.DateField()
	end_time = schema.TimeField()
	
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
	
	@permalink
	def get_absolute_url(self):
		return ('event_detail', None, {
			'event_id':	self.id,
		})
	
	@property
	def start_datetime(self):
		if self.start_time and self.start_date:
			return datetime.combine(self.start_date, self.start_time)
		else:
			return datetime.combine(self.start_date, time(0, 0))
	
	@property
	def end_datetime(self):
		if self.end_time and self.end_date:
			return datetime.combine(self.end_date, self.end_time)
		elif self.end_date:
			return datetime.combine(self.end_date, time(0, 0))
		else:
			return None
	
	@classmethod
	def all_years(self):
		return [datetime(row.key[0], 1, 1) for row in
			db.view('_view/events/years', group=True)]
	
	@classmethod
	def all_months(cls):
		return [datetime(row.key[0], row.key[1], 1) for row in
			db.view('_view/events/months', group=True)]
	
	@classmethod
	def all_days(self):
		return [datetime(row.key[0], row.key[1], 1) for row in
			db.view('_view/events/days', group=True)]
	
	@classmethod
	def by_year(cls, **options):
		return cls.view(db, '_view/events/by_year', **options)
	
	@classmethod
	def by_month(cls, **options):
		return cls.view(db, '_view/events/by_month', **options)
	
	@classmethod
	def by_day(cls, **options):
		return cls.view(db, '_view/events/by_day', **options)
	
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
		event_stored.send(sender=self)
