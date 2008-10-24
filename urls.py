from re import escape
from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('',
	url(r'^$',
		view	= 'comfy.apps.tumblelog.views.homepage',
		name	= 'homepage',
	),
	(r'^blog/', include('comfy.apps.blog.urls')),
	(r'^comments/', include('comfy.contrib.comments.urls')),
	(r'^notes/', include('comfy.apps.notes.urls')),
	(r'^bookmarks/', include('comfy.apps.bookmarks.urls')),
	(r'^tumblelog/', include('comfy.apps.tumblelog.urls')),
	(r'^tags/', include('comfy.contrib.tags.urls')),
	(r'^wiki/', include('comfy.apps.wiki.urls')),
	
	(r'^r/', include('comfy.contrib.redirects.urls')),
	(r'^admin/', include('comfy.contrib.admin.urls')),
)

if settings.DEBUG:
	from django.views.generic.simple import direct_to_template
	urlpatterns += patterns('',
		(r'^favicon.ico$', 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT }),
		(r'^%s/(.*)$' % escape(settings.MEDIA_URL.strip('/')), 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT }),
		(r'^404/$', direct_to_template, {'template': '404.html'}),
		(r'^500/$', direct_to_template, {'template': '500.html'}),
	)
