from datetime import datetime
from urllib import unquote_plus

from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

from comfy.apps.utils.akismet import Akismet
from comfy.apps.comments.forms import CommentForm
from comfy.apps.comments.models import Comment

db = settings.COUCHDB

def post(request):
	if request.method == 'POST':
		new_data = request.POST.copy()
		form = CommentForm(new_data)
		success_redirect = unquote_plus(new_data['next']) + "?comment=sucess"
		error_redirect = unquote_plus(new_data['next']) + "?comment=error"
		comments_closed_redirect = unquote_plus(new_data['next']) + "?comment=closed"
		if form.is_valid():
			if not request.user.is_active:
				ak_api = Akismet(settings.AKISMET_API_KEY, blog_url="http://%s/" % Site.objects.get_current().domain, agent=settings.DEFAULT_USER_AGENT)
				if ak_api.verify_key():
					ak_data = {
						'user_ip': request.META.get('REMOTE_ADDR', '127.0.0.1'),
						'user_agent': request.META.get('HTTP_USER_AGENT', ''),
						'referrer': request.META.get('HTTP_REFERER', ''),
						'comment_type': 'comment',
						'comment_author': form.cleaned_data['author_name'],
						'comment_author_email': form.cleaned_data["author_email"],
						'comment_author_url': form.cleaned_data["author_url"]
					}
				if ak_api.comment_check(form.cleaned_data["comment"], data=ak_data, build_data=True):
					is_spam = True
				else:
					is_spam = False
			else:
				is_spam = False
				form.cleaned_data['author_name'] = request.user.get_full_name()
				form.cleaned_data['author_email'] = request.user.email
			
			document = Comment.load(db, form.cleaned_data["document_id"])
			if document.allow_comments:
				document.comments.user_agent = request.META.get('REMOTE_ADDR', '127.0.0.1')
				document.comments.ip_address = request.META.get('HTTP_USER_AGENT', '')
				document.comments.author = { 'name': form.cleaned_data["author_name"], 'email': form.cleaned_data["author_email"], 'url': form.cleaned_data["author_url"] }
				document.comments.comment = form.cleaned_data["comment"]
				document.comments.is_spam = is_spam
				document.comments.time = datetime.now()
				document.store()
			else:
				return HttpResponseRedirect(comments_closed_redirect)
			
			return HttpResponseRedirect(success_redirect)
		else:
			return HttpResponseRedirect(error_redirect)
	
	return HttpResponseBadRequest()
