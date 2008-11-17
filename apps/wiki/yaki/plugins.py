#!/usr/bin/env python
# encoding: utf-8
"""
Plugins.py

Plugin registration and invocation

Created by Rui Carmo on 2006-11-12.
Published under the MIT license.
"""

import os, re
from django.conf import settings
from comfy.apps.wiki.settings import YAKI_PLUGINS_DIR
from comfy.apps.wiki.yaki.utils import *

class PluginRegistry:
	plugins = {'markup': {}}
	serial = 0
	
	def __init__(self):
		print "Loading Wiki plugins..."
		# Get plugin directory
		plugindir = os.path.join(settings.PROJECT_ROOT, YAKI_PLUGINS_DIR)
		for f in locate('*.py', plugindir):
			relpath = f.replace(settings.PROJECT_ROOT + '/', '')
			(modname, ext) = rsplit(relpath, '.', 1)
			modname = '.'.join(modname.split('/'))
			try:
				_module = __import__(modname, globals(), locals(), [''])
				# Load each python file
				for x in dir(_module):
					if 'WikiPlugin' in x:
						_class = getattr(_module, x)
						_class() # plugins will register themselves
			except ImportError:
				pass
	  
	def register(self, category, instance, tag, name):
		print "Plugin %s registered in category %s for tag %s" % (name,category,tag)
		if tag not in self.plugins[category].keys():
			self.plugins[category][tag] = {}
		self.plugins[category][tag][name.lower()] = instance
	
	def runForAllTags(self, pagename, soup, request=None, response=None):
		"""Runs all markup plugins that process specific tags (except the plugin one)"""
		for tagname in self.plugins['markup'].keys():
			if tagname != 'plugin':
				for i in self.plugins['markup'][tagname]:
					plugin = self.plugins['markup'][tagname][i]
					# Go through all tags in document
					for tag in soup(tagname):
						result = plugin.run(self.serial, tag, tagname, pagename, soup, request, response)
						self.serial = self.serial + 1
						if result == True:
							continue
	
	def run(self, tag, tagname, pagename=None, soup=None, request=None, response=None):
		if tagname == 'plugin':
			try:
				name = tag['name'].lower() # get the attribute
			except KeyError:
				return
			if name in self.plugins['markup']['plugin']:
				plugin = self.plugins['markup']['plugin'][name]
				result = plugin.run(self.serial, tag, tagname, pagename, soup, request, response)
				self.serial = self.serial + 1
				# ignore the result for plugin tags
		elif tagname in self.plugins['markup']:
			for i in self.plugins['markup'][tagname]:
				plugin = self.plugins['markup'][tagname][i]
				result = plugin.run(self.serial, tag, tagname, pagename, soup, request, response)
				self.serial = self.serial + 1
				# if plugin returns False, then the tag does not need to be processed any further
				if result == False:
					return

class WikiPlugin:
	"""Base class for all Wiki plugins"""
	def __init__(self, registry, webapp):
		# Register this (override in child classes)
		registry.register('markup', self, 'plugin', 'base')  
	def run(self, serial, tag, tagname, pagename, soup, request=None, response=None):
		pass
