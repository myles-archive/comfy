from datetime import date, datetime
from time import strptime
from calendar import timegm

from django import template

register = template.Library()

def convert_date(value):
	if isinstance(value, basestring):
		try:
			value = date(*strptime(value, '%Y-%m-%d')[:3])
		except ValueError, e:
			raise ValueError('Invalid ISO date %r' % value)
	return value

register.filter('convert_date', convert_date)

def convert_datetime(value):
	if isinstance(value, basestring):
		try:
			value = value.split('.', 1)[0]
			value = value.rstrip('Z')
			timestamp = timegm(strptime(value, '%Y-%m-%dT%H:%M:%S'))
			value = datetime.utcfromtimestamp(timestamp)
		except ValueError, e:
			raise ValueError('Invalid ISO date/time %r' % value)
	return value

register.filter('convert_datetime', convert_datetime)