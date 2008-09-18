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
