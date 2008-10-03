from django import template
from django.template.loader import get_template
from django.utils.html import escape
from django.conf import settings

from comfy.apps.blog.models import Post
from comfy.apps.notes.models import Note
from comfy.apps.wiki.models import Document

db = settings.COUCHDB
register = template.Library()

@register.filter
def render_item(item, document_type=None, template_directory='items'):
	if document_type == 'Post':
		content_object = Post.load(db, item.id)
	elif document_type == 'Note':
		content_object = Note.load(db, item.id)
	elif document_type == 'Wiki':
		content_object = Document.load(db, item.id)
	else:
		content_object = None
		document_type = 'none'
		
	t = get_template('tumblelog/%s/%s.html' % (template_directory, document_type.lower()))
	return t.render(template.Context({ 'item': content_object }))
