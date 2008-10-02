from datetime import datetime
from urllib import quote_plus
from itertools import groupby

from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.core.urlresolvers import reverse

from comfy.apps.blog.models import Post
from comfy.apps.comments.forms import CommentForm

# db = settings.COUCHDB

def index(request):
	"""
	The weblog index page.
	"""
	posts = list(Post.by_time(descending=True, count=10))
	
	context = { 'posts': posts }
	
	return render_to_response('blog/index.html', context, context_instance=RequestContext(request))

def archive_month(request, year, month):
	"""
	The weblog arichve page for a given year.
	"""
	posts = []
	prev = next = None
	for year_month, lst in groupby(Post.by_month(), lambda x: (x.published.year, x.published.month)):
		if year_month == (int(year), int(month)):
			posts = list(lst)
		elif not posts:
			prev = year_month
		else:
			next = year_month
			break
	
	context = {
		'posts':	posts,
		'month':	datetime(int(year), int(month), 1),
		'prev':		prev and datetime(prev[0], prev[1], 1) or None,
		'next':		next and datetime(next[0], next[1], 1) or None
	}
	
	return render_to_response('blog/archive_month.html', context, context_instance=RequestContext(request))

def detail(request, year, month, day, slug):
	"""
	The weblog post detail page.
	"""
	posts = list(Post.by_slug()[(int(year), int(month), int(day), slug)])
	post = posts[0]
	
	prev = list(Post.by_time(count=-1, startkey_docid=post.id, skip=1)
		[[post.published.isoformat() + 'Z']:])
	next = list(Post.by_time(count=1, startkey_docid=post.id, skip=1)
		[[post.published.isoformat() + 'Z']:])
	
	try:
		user = User.objects.get(email=post.author.email)
	except User.DoesNotExist:
		user = None
	
	comment_form = CommentForm(initial={
		'document_id':	post.id,
		'next':			quote_plus(post.get_absolute_url())
	})
	
	context = {
		'post':			post,
		'prev':			prev,
		'next':			next,
		'user':			user,
		'comment_form':	comment_form
	}
	
	return render_to_response('blog/detail.html', context, context_instance=RequestContext(request))
