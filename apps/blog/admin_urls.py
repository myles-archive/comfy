from django.conf.urls.defaults import *

urlpatterns = patterns('comfy.apps.blog.admin_views',
	(r'^posts/add/$', 'post_add_edit'),
	(r'^posts/(?P<id>[-\w]+)/$', 'post_add_edit'),
)