import vobject

from django.http import HttpResponse

EVENT_ITEMS = (
	('uid', 'uid'),
	('dtstart', 'start'),
	('dtend', 'end'),
	('summary', 'summary'),
	('location', 'location'),
	('last_modified', 'last_modified'),
	('created', 'created'),
)

class ICalendarFeed(object):
	
	def __call__(self, *args, **kwargs):
		cal = vobject.iCalendar()
		
		for item in self.items():
			event = cal.add('vevent')
			# TODO http://www.technobabble.dk/2008/mar/06/exposing-calendar-events-using-icalendar-django/