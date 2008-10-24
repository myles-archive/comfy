#!/usr/bin/env python
# encoding: utf-8
"""
Store.py

Content store access

Created by Rui Carmo on 2006-11-12.
Published under the MIT license.
"""

import os, stat, codecs
import rfc822 # for basic parsing
from comfy.apps.wiki.yaki.page import Page
from comfy.apps.wiki.yaki.utils import *

BASE_FILENAME="index.txt"
BASE_PAGE = """From: %(author)s
Date: %(date)s
Content-Type: %(markup)s
Content-Encoding: utf-8
Title: %(title)s
Keywords: %(keywords)s
Categories: %(categories)s
Tags: %(tags)s
%(_headers)s

%(content)s
"""

class Store:
  """
  Wiki Store - abstracts actual storage and versioning
  """
  def __init__(self, path="space"):
    """Constructor"""
    self.path = path
    self.pages={}
    self.aliases={}
    self.dates={}
  
  def getPath(self,pagename):
    """Append the store path to the pagename"""
    return os.path.join(self.path, pagename)
  
  def date(self, pagename):
    """
    Retrieve a page's stored date (or fall back to mtime)
    """
    if pagename in self.dates.keys():
      return self.dates[pagename]
    else:
      return self.mtime(pagename)

  def mtime(self, pagename):
    """
    Retrieve modification time for the current revision of a given page
    """
    targetpath = self.getPath(pagename)
    targetfile = os.path.join(targetpath, BASE_FILENAME)
    if(os.path.exists(targetpath)):
      if(os.path.exists(targetfile)):
        return os.stat(targetfile)[stat.ST_MTIME]
    return None
  
  def getAttachmentFilename(self, pagename, attachment):
    """
    Returns the filename for an attachment
    """
    targetpath = self.getPath(pagename)
    targetfile = os.path.join(targetpath,attachment)
    return targetfile
  
  def getRevision(self, pagename, revision = ""):
    """
    Retrieve the specified revision from the store.
    
    At this point we ignore the revision argument
    (versioning will be added at a later date, if ever)
    """
    targetpath = self.getPath(pagename)
    targetfile = os.path.join(targetpath,BASE_FILENAME)
    mtime = self.mtime(pagename)
    if mtime != None:
      mtime = self.mtime(pagename)
      try:
        buffer = codecs.open(targetfile,'r','utf-8').read()
        p = self.parseRaw(buffer)
  
        # If the page has no title header, use the path name
        if 'title' not in p.headers.keys():
          p.headers['title'] = pagename
        p.headers['name'] = pagename
        
        # Now try to supply a sensible set of dates
        try:
          # try parsing the date header
          p.headers['date'] = parseDate(p.headers['date'])
        except:
          # if there's no date header, use the file's modification time
          # (if only to avoid throwing an exception again)
          p.headers['date'] = mtime
          pass
        # Never rely on the file modification time for last-modified
        # (otherwise SVN, Unison, etc play havoc with modification dates)
        try:
          p.headers['last-modified'] = parseDate(p.headers['last-modified'])
        except:
          p.headers['last-modified'] = p.headers['date']
          pass
        self.dates[pagename] = p.headers['date']
        return p
      except IOError:
        raise IOError, "Couldn't find page %s." % (pagename)
    else:
       raise IOError, "Couldn't find page %s." % (pagename)
    return None
  
  def parseRaw(self,raw):
    """
    Parse raw page data (currently in RFC2822 format)
    """
    headers = {}
    try:
      (header_lines,buffer) = raw.split("\n\n", 1)
      for header in header_lines.split("\n"):
        (name, value) = header.split(": ", 1)
        headers[name.lower()] = unicode(value.strip())
      p = Page()
      p.headers = headers
      p.raw = unicode(buffer)
      return p
    except:
      raise TypeError, "Invalid page file format."
  
  def allPages(self):
    """
    Enumerate all pages and their last modification time
    """
    for folder, subfolders, files in os.walk(self.path):
      if( "index.txt" in files ):
        # Check for modification date of markup file only
        # (we can use the folder modification time instead)
        mtime = os.stat(os.path.join(folder,BASE_FILENAME))[stat.ST_MTIME]
        # Add each path (removing the self.path prefix)
        self.pages[folder[len(self.path)+1:]] = mtime

    for name in self.pages.keys():
      base = os.path.basename(name).lower()
      if base in self.aliases.keys():
        if len(self.aliases[base]) > len(name):
          self.aliases[base] = name
      else:
        self.aliases[base] = name        
      for replacement in ALIASING_CHARS:
        alias = name.lower().replace(' ',replacement)
        self.aliases[alias] = name
    return self.pages
  
  def updatePage(self, pagename, fields):
    """
    Updates a given page.
    """
    targetpath = self.getPath(pagename)
    if(not os.path.exists(targetpath)):
      os.makedirs(targetpath)
    filename = os.path.join(targetpath,BASE_FILENAME) 
    try:
      open(filename, "wb").write((BASE_PAGE % fields).encode('utf-8'))
    except IOError:
      return None
    return True
  

#=================================

if __name__=="__main__":
  print "Initializing test store."
  s = Store('../space')
  print s.allPages()
  print "Getting test page."
  r = s.getRevision('SandBox')
  if None != r:
    print r.raw
  else:
    print "Empty page."