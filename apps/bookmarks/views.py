from datetime import datetime, date

from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from comfy.apps.bookmarks.models import Bookmark
from comfy.contrib.comments.forms import CommentForm

# db = settings.COUCHDB

def index(request, page=1):
	bookmark_list = list(Bookmark.by_time(descending=True))
	paginator = Paginator(bookmark_list, 10)
	
	try:
		bookmarks = paginator.page(page)
	except (EmptyPage, InvalidPage):
		bookmarks = paginator.page(paginator.num_pages)
	
	context = {
		'bookmarks':			bookmarks.object_list,
		'has_next':				bookmarks.has_next(),
		'has_previous':			bookmarks.has_previous(),
		'has_other_pages':		bookmarks.has_other_pages(),
		'start_index':			bookmarks.start_index(),
		'end_index':			bookmarks.end_index(),
		'previous_page_number':	bookmarks.previous_page_number(),
		'next_page_number':		bookmarks.next_page_number(),
	}
	
	return render_to_response('bookmarks/index.html', context, context_instance=RequestContext(request))
