from datetime import datetime
from django.conf import settings
from couchdb import Server

from comfy.apps.talks.models import Presentation

class PresentationTestCase(unittest.TestCase):
	def setUp(self):
		self.server = Server(settings.COUCHDB_SERVER)
		try:
			self.db = self.server.create('comfy_blog_test')
		except:
			self.db = self.server['comfy_blog_test']
		
		self.presentation = Presentation(title=u"Hello, World!", slug=u"hello-world", published=datetime(2008, 8, 8), author={'name': 'Myles Braithwaite', 'email': 'myles.braithwaite@example.com'})
		self.presentation.store(self.db)
	
	def testAddSlides(self):
		self.presentation.slides = [{
			'title': u"First Slide",
			'body': u"Hello, World!",
			'notes': u"<p>Hello, World!",
		}]
		self.presentation.store(self.db)
	
	def tearDown(self):
		del self.server['comfy_blog_test']
