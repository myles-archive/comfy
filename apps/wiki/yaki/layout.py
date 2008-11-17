#!/usr/bin/env python
# encoding: utf-8
"""
Layout.py

Utility functions for formatting and layout (i.e., stuff that affects navigation, page look, etc.)

Created by Rui Carmo on 2006-09-23.
Published under the MIT license.
"""

import sys, os
from comfy.apps.wiki.yaki.utils import *

def pagetrail(i18n, trail, linkclass = "wiki"):
  """
  Build a breadcrumb trail for display atop the page
  """
  buffer = []
  for crumb in trail:
    buffer.append('<a class="%s" href="%s" title="%s %s">%s</a> : ' % (linkclass,crumb['link'],crumb['name'],
    i18n['updated_ago_format'] % timeSince(i18n, crumb['last-modified']), crumb['title']))
  return ''.join(buffer)[:-2]

def technoratiTags(headers, soup):
  """
  Build a div containing Technorati-style "tags" from the Wiki links and other page metadata
  """
  parse = ['keywords','categories','tags'] # headers to parse
  all = [] 
  links = soup.findAll('a',{'class':re.compile('^wiki.*')})
  for link in links:
    if 'blog' not in link['href'].lower():
      tags = link['href'].lower().split('/')
      for tag in tags:
        if tag not in all and tag != '':
          all.append(tag)
  for header in parse:
    if header in headers:
      tags = [tag.strip().lower() for tag in headers[header].split(',')]
      for tag in tags:
        if tag not in all and tag != '':
          all.append(tag)
  if len(all) < 4: # be sparing
    return ''
  all.sort()
  buffer=[]
  for tag in all:
    buffer.append('<a href="http://technorati.com/tag/%s" rel="tag">%s</a>' % (tag, tag))
  return '<div class="technorati_tags" align="right"><small>Technorati Tags: %s</small></div>' % ', '.join(buffer)

def linktable(i18n, pagehash, width = 4, linkclass = "wiki", tableclass = "seealso", sort=True):
  """
  The world famous SeeAlso table
  """
  i = 0
  pages = pagehash.keys()
  if sort:
    pages.sort(lambda a, b: -cmp(pagehash[a]['last-modified'],pagehash[b]['last-modified']))
  count = len(pages)
  row = []
  buffer = []
  for link in pages:
    td = '<a class="%s" href="%s" title="%s %s">%s</a>' % (linkclass,link,pagehash[link]['name'],
    i18n['updated_ago_format'] % timeSince(i18n, pagehash[link]['last-modified']), pagehash[link]['title'])
    color = '#' + ('%02X' % (16*16 - (1.0*i/count)*48-1)) + ('%02X' % (16*16 - (1.0*i/count)*38-1)) + ('%02X' % (16*16 - (1.0*i/count)*32-1))
    row.append('<td width="%d%%" bgcolor="%s">%s</td>' % (100/width, color, td))
    i = i + 1
    if 0 == i % 4:
      buffer.append('<tr>%s</tr>' % ''.join(row))
      row = []
  buffer.append('<tr>%s</tr>' % ''.join(row))
  return '<table class="%s" width="100%%">%s</table>' % (tableclass,''.join(buffer))
