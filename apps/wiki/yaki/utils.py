#!/usr/bin/env python
# encoding: utf-8
"""
Utils.py

Miscellaneous utility functions

Created by Rui Carmo on 2006-09-10.
Published under the MIT license.
"""

import math, time, datetime, unittest, feedparser
import os, sys, re, sha, binascii, fnmatch, xmlrpclib, cgi
import comfy.apps.wiki.yaki.locale as Locale

#
# Shared data - constants, definitions, etc.
# 

# Characters used for generating page/URL aliases
ALIASING_CHARS = ['','.','-','_']

# Prefixes used to identify attachments (cid is MIME-inspired)
ATTACHMENT_SCHEMAS = ['cid','attach']

# regexp for matching caching headers
MAX_AGE_REGEX = re.compile('max-age(\s*)=(\s*)(\d+)')


#
# Date handling
#

# Embrace and extend Mark's feedparser mechanism
_textmate_date_re = \
    re.compile('(\d{4})-(\d{2})-(\d{2})\s+(\d{2}):(\d{2}):(\d{2})$')

def parseDate(date):
  """
  Parse a TextMate date (YYYY-MM-DD HH-MM-SS, no time zone)
  """
  m = _textmate_date_re.match(date)
  if not m:
    return time.mktime(feedparser._parse_date(date))
  isodate = '%(year)s-%(month)s-%(day)sT%(hour)s:%(minute)s:%(second)s%(zonediff)s' % {'year': m.group(1), 'month': m.group(2), 'day': m.group(3), 'hour': m.group(4), 'minute': m.group(5), 'second': m.group(6), 'zonediff': '+00:00'} 
  return time.mktime(feedparser._parse_date(isodate))

def isoTime(value=None):
  """
  Time string in ISO format
  """
  if value == None:
    value = time.localtime()
  tz = time.timezone/3600
  return time.strftime("%Y-%m-%dT%H:%M:%S-", value) + ("%(tz)02d:00" % vars())

def httpTime(value=None):
  """
  Time string for HTTP headers
  """
  if value == None:
    value = time.localtime()
  return time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime(value))

def plainTime(i18n, value=None):
  """
  A simple time string
  """
  value = float(value)
  format = "%H:%M"
  if time.gmtime(value)[0] != time.gmtime()[0]:
    # we have a different year
    format = "%Y, " + format
  format = i18n[time.strftime("%b",time.gmtime(value))] + " %d, " + format
  return time.strftime(format, time.gmtime(value))

def timeSince(i18n, older=None,newer=None,detail=2):
  """
  Human-readable time strings, based on Natalie Downe's code from
  http://blog.natbat.co.uk/archive/2003/Jun/14/time_since
  Assumes time parameters are in seconds
  """
  intervals = {
    31556926: 'year', # corrected from the initial 31536000
    2592000: 'month',
    604800: 'week',
    86400: 'day',
    3600: 'hour',
    60: 'minute',
  }
  chunks = intervals.keys()
  
  # Reverse sort using a lambda (for Python 2.3 backwards compatibility)
  chunks.sort(lambda x, y: y-x)
  
  if newer == None:
    newer = time.time()
  
  interval = newer - older
  if interval < 0:
    return i18n['some_time']
    # We should ideally do this:
    # raise ValueError('Time interval cannot be negative')
    # but it makes sense to fail gracefully here
  if interval < 60:
    return i18n['less_1min']
  
  output = ''
  for steps in range(detail):
    for seconds in chunks:
      count = math.floor(interval/seconds)
      unit = intervals[seconds]
      if count != 0:
        break
    if count > 1:
      unit = unit + 's'
    if count != 0:
      output = output + "%d %s, " % (count, i18n[unit])
    interval = interval - (count * seconds)
  output = output[:-2]
  return output
  
#
# String utility functions
#

def rsplit(s, sep=None, maxsplit=-1):
  """
  Equivalent to str.split, except splitting from the right.
  """
  if sys.version_info < (2, 4, 0):
    if sep is not None:
      sep = sep[::-1]
    L = s[::-1].split(sep, maxsplit)
    L.reverse()
    return [s[::-1] for s in L]
  else:
    return s.rsplit(sep, maxsplit)


def shrink(line,bound=50,rep='[...]'):
  """
  Shrinks a string, adding an ellipsis to the middle
  """
  l = len(line)
  if l < bound:
    return line
  if bound <= len(rep):
    return rep
  k = bound - len(rep)
  return line[0:k/2] + rep + line[-k/2:]

#
# File utility functions
#

def locate(pattern, root=os.getcwd()):
  """
  Generator for iterating inside a file tree
  """
  for path, dirs, files in os.walk(root):
    for filename in [os.path.abspath(os.path.join(path, filename)) for filename in files if fnmatch.fnmatch(filename, pattern)]:
      yield filename

#
# Wild Wild Web
#

def formatComments(ac, request, path):
  c = request.getContext()
  # Try to use the main site URL to avoid trouble with reverse proxying and port numbers
  try:
    siteurl = ac.siteinfo['siteurl'] 
  except:
    siteurl = request.getBaseURL()
  baseurl = siteurl + ac.base
  c.comments = ""
  # check if we need to deal with comments here
  if ac.commentwindow > 0 and re.match('^blog',path):
    try:
      mtime = ac.indexer.pageinfo[path]['last-modified']
      title = ac.indexer.pageinfo[path]['title']
      window = mtime + ac.commentwindow - time.time()
      if int(window/86400) > 0:
        c.comments = ac.templates['comments-enabled'] % {'page':path, 'window': str(int(window/86400)), 'permalink': baseurl + path, 'title': cgi.escape(title)} 
      else:
        c.comments = ac.templates['comments-disabled'] % {'permalink': baseurl + path, 'title': cgi.escape(title)}
    except:
      pass

def doPings(siteinfo):
  try:
    for target in siteinfo['ping']:
      if target == 'technorati':
        print "Pinging Technorati..."
        server = xmlrpclib.Server('http://rpc.technorati.com/rpc/ping')
        print server.weblogUpdates.ping(siteinfo['sitetitle'], siteinfo['ping'][target])
  except:
    pass
