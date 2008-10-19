from re import escape
from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('',
	url(r'^$',
		view	= 'comfy.apps.tumblelog.views.homepage',
		name	= 'homepage',
	),
	(r'^blog/', include('comfy.apps.blog.urls')),
	(r'^comments/', include('comfy.core.comments.urls')),
	(r'^notes/', include('comfy.apps.notes.urls')),
	(r'^tumblelog/', include('comfy.apps.tumblelog.urls')),
	(r'^tags/', include('comfy.core.tags.urls')),
	
	(r'^r/', include('comfy.core.redirects.urls')),
	(r'^admin/', include('comfy.core.admin.urls')),
)

if settings.DEBUG:
	urlpatterns += patterns('',
		(r'^favicon.ico$', 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT }),
		(r'^%s/(.*)$' % escape(settings.MEDIA_URL.strip('/')), 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT }),
	)
