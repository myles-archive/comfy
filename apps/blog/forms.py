from django import forms
from django.conf import settings

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
	"""
	TODO None of this is going to work.
	"""
	author_name = forms.CharField()
	author_email = forms.EmailField()
	author_url = forms.URLField()
	comment = forms.CharField(widget=forms.Textarea)
