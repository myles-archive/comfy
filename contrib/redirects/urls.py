from django.conf.urls.defaults import *

urlpatterns = patterns('comfy.core.redirects.views',
	url(r'^(?P<document_id>\w+)/$',
		view	= 'redirect',
		name	= 'redirect'
	),
)