import unittest
from datetime import datetime
from django.conf import settings
from couchdb import Server

from comfy.apps.blog.models import Post

class PostTestCase(unittest.TestCase):
	def setUp(self):
		self.server = Server(settings.COUCHDB_SERVER)
		try:
			self.db = self.server.create('comfy_blog_test')
		except:
			self.db = self.server['comfy_blog_test']
		
		self.post1 = Post(title=u"Hello, World!", slug=u"foo-bar", published=datetime(2008, 8, 8), author={'name': 'Myles Braithwaite', 'email': 'me@mylesbraithwaite.com'})
		self.post2 = Post(title=u"Hello, World!", published=datetime(2007, 7, 7))
		self.post1.store(self.db)
		self.post2.store(self.db)
	
	def testURL(self):
		self.assertEquals(self.post1.get_absolute_url(), '/blog/2008/8/8/foo-bar/')
		self.assertEquals(self.post2.get_absolute_url(), '/blog/2007/7/7/hello-world/')
	
	def testSlugify(self):
		self.assertEquals(self.post2.slug, 'hello-world')
	
	def testAddComment(self):
		post = Post.load(self.db, self.post1.id)
		post.comments.author = {'name': u"Myles Braithwaite", 'email': "me@mylesbraithwaite.com", 'url': u"http://mylesbraithwaite.com/"}
		post.comments.comment = u"Hello, World!"
		post.comments.time = datetime.now()
		post.comments.user_agent = u"Python Unit Test"
		post.comments.ip_address = u"127.0.0.1"
		post.comments.is_spam = False
		post.store(self.db)
		# TODO Still working on doing something here to see if the test actually worked.
	
	def tearDown(self):
		del self.server['comfy_blog_test']
