from django.shortcuts import render_to_response
from django.template import RequestContext

from comfy.contrib.tags.models import Tag

def index(request):
	tags = Tag.all_tags()
	
	context = { 'tags': tags }
	
	return render_to_response('tags/index.html', context, context_instance=RequestContext(request))

def detail(request, tag):
	docs = list(Tag.by_tag()[[tag]:[tag, "9999"]])
	tags = Tag.all_tags()
	
	context = {
		'docs':	docs,
		'tags':	tags,
		'tag':	tag
	}
	
	return render_to_response('tags/detail.html', context, context_instance=RequestContext(request))
