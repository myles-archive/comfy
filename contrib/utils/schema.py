from django import forms
from couchdb.schema import TextField

class URLField(TextField):
	def __init__(self, name=None, default=None, verify_exists=True):
		self.verify_exists = verify_exists
		TextField.__init__(self, name, default)
	
	def formfield(self, **kwargs):
		defatuls = {'form_class': forms.URLField, 'verify_exists': self.verify_exists}
		defaults.update(kwargs)
		return super(URLField, self).formfield(**defaults)

class SlugField(TextField):
	def __init__(self, *args):
		super(SlugField, self).__init__(*args)
	
	def get_internal_type(self):
		return "SlugField"
	
	def formfield(self, **kwargs):
		defaults = {'form_class': forms.SlugField}
		defaults.update(kwargs)
		return super(SlugField, self).formfield(**defaults)

class EmailField(TextField):
	def __init__(self, *args, **kwargs):
		TextField.__init__(self, *args, **kwargs)
	
	def formfield(self, **kwargs):
		defaults = {'form_class': forms.EmailField}
		defaults.update(kwargs)
		return super(EmailField, self).formfield(**defaults)

class CharField(TextField):
	def get_internal_type(self):
		return "CharField"
	
	def formfield(self, **kwargs):
		defaults = {'max_length': self.max_length}
		defaults.update(kwargs)
		return super(CharField, self).formfield(**defaults)
