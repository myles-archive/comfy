from comfy.apps.flatpages.models import FlatPage
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings
from django.core.xheaders import populate_xheaders
from django.utils.safestring import mark_safe

DEFAULT_TEMPLATE = 'flatpages/default.html'

def flatpage(request, url):
	"""
	Flat page view.
	"""
	if not url.endswith('/') and settings.APPEND_SLASH:
		return HttpResponseRedirect("%s/" % request.path)
	
	if not url.startswith('/'):
		url = "/" + url
	
	flatpages = list(FlatPage.by_url()[(url)])
	
	try:
		f = flatpages[0]
	except:
		raise Http404
	
	# If registration is required for accessing this page, and the user isn't
	# logged in, redirect to the login page.
	if f.registration_required and not request.user.is_authenticated():
		from django.contrib.auth.views import redirect_to_login
		return redirect_to_login(request.path)
	
	if f.template_name:
		t = loader.select_template((f.template_name, DEFAULT_TEMPLATE))
	else:
		t = loader.get_template(DEFAULT_TEMPLATE)
	
	# To avoid having to always use the "|safe" filter in flatpage templates,
	# mark the title and content as already safe (since they are raw HTML
	# content in the first place).
	f.title = mark_safe(f.title)
	f.content = mark_safe(f.content)
	
	c = RequestContext(request, {
		'flatpage': f,
	})
	response = HttpResponse(t.render(c))
	# populate_xheaders(request, response, FlatPage, f.id)
	return response
