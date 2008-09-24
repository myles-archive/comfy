from django import forms

from comfy.apps.tags.fields import TagField

class PostForm(forms.Form):
	title			= forms.CharField(label=u"Title")
	slug			= forms.CharField(label=u"Slug", help_text="If not entered will be generated automatically.", required=False)
	body			= forms.CharField(label=u"Body", widget=forms.Textarea)
	tags			= TagField(label=u"Tags", required=False, help_text=u"Seperate tags with a comma (,).")
	published		= forms.DateField(label=u"Published", initial=False)
	allow_comments	= forms.BooleanField(label=u"Allow Comments", initial=True)
	allow_pings		= forms.BooleanField(label=u"Allow Pings", initial=True)
