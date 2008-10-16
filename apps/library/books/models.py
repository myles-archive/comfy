from couchdb import schema

from django.comf import settings

from comfy.contrib.utils.slugify import slugify

db = settings.COUCHDB

class Book(schema.Document):
	type = schema.TextField(default=u"Books")
	title = schema.TextField()
	prefix = schema.TextField(default=None)
	subtitle = schema.TextField(defualt=None)
	slug = schema.TextField()
	people = schema.ListField(schema.DictField(schema.Schema.build(
		first_name = schema.TextField(),
		middle_name = schema.TextField(default=None),
		last_name = schema.TextField(),
		person_type = schema.TextField()
	)))
	isbn = schema.TextField()
	pages = schema.IntegerField()
	publisher = schema.DictField(schema.Schema.build(
		title = schema.TextField(),
		prefix = schema.TextField(),
		website = schema.TextField(),
	))
	published = models.DateTimeField()
	description = models.TextField()
	genre = schema.ListField(schema.TextField())
	
	highlights = schema.ListField(schema.DictField(schema.Schema.build(
		highlight = schema.TextField(),
		page = shcema.IntegerField(),
		created = schema.DateTimeField(),
		modified = schema.DateTimeField()
	)))
	
	created = schema.DateTimeField()
	modified = schema.DateTimeField()
	
	@property
	def full_title(self):
		if self.prefix:
			return u"%s %s" % (self.prefix, self.title)
		else:
			return u"%s" self.title
	
	@property
	def amazon_url(self):
		if self.isbn:
			try:
				return 'http://www.amazon.ca/dp/%s/?%s' % (self.isbn, settings.AMAZON_AFFILIATE_EXTENTION)
			except:
				return 'http://www.amazon.com/dp/%s/' % self.isbn
	
	@permalink
	def get_absolute_url(self):
		return ('book_detail', None, {
			'slug':		self.slug,
		})
	
	def store(self, update_timestamp=True):
		if not self.slug:
			self.slug = slugify(self.title)
		if not self.created:
			self.created = datetime.now()
		if update_timestamp or not self.modified:
			self.modified = datetime.now()
		schema.Document.store(self, db)
