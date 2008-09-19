import unittest

from comfy.apps.utils.slugify import slugify
from comfy.apps.utils.templatetags import typogrify

class SlugifyTestCase(unittest.TestCase):
	def setUp(self):
		self.title1 = u"Hello, World!"
		# TODO Add some more fo non-latian characters.
	
	def testSlugify(self):
		self.assertEquals(slugify(self.title1), 'hello-world')

class TypogifyTestCase(unittest.TestCase):
	def testApersands(self):
		self.assertEquals(typogrify.amp('One & two'), 'One <span class="amp">&amp;</span> two')
		self.assertEquals(typogrify.amp('One &amp; two'), u'One <span class="amp">&amp;</span> two')
		self.assertEquals(typogrify.amp('One &#38; two'), u'One <span class="amp">&amp;</span> two')
		self.assertEquals(typogrify.amp('One&nbsp;&amp;&nbsp;two'), u'One&nbsp;<span class="amp">&amp;</span>&nbsp;two')
		self.assertEquals(typogrify.amp('One <span class="amp">&amp;</span> two'), u'One <span class="amp">&amp;</span> two')
		self.assertEquals(typogrify.amp('&ldquo;this&rdquo; & <a href="/?that&amp;test">that</a>'), u'&ldquo;this&rdquo; <span class="amp">&amp;</span> <a href="/?that&amp;test">that</a>')
		self.assertEquals(typogrify.amp('<link href="xyz.html" title="One & Two">xyz</link>'), u'<link href="xyz.html" title="One & Two">xyz</link>')
	
	def testCaps(self):
		self.assertEquals(typogrify.caps("A message from KU"), u'A message from <span class="caps">KU</span>')
		self.assertEquals(typogrify.caps("<PRE>CAPS</pre> more CAPS"), u'<PRE>CAPS</pre> more <span class="caps">CAPS</span>')
		self.assertEquals(typogrify.caps("A message from 2KU2 with digits"), u'A message from <span class="caps">2KU2</span> with digits')
		self.assertEquals(typogrify.caps("Dotted caps followed by spaces should never include them in the wrap D.O.T.   like so."), u'Dotted caps followed by spaces should never include them in the wrap <span class="caps">D.O.T.</span>  like so.')
		
	def testQuotes(self):
		self.assertEquals(typogrify.initial_quotes('"With primes"'), u'<span class="dquo">"</span>With primes"')
		self.assertEquals(typogrify.initial_quotes('<a href="#">"With primes and a link"</a>'), u'<a href="#"><span class="dquo">"</span>With primes and a link"</a>')
		self.assertEquals(typogrify.initial_quotes('&#8220;With smartypanted quotes&#8221;'), u'<span class="dquo">&#8220;</span>With smartypanted quotes&#8221;')
	
	def testSmartypants(self):
		self.assertEquals(typogrify.smartypants('The "Green" man'), u'The &#8220;Green&#8221; man')
	
	def tesTitleCase(self):
		self.assertEquals(typogrify.titlecase("this V that"), u'This v That')
		self.assertEquals(typogrify.titlecase("this is just an example.com"), u'This Is Just an example.com')
	
	def testTypogrify(self):
		self.assertEquals(typogrify.typogrify('<h2>"Jayhawks" & KU fans act extremely obnoxiously</h2>'), u'<h2><span class="dquo">&#8220;</span>Jayhawks&#8221; <span class="amp">&amp;</span> <span class="caps">KU</span> fans act extremely&nbsp;obnoxiously</h2>')
		from django.utils.html import conditional_escape
		self.assertEquals(conditional_escape(typogrify.typogrify('<h2>"Jayhawks" & KU fans act extremely obnoxiously</h2>')), u'<h2><span class="dquo">&#8220;</span>Jayhawks&#8221; <span class="amp">&amp;</span> <span class="caps">KU</span> fans act extremely&nbsp;obnoxiously</h2>')
	
	def testWidont(self):
		self.assertEquals(typogrify.widont('A very simple test'), u'A very simple&nbsp;test')
		self.assertEquals(typogrify.widont('Test'), u'Test')
		self.assertEquals(typogrify.widont(' Test'), u' Test')
		self.assertEquals(typogrify.widont('<ul><li>Test</p></li><ul>'), u'<ul><li>Test</p></li><ul>')
		self.assertEquals(typogrify.widont('<ul><li> Test</p></li><ul>'), u'<ul><li> Test</p></li><ul>')
		self.assertEquals(typogrify.widont('<p>In a couple of paragraphs</p><p>paragraph two</p>'), u'<p>In a couple of&nbsp;paragraphs</p><p>paragraph&nbsp;two</p>')
		self.assertEquals(typogrify.widont('<h1><a href="#">In a link inside a heading</i> </a></h1>'), u'<h1><a href="#">In a link inside a&nbsp;heading</i> </a></h1>')
		self.assertEquals(typogrify.widont('<h1><a href="#">In a link</a> followed by other text</h1>'), u'<h1><a href="#">In a link</a> followed by other&nbsp;text</h1>')
		self.assertEquals(typogrify.widont('<h1><a href="#"></a></h1>'), u'<h1><a href="#"></a></h1>')
		self.assertEquals(typogrify.widont('<div>Divs get no love!</div>'), u'<div>Divs get no love!</div>')
		self.assertEquals(typogrify.widont('<pre>Neither do PREs</pre>'), u'<pre>Neither do PREs</pre>')
		self.assertEquals(typogrify.widont('<div><p>But divs with paragraphs do!</p></div>'), u'<div><p>But divs with paragraphs&nbsp;do!</p></div>')
