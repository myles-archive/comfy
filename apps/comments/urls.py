from django.conf.urls.defaults import *

urlpatterns = patterns('comfy.apps.comments.views',
	url(r'^post/$',
		view	= 'post',
		name	= 'post_comment',
	)
)