from django.contrib.syndication.feeds import Feed, FeedDoesNotExist
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.conf import settings

from comfy.apps.blog.models import Post

class PostComments(Feed):
	def get_object(self, bits):
		if len(bits) != 1:
			raise ObjectDoesNotExist
		return Post.load(settings.COUCHDB, bits[0])
	
	def title(self, obj):
		return u"%s Comments" % obj.title
	
	def description(self, obj):
		return u"%s Blog Post %s Comments" % (Site.objects.get_current().name, obj.title)
	
	def link(self, obj):
		if not obj:
			raise FeedDoesNotExist
		return obj.get_absolute_url()
	
	def author_name(self, obj):
		return obj.author.name
	
	def author_email(self, obj):
		return obj.author.email
	
	def items(self, obj):
		return obj.comments
	
	def item_link(self, item):
		return self.link
	
	def item_author_name(self, item):
		return item.author.name
	
	def item_author_link(self, item):
		return item.author.url
