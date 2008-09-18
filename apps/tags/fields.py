from django import forms

class TagField(forms.CharField):
	def clean(self, value):
		value = super(TagField, self).clean(value)
		tags = value.split(', ')
		return tags
