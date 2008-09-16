from django.conf.urls.defaults import *

urlpatterns = patterns('comfy.apps.blog.views',
	url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
		view	= 'detail',
		name	= 'blog_detail',
	),
	# url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
	# 	view	= 'day',
	# 	name	= 'blog_day'
	# ),
	# url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$',
	# 	view	= 'month',
	# 	name	= 'blog_month'
	# ),
	# url(r'^(?P<year>\d{4})/$',
	# 	view	= 'year',
	# 	name	= 'blog_year'
	# ),
	url(r'^$',
		view	= 'index',
		name	= 'blog_index'
	),
)