from django.conf.urls.defaults import *

urlpatterns = patterns('comfy.contrib.tags.views',
	url(r'^(?P<tag>[-\w]+)/$',
		view	= 'detail',
		name	= 'tag_detail',
	),
	url(r'^$',
		view	= 'index',
		name	= 'tags_index'
	),
)