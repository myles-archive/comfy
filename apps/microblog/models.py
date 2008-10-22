from couchdb import schema

from django.db.models import permalink
from django.conf import settings

from comfy.apps.microblog import signals

from comfy.core.couchdb import Database

db = Database 

class Micro(schema.Document):
	type = schema.TextField(default='MicroBlog')
	body = schema.TextField()
	tags = schema.ListField(schema.TextField())
	
	author = schema.DictField(schema.Schema.build(
		name = schema.TextField(),
		email = schema.TextField(),
	))
	
	published = schema.DateField()
	created = schema.DateTimeField()
	modified = schema.DateTimeField()
	
	@permalink
	def get_absolute_url(self):
		return ('micro_detail', None, {
			'id':	self._id,
		})
	
	def store(self, update_timestamp=True):
		if not self.created:
			self.created = datetime.now()
		if not self.published:
			self.published = date.today()
		if update_timestamp or not self.modified:
			self.modified = datetime.now()
		schema.Document.store(self, db)
		micro_stored.send(sender=self)
