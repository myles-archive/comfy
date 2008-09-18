import unittest

from comfy.apps.utils.slugify import slugify

class SlugifyTestCase(unittest.TestCase):
	def setUp(self):
		self.title1 = u"Hello, World!"
		# TODO Add some more fo non-latian characters.
	
	def testSlugify(self):
		self.assertEquals(slugify(self.title1), 'hello-world')
