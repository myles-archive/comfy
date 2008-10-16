from django.conf.urls.defaults import *

urlpatterns = patterns('comfy.apps.tumblelog.views',
	# url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
	# 	view	= 'detail',
	# 	name	= 'post_detail',
	# ),
	# url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
	# 	view	= 'archive_day',
	# 	name	= 'post_archive_day'
	# ),
	# url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$',
	# 	view	= 'archive_month',
	# 	name	= 'post_archive_month'
	# ),
	# url(r'^(?P<year>\d{4})/$',
	# 	view	= 'archive_year',
	# 	name	= 'post_archive_year'
	# ),
	url(r'^page/(?P<page>\d)/$',
		view	= 'index',
		name	= 'tumblelog_archive_pagination',
	),
	url(r'^$',
		view	= 'index',
		name	= 'tumblelog_index'
	),
)