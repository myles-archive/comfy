# Django settings for comfy project.
import os, sys, logging
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
execfile(os.path.join(PROJECT_ROOT, 'local_settings.py'))

logging.basicConfig(
	level	= logging.DEBUG,
	format	= '%(asctime)s %(levelname)s %(message)s',
)
logging.info("Loading settings file.")

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
	# ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = MEDIA_URL + '/admin/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.load_template_source',
	'django.template.loaders.app_directories.load_template_source',
	# 'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
	'comfy.apps.flatpages.middleware.FlatpageFallbackMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'comfy.urls'

TEMPLATE_DIRS = (
	# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
	# Always use forward slashes, even on Windows.
	# Don't forget to use absolute paths, not relative paths.
	os.path.join(PROJECT_ROOT, 'templates/'),
)

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.admin',
	'django.contrib.admindocs',
	'django.contrib.humanize',
	'django.contrib.markup',
	'comfy.apps.blog',
	'comfy.apps.flatpages',
	'comfy.apps.tumblelog',
	'comfy.apps.talks',
	'comfy.apps.notes',
	'comfy.apps.bookmarks',
	'comfy.apps.events',
	'comfy.apps.wiki',
	'comfy.contrib.search',
	'comfy.contrib.comments',
	'comfy.contrib.utils',
	'comfy.contrib.redirects',
	'comfy.contrib.tags',
	'comfy.contrib.admin',
)

TEMPLATE_CONTEXT_PROCESSORS = (
	'django.core.context_processors.auth',
	'django.core.context_processors.media',
	'comfy.contrib.utils.context_processors.standard',
)

DEFAULT_USER_AGENT = "Comfy/0.1 (http://mylesbraithwaite.com/)"
URL_VALIDATOR_USER_AGENT = DEFAULT_USER_AGENT

LOGIN_REDIRECT_URL = '/'

DATE_FORMAT = 'l, j F, Y'
TIME_FORMAT = 'g:i a'
YEAR_MONTH_FORMAT = 'F Y'
MONTH_DAY_FORMAT = 'j F'
DATETIME_FORMAT = DATE_FORMAT + TIME_FORMAT

from couchdb import Server, ResourceConflict, ServerError
from socket import error as SocketError
try:
	SERVER = Server(COUCHDB_SERVER)
	try:
		COUCHDB = SERVER.create(COUCHDB_DATABASE)
		logging.info("Need to created the database %s" % COUCHDB_DATABASE)
	except ResourceConflict:
		COUCHDB = SERVER[COUCHDB_DATABASE]
	except ServerError:
		COUCHDB = SERVER[COUCHDB_DATABASE]
except SocketError:
	logging.error("Could not connect to the CouchDB server at %s." % COUCHDB_SERVER)
	SERVER = None
	COUCHDB = None
