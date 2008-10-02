from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings

from comfy.apps.notes.models import Note
from comfy.apps.notes.forms import NoteForm

db = settings.COUCHDB

def index(request):
	# TODO Paginate
	notes = list(Note.by_time(descending=True, count=10))
	if request.user.is_staff:
		form = NoteForm()
	else:
		form = None
	
	return render_to_response('notes/index.html', { 'notes': notes, 'form': form }, context_instance=RequestContext(request))

def detail(request, note_id):
	note = Note.load(db, note_id)
	if note.private and not request.user.is_staff:
		raise Http404
	
	if request.user.is_staff:
		form = NoteForm(initial={
			'body':				note.body,
			'tags':				note.tags,
			'allow_comments':	note.allow_comments,
			'private':			note.private,
		})
	else:
		form = None
	
	return render_to_response('notes/detail.html', { 'note': note, 'form': form }, context_instance=RequestContext(request))

@staff_member_required
def delete(request, note_id):
	note = Note.load(db, note_id)
	
	if request.method == 'POST':
		# TODO The delete function here.
		return HttpResponseRedirect(reverse('notes_index'))
	
	return render_to_response('notes/delete.html', { 'note': note }, context_instance=RequestContext(request))

@staff_member_required
def create(request):
	if request.method == 'POST':
		new_data = request.POST.copy()
		form = NoteForm(new_data)
		if form.is_valid():
			note = Note()
			note.body = form.cleaned_data['body']
			note.tags = form.cleaned_data['tags']
			note.allow_comments = form.cleaned_data['allow_comments']
			note.private = form.cleaned_data['private']
			note.store()
	
	form = NoteForm()
	return render_to_response('notes/form.html', { 'form': form }, context_instance=RequestContext(request))

@staff_member_required
def update(request, note_id):
	note = Note.load(db, note_id)
	
	if request.method == 'POST':
		new_data = request.POST.copy()
		form = NoteForm(new_data)
		if form.is_valid():
			note.body = form.cleaned_data['body']
			note.tags = form.cleaned_data['tags']
			note.allow_comments = form.cleaned_data['allow_comments']
			note.private = form.cleaned_data['private']
			note.store()
	
	form = NoteForm(initial={
		'body':				note.body,
		'tags':				note.tags,
		'allow_comments':	note.allow_comments,
		'private':			note.private,
	})
	
	return render_to_response('notes/form.html', { 'form': form, 'note': note }, context_instance=RequestContext(request))
