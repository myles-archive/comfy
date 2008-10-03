from re import escape
from django.conf import settings
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$',
		view	= 'comfy.apps.tumblelog.views.index',
		name	= 'homepage',
	),
	(r'^blog/', include('comfy.apps.blog.urls')),
	(r'^comments/', include('comfy.apps.comments.urls')),
	(r'^notes/', include('comfy.apps.notes.urls')),
	
	(r'^r/', include('comfy.apps.redirects.urls')),
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	(r'^admin/blog/', include('comfy.apps.blog.admin_urls')),
	(r'^admin/(.*)', admin.site.root),
)

if settings.DEBUG:
	urlpatterns += patterns('',
		(r'^%s/(.*)$' % escape(settings.MEDIA_URL.strip('/')), 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT }),
	)
