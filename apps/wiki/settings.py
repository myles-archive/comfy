from django.conf import settings

YAKI_EMPTY_PAGE = getattr(settings, "YAKI_EMPTY_PAGE", "meta/EmptyPage")
YAKI_HOME_PAGE = getattr(settings, "YAKI_HOME_PAGE", "HomePage")
YAKI_PLUGINS_DIR = getattr(settings, "YAKI_PLUGINS_DIR", 'apps/wiki/plugins/')