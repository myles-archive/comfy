from django import forms
from django.contrib.admin import widgets

from comfy.core.tags.fields import TagField

class PostForm(forms.Form):
	title			= forms.CharField(label=u"Title", required=True, widget=widgets.AdminTextInputWidget)
	slug			= forms.CharField(label=u"Slug", help_text="If not entered will be generated automatically.", required=False, widget=widgets.AdminTextInputWidget)
	body			= forms.CharField(label=u"Body", widget=widgets.AdminTextareaWidget)
	tags			= TagField(label=u"Tags", required=False, help_text=u"Seperate tags with a comma (,).", widget=widgets.AdminTextInputWidget)
	published		= forms.DateField(label=u"Published", widget=widgets.AdminDateWidget)
	allow_comments	= forms.BooleanField(label=u"Allow Comments", initial=True)
	allow_pings		= forms.BooleanField(label=u"Allow Pings", initial=True)
