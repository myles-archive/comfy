from datetime import datetime, date
from couchdb import schema
from django.db.models import permalink
from django.conf import settings

db = settings.COUCHDB

class Video(schema.Document):
	type = schema.TextField(default='Tumblelog')
	tumble_type = schema.TextField(default='Video')
	service = schema.DictField(schema.Schema.build(
		name = schema.TextField(default=None),
		url = schema.TextField(default=None),
		profile_url = schema.TextField(default=None),
	))
	
	title = schema.TextField(default=None)
	body = schema.TextField(default=None)
	video = schema.TextField(default=None)
	
	author = schema.DictField(schema.Schema.build(
		name = schema.TextField(),
		email = schema.TextField(),
	))
	
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
	
	def store(self, db, update_timestamp=True):
		if not self.created:
			self.created = datetime.now()
		if update_timestamp or not self.modified:
			self.modified = datetime.now()
		schema.Document.store(self, db)

class Audio(schema.Document):
	type = schema.TextField(default='Tumblelog')
	tumble_type = schema.TextField(default='Audio')
	service = schema.DictField(schema.Schema.build(
		name = schema.TextField(default=None),
		url = schema.TextField(default=None),
		profile_url = schema.TextField(default=None),
	))
	
	title = schema.TextField(default=None)
	body = schema.TextField(default=None)
	audio_url = schema.TextField(name='url')
	
	author = schema.DictField(schema.Schema.build(
		name = schema.TextField(),
		email = schema.TextField(),
	))
	
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
	
	def store(self, db, update_timestamp=True):
		if not self.created:
			self.created = datetime.now()
		if update_timestamp or not self.modified:
			self.modified = datetime.now()
		schema.Document.store(self, db)

class Chat(schema.Document):
	type = schema.TextField(default='Tumblelog')
	tumble_type = schema.TextField(default='Chat')
	service = schema.DictField(schema.Schema.build(
		name = schema.TextField(default=None),
		url = schema.TextField(default=None),
		profile_url = schema.TextField(default=None),
	))
	
	title = schema.TextField(default=None)
	dialogue = schema.TextField(name='body')
	
	author = schema.DictField(schema.Schema.build(
		name = schema.TextField(),
		email = schema.TextField(),
	))
	
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
	
	def store(self, db, update_timestamp=True):
		if not self.created:
			self.created = datetime.now()
		if update_timestamp or not self.modified:
			self.modified = datetime.now()
		schema.Document.store(self, db)

class Text(schema.Document):
	type = schema.TextField(default='Tumblelog')
	tumble_type = schema.TextField(default='Text')
	service = schema.DictField(schema.Schema.build(
		name = schema.TextField(default=None),
		url = schema.TextField(default=None),
		profile_url = schema.TextField(default=None),
	))
	
	title = schema.TextField(default=None)
	body = schema.TextField()
	
	author = schema.DictField(schema.Schema.build(
		name = schema.TextField(),
		email = schema.TextField(),
	))
	
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
	
	def store(self, db, update_timestamp=True):
		if not self.created:
			self.created = datetime.now()
		if update_timestamp or not self.modified:
			self.modified = datetime.now()
		schema.Document.store(self, db)

class Image(schema.Document):
	type = schema.TextField(default='Tumblelog')
	tumble_type = schema.TextField(default='Image')
	service = schema.DictField(schema.Schema.build(
		name = schema.TextField(default=None),
		url = schema.TextField(default=None),
		profile_url = schema.TextField(default=None),
	))
	
	title = schema.TextField(default=None)
	url = schema.TextField()
	link = schema.TextField(default=None)
	tags = schema.ListField(schema.TextField())
	
	author = schema.DictField(schema.Schema.build(
		name = schema.TextField(),
		email = schema.TextField(),
	))
	
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
	
	def store(self, db, update_timestamp=True):
		if not self.created:
			self.created = datetime.now()
		if update_timestamp or not self.modified:
			self.modified = datetime.now()
		schema.Document.store(self, db)

class Quote(schema.Document):
	type = schema.TextField(default='Tumblelog')
	tumble_type = schema.TextField(default='Quote')
	service = schema.DictField(schema.Schema.build(
		name = schema.TextField(default=None),
		url = schema.TextField(default=None),
		profile_url = schema.TextField(default=None),
	))
	
	quote = schema.TextField(name='body')
	source = schema.TextField(default=None)
	tags = schema.ListField(schema.TextField())
	
	author = schema.DictField(schema.Schema.build(
		name = schema.TextField(),
		email = schema.TextField(),
	))
	
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
	
	def store(self, db, update_timestamp=True):
		if not self.created:
			self.created = datetime.now()
		if update_timestamp or not self.modified:
			self.modified = datetime.now()
		schema.Document.store(self, db)
	

class Link(schema.Document):
	type = schema.TextField(default='Tumblelog')
	tumble_type = schema.TextField(default='Link')
	service = schema.DictField(schema.Schema.build(
		name = schema.TextField(default=None),
		url = schema.TextField(default=None),
		profile_url = schema.TextField(default=None),
	))
	
	title = schema.TextField()
	body = schema.TextField(default=None)
	tags = schema.ListField(schema.TextField())
	
	author = schema.DictField(schema.Schema.build(
		name = schema.TextField(),
		email = schema.TextField(),
	))
	
	uri = schema.TextField()
	via_uri = schema.TextField(default=None)
	via_title = schema.TextField(default=None)
	
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
	
	def store(self, db, update_timestamp=True):
		if not self.created:
			self.created = datetime.now()
		if update_timestamp or not self.modified:
			self.modified = datetime.now()
		schema.Document.store(self, db)
