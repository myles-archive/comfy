from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage

db = settings.COUCHDB

def tumblelog_index_view(request, page=1, template_name='tumblelog/index.html', context={}):
	"""
	The tumblelog index page.
	"""
	item_list = list(db.view('_view/tumblelog/by_type', descending=True))
	paginator = Paginator(item_list, 10)
	
	try:
		items = paginator.page(page)
	except (EmptyPage, InvalidPage):
		items = paginator.page(paginator.num_pages)
	
	context.update({
		'items':				items.object_list,
		'has_next':				items.has_next(),
		'has_previous':			items.has_previous(),
		'has_other_pages':		items.has_other_pages(),
		'start_index':			items.start_index(),
		'end_index':			items.end_index(),
		'previous_page_number':	items.previous_page_number(),
		'next_page_number':		items.next_page_number(),
	})
	
	return render_to_response(template_name, context, context_instance=RequestContext(request))

def index(request, page=1):
	"""
	The tumblelog index page.
	"""
	return tumblelog_index_view(request, page)

def homepage(request):
	"""
	The homepage index page.
	"""
	context = {
		'homepage':		True,
	}
	return tumblelog_index_view(request, template_name='home.html', context=context)
