from django import forms
from django.conf import settings
from django.contrib.sites.models import Site

from comfy.core.comments.models import Comment

db = settings.COUCHDB

class CommentForm(forms.Form):
	document_id		= forms.CharField(widget=forms.HiddenInput)
	next			= forms.CharField(widget=forms.HiddenInput, required=False)
	author_name		= forms.CharField(label=u"Name")
	author_email	= forms.EmailField(label=u"Email", help_text=u"We will not publish your email address.")
	author_url		= forms.URLField(label=u"URL", required=False)
	comment			= forms.CharField(label=u"Comment", widget=forms.Textarea)

class PingForm(forms.Form):
	document_id		= forms.CharField(widget=forms.HiddenInput)
	uri				= forms.CharField()
	title			= forms.CharField()
	excerpt			= forms.CharField()
	author			= forms.CharField()
	time			=  forms.CharField()
