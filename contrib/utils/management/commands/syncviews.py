from django.conf import settings
from django.core.management.base import NoArgsCommand
import os
from glob import glob
from optparse import make_option

class Command(NoArgsCommand):
	option_list = NoArgsCommand.option_list + (
		make_option('--verbosity', action='store', dest='verbosity', default='1',
			type='choice', choices=['0', '1', '2'],
			help='Verbosity level; 0=minimal output, 1=normal output, 2=all output'),)
	help = "Synchronize views in couchdb"
	
	def handle_noargs(self, **options):
		verbosity = int(options.get('verbosity', 1))
		
		db = settings.COUCHDB
		
		if verbosity >= 1:
			print "\nLoad CouchDB views ..."
		for app in settings.INSTALLED_APPS:
			appdir = os.path.dirname(__import__(app, {}, {}, ['']).__file__)
			design_path = os.path.join(appdir, '_design')
			if os.path.exists(design_path):
				for name in os.listdir(design_path):
					path = os.path.join(design_path,name)
					views = {}
					for view in os.listdir(path):
						views[view] = {}
						for js in glob(os.path.join(path, view, '*.js')):
							if os.path.basename(js) == 'map.js':
								views[view]['map'] = open(js, 'rb').read()
							if os.path.basename(js) == 'reduce.js':
								views[view]['reduce'] = open(js, 'rb').read()
						if verbosity >= 2:
							print "add %s/%s" % (name, view)
					try:
						db['_design/%s' % name] = {
							'language': 'javascript',
							'views': views
						}
					except:
						v = db['_design/%s' % name] 
						v['views'] = views
						db['_design/%s' % name] = v
