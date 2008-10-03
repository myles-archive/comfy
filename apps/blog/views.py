from datetime import datetime, date
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

def archive_year(request, year):
	"""
	The weblog archive page for a given year.
	"""
	posts = []
	prev = next = None
	for year_time, lst in groupby(Post.by_month(), lambda x: x.published.year):
		if year_time == int(year):
			posts = list(lst)
		elif not posts:
			prev = year_time
		else:
			next = year_time
			break
	
	context = {
		'posts':	posts,
		'year':		date(int(year), 1, 1),
		'prev':		prev and date(prev, 1, 1) or None,
		'next':		next and date(next, 1, 1) or None
	}
	
	return render_to_response('blog/archive_year.html', context, context_instance=RequestContext(request))

def archive_month(request, year, month):
	"""
	The weblog archive page for a given month.
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
		'month':	date(int(year), int(month), 1),
		'prev':		prev and date(prev[0], prev[1], 1) or None,
		'next':		next and date(next[0], next[1], 1) or None
	}
	
	return render_to_response('blog/archive_month.html', context, context_instance=RequestContext(request))

def archive_day(request, year, month, day):
	"""
	The weblog archive page for a given day.
	"""
	posts = []
	prev = next = None
	for year_month_day, lst in groupby(Post.by_month(), lambda x: (x.published.year, x.published.month, x.published.day)):
		if year_month_day == (int(year), int(month), int(day)):
			posts = list(lst)
		elif not posts:
			prev = year_month_day
		else:
			next = year_month_day
			break
		
	context = {
		'posts':	posts,
		'day':		date(int(year), int(month), int(day)),
		'prev':		prev and date(prev[0], prev[1], prev[2]) or None,
		'next':		next and date(next[0], next[1], next[2]) or None
	}
		
	return render_to_response('blog/archive_day.html', context, context_instance=RequestContext(request))

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
