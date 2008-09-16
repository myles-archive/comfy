from django.conf.urls.defaults import *

urlpatterns = patterns('comfy.apps.blog.views',
	url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
		view	= 'detail',
		name	= 'blog_detail',
	),
	url(r'^$',
		view	= 'index',
		name	= 'blog_index'
	),
)