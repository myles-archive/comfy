from django.conf.urls.defaults import *

urlpatterns = patterns('comfy.apps.wiki.views',
	url(r'(?P<path>[\w./-]*)/$',
		view	= 'page',
		name	= 'wiki_page',
	),
	url(r'^$',
		view	= 'page',
		name	= 'wiki_index'
	),
)