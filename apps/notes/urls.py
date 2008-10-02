from django.conf.urls.defaults import *

urlpatterns = patterns('comfy.apps.notes.views',
	url(r'^create/$',
		view = 'create',
		name = 'note_create',
	),
	url(r'^(?P<note_id>[-\w]+)/update/$',
		view = 'update',
		name = 'note_update',
	),
	url(r'^(?P<note_id>[-\w]+)/delete/$',
		view = 'delete',
		name = 'note_delete',
	),
	url(r'^(?P<note_id>[-\w]+)/$',
		view = 'detail',
		name = 'note_detail',
	),
	url(r'^$',
		view = 'index',
		name = 'notes_index'
	),
)