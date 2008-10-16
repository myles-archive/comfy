from django.conf import settings
from django.core.management.base import NoArgsCommand
import os
from glob import glob
from optparse import make_option

class Command(NoArgsCommand):
	help = "Index CouchDB Documents."
	
	def handle_noargs(self, **options):
		if settings.XAPIAN_INDEX_DIR:
			if not os.path.isdir(settings.XAPIAN_INDEX_DIR):
				os.mkdir(settings.XAPIAN_INDEX_DIR)
			
			from comfy.apps.search.index import Index, updates
			index = Index(dir=settings.XAPIAN_INDEX_DIR)
			index.reindex()
		else:
			print "\nSearch is disabled."
