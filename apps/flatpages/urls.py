from django.conf.urls.defaults import *

urlpatterns = patterns('comfy.apps.flatpages.views',
	(r'^(?P<url>.*)$', 'flatpage'),
)