from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response
from django.template import RequestContext

@staff_member_required
def index(request):
	context = {}
	return render_to_response('comfy_admin/index.html', context, context_instance=RequestContext(request))
