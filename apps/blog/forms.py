from datetime import datetime
from django import forms
from django.conf import settings
from django.contrib.sites.models import Site

from comfy.apps.blog.models import Post

db = settings.COUCHDB

class PostForm(forms.Form):
	"""
	TODO None of this is going to work.
	"""
	title = forms.CharField()
	body = forms.CharField(widget=forms.Textarea)
	tags = forms.CharField()
	published = forms.DateTimeField()
	allow_comments = forms.BooleanField()
	allow_pings = forms.BooleanField()

class CommentForm(forms.Form):
	document_id		= forms.CharField(widget=forms.HiddenInput)
	author_name		= forms.CharField(label=u"Name")
	author_email	= forms.EmailField(label=u"Email", help_text=u"We will not publish your email address.")
	author_url		= forms.URLField(label=u"URL", required=False)
	comment			= forms.CharField(label=u"Comment", widget=forms.Textarea)
	
	def save(self, user_agent, ip_address):
		from comfy.apps.utils.akismet import Akismet
		a = Akismet(settings.AKISMET_API_KEY, blog_url="http://%s/" % Site.objects.get_current().domain)
		akismet_data = {}
		akismet_data['comment_type'] ='comment'
		post = Post.load(db, self.cleaned_data["document_id"])
		if post.allow_comments:
			post.comments.user_agent = akismet_data['user_agent'] = user_agent
			post.comments.ip_address = akismet_data['ip_address'] = ip_address
			post.comments.author(name=self.cleaned_data["author_name"], email=self.cleaned_data["author_email"], url=self.cleaned_data["author_url"])
			akismet_data['comment_author'] = self.cleaned_data["author_name"]
			akismet_data['comment_author_email'] = self.cleaned_data["author_email"]
			akismet_data['comment_author_url'] = self.cleaned_data["author_url"]
			post.comments.comment = self.cleaned_data["comment"]
			post.comments.is_spam = a.comment_check(post.comments.comment, akismet_data)
			post.comments.time = datetime.now()
			post.comments.store(db)
			return post.comments
		else:
			return None
