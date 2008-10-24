#!/usr/bin/env python
# encoding: utf-8
"""
Page.py

Created by Rui Carmo on 2006-08-19.
Published under the MIT license.
"""

# ============================================================================
# Wiki Page
# ============================================================================

import rfc822

from django.utils.encoding import smart_str, force_unicode
from django.utils.safestring import mark_safe

from docutils.core import publish_parts as rst
from comfy.contrib.markup import textile
from comfy.contrib.markup import pymarkdown

# helper functions for rendering

def _markdown(buffer):
	return mark_safe(force_unicode(pymarkdown.Markdown(buffer)))

def _plaintext(buffer):
	return mark_safe(force_unicode(u'<pre>\n%s</pre>' % buffer))

def _textile(buffer):
	# this one is necessary due to textile's use of kargs
	return mark_safe(force_unicode(textile.textile(buffer, head_offset=0, validate=0, sanitize=1, encoding='utf-8', output='utf-8')))

def _restructuredtext(buffer):
	docutils_settings = getattr(settings, "RESTRUCTUREDTEXT_FILTER_SETTINGS", {})
	return mark_safe(force_unicode(publish_parts(source=buffer, writer_name="html4css1", settings_overrides=docutils_settings)))

def _raw(buffer):
	return mark_safe(force_unicode(buffer))

class Page:
	"""
	Wiki Page - handles storage format and markup
	"""
	
	def __init__(self):
		"""
		Constructor
		"""
		self.headers={}
		self.raw = self.html = ''
	  
	def rfc2822(self):
		"""
		Render this page into an RFC2822 buffer
		"""
		buffer = ''
		for header in self.headers.keys():
			buffer = buffer + header + ": " + self.headers[header] + "\n"
		buffer = buffer + "\n\n" + self.raw
		return buffer
	
	def update(self, markup, text):
		self.raw = text
		self.headers['content-type'] = markup
	
	def render(self, default='text/x-textile'):
		"""
		Render page contents as HTML
		"""
		try:
			format = self.headers['content-type']
		except:
			format = default
		self.html = { u'text/plain': _plaintext,
			u'text/x-markdown': _markdown,
			u'text/x-textile': _textile,
			u'text/x-rst': _restructuredtext,
			u'text/html': _raw }[format](unicode(self.raw))
		return self.html
