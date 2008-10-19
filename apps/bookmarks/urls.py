from django.conf.urls.defaults import *

urlpatterns = patterns('comfy.apps.bookmarks.views',
	url(r'^page/(?P<page>\d)/$',
		view	= 'index',
		name	= 'bookmarks_archive_pagination',
	),
	url(r'^$',
		view	= 'index',
		name	= 'bookmarks_index'
	),
)