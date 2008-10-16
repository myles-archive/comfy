from django import forms
from django.contrib.admin import widgets

from comfy.core.tags.fields import TagField

class NoteForm(forms.Form):
	body			= forms.CharField(label=u"Body", widget=widgets.AdminTextareaWidget)
	tags			= TagField(label=u"Tags", required=False, help_text=u"Seperate tags with a comma (,).", widget=widgets.AdminTextInputWidget)
	allow_comments	= forms.BooleanField(label=u"Allow Comments", initial=False, widget=widgets.AdminTextInputWidget)
	private			= forms.BooleanField(label=u"Private", initial=False, widget=widgets.AdminTextInputWidget)
