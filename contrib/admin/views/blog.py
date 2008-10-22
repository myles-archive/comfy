from django.template import RequestContext, Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django import forms

from comfy.apps.blog.models import Post
from comfy.apps.blog.forms import PostForm

db = settings.COUCHDB

@staff_member_required
def index(request):
	context = {}
	return render_to_response('comfy_admin/blog/index.html', context, context_instance=RequestContext(request))

@staff_member_required
def post_list(request):
	posts = list(Post.by_time())
	
	return render_to_response('comfy_admin/blog/posts/post_list.html', {
		'posts':	posts,
	}, context_instance=RequestContext(request))

@staff_member_required
def post_add_edit(request, id=None):
	if id:
		post = Post.load(db, id)
		form = PostForm(initial={
			'title':			post.title,
			'slug':				post.slug,
			'body':				post.body,
			'published':		post.published,
			'tags':				', '.join(post.tags),
			'allow_comments':	post.allow_comments,
			'allow_pings':		post.allow_pings
		})
		add = False
	else:
		post = None
		form = PostForm()
		add = True
	
	if request.method == 'POST':
		new_data = request.POST.copy()
		form = PostForm(new_data)
		if form.is_valid():
			if add:
				# Adding a new Post
				post = Post()
				post.title = form.cleaned_data['title']
				post.slug = form.cleaned_data['slug']
				post.body = form.cleaned_data['body']
				post.published = form.cleaned_data['published']
				post.tags = form.cleaned_data['tags']
				post.allow_comments = form.cleaned_data['allow_comments']
				post.allow_pings = form.cleaned_data['allow_pings']
				post.store()
			else:
				# Updating a new Post
				post = Post.load(db, id)
				post.title = form.cleaned_data['title']
				post.slug = form.cleaned_data['slug']
				post.body = form.cleaned_data['body']
				post.published = form.cleaned_data['published']
				post.tags = form.cleaned_data['tags']
				post.allow_comments = form.cleaned_data['allow_comments']
				post.allow_pings = form.cleaned_data['allow_pings']
				post.store()
	
	return render_to_response('comfy_admin/blog/posts/post_add_edit.html', {
		'title':		u'%s %s' % (add and _('Add') or _('Edit'), _('page')),
		'post':			post,
		'form':			form,
		'add':			add,
	}, context_instance=RequestContext(request))
