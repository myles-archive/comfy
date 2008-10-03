from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

db = settings.COUCHDB

def index(request):
	"""
	The tumblelog index page.
	"""
	items = list(db.view('_view/tumblelog/by_type'))
	
	context = { 'items': items }
	
	return render_to_response('tumblelog/index.html', context, context_instance=RequestContext(request))
