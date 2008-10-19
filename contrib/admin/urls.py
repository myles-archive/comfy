from django.conf.urls.defaults import *

from django.contrib import admin as django_admin
django_admin.autodiscover()

urlpatterns = patterns('',
	(r'^django/doc/', include('django.contrib.admindocs.urls')),
	(r'^django/(.*)', django_admin.site.root),
)

urlpatterns += patterns('comfy.contrib.admin.views',
	url(r'^$',
		view	= 'index',
		name	= 'admin_index'
	),
)

urlpatterns += patterns('comfy.contrib.admin.views.blog',
	url(r'^blog/$',
		view	= 'index',
		name	= 'comfy_admin_blog'
	),
	url(r'^blog/posts/add/$',
		view	= 'post_add_edit',
		name	= 'comfy_admin_blog_post_add'
	),
	url(r'^blog/posts/(?P<id>[-\w]+)/$',
		view	= 'post_add_edit',
		name	= 'comfy_admin_blog_post_edit'
	),
)