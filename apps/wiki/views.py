import urllib
import os

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.http import Http404
from django.utils.encoding import smart_str, force_unicode
from django.utils.safestring import mark_safe

from comfy.apps.wiki.yaki.store import Store
from comfy.contrib.BeautifulSoup import BeautifulSoup
from comfy.apps.wiki.yaki.plugins import PluginRegistry
from comfy.apps.wiki.settings import YAKI_EMPTY_PAGE, YAKI_HOME_PAGE

store = Store(settings.YAKI_STORE_DIR)


def page(request, path=YAKI_HOME_PAGE):
	try:
		page = store.getRevision(urllib.unquote(path))
	except IOError:
		page = store.getRevision(YAKI_EMPTY_PAGE)
	
	plugins = PluginRegistry()
	soup = BeautifulSoup(page.render(), selfClosingTags=['plugin'], convertEntities=['html','xml'])
	for tag in soup('plugin'):
		plugins.run(tag, 'plugin', page.headers['name'], soup)
	plugins.runForAllTags(page.headers['name'], soup)
	
	context = {
		'path':		path,
		'render':	mark_safe(force_unicode(soup.renderContents())),
		'headers':	page.headers,
	}
	
	return render_to_response('wiki/page.html', context, context_instance=RequestContext(request))
