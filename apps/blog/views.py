from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.core.urlresolvers import reverse

from comfy.apps.blog.models import Post
# from comfy.apps.blog.forms import 

# db = settings.COUCHDB

def index(request):
	"""
	The weblog index page.
	"""
	posts = list(Post.by_time(descending=True, count=10))
	
	return render_to_response('blog/index.html', { 'posts': posts }, context_instance=RequestContext(request))

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
	
	# try:
	# 	User.objects.get(email=post.author.email)
	# except User.DoesNotExist:
	# 	User = None
	
	return render_to_response('blog/detail.html', { 'post': post, 'prev': prev, 'next': next }, context_instance=RequestContext(request))
