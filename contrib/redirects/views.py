from django.http import Http404, HttpResponseRedirect
from django.conf import settings

from comfy.core.redirects.models import Document

db = settings.COUCHDB

def redirect(request, document_id):
	# FIXME Fuck I am an idiot need to figure out a way to make this better.
	# Maybe something like Django's Content Types where it will look up the model
	# within the `INSTALLED_APPS` or something.
	try:
		doc = Document.load(db, document_id)
	except:
		raise Http404
	
	# Is it a Blog post?
	if doc.type == 'Post':
		from comfy.apps.blog.models import Post
		post = Post.load(db, doc.id)
		return HttpResponseRedirect(post.get_absolute_url())
	# Is it a Flat page?
	elif doc.type == 'FlatPage':
		from comfy.apps.flatpages.models import FlatPage
		f = FlatPage.load(db, doc.id)
		return HttpResponseRedirect(f.get_absolute_url())
	# Is it a Note?
	elif doc.type == 'Note':
		from comfy.apps.notes.models import Note
		note = Note.load(db, doc.id)
		return HttpResponseRedirect(note.get_absolute_url())
	else:
		raise Http404
