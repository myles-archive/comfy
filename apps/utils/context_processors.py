import datetime

from django.contrib.sites.models import Site
from django.conf import settings

from comfy import get_version

def standard(request):
	context = {
		'site_name':		Site.objects.get_current().name,
		'section':			request.path[1:-1].split('/')[0] or 'home',
		'current_year':		datetime.date.today().year,
		'site_url':			Site.objects.get_current().domain,
		'today':			datetime.datetime.now(),
		'comfy_verson':		get_version(),
	}
	return context
