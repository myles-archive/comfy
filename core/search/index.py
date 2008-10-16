import logging
import os
import sys

from django.conf import settings
import simplejson
import xapian

db = settings.COUCHDB

log = logging.getLogger(__name__)

class Index(object):
	def __init__(self, dir):
		log.info("Creating indexer")
		self.idxfile = os.path.join(dir, '%s.idx' % settings.COUCHDB_DATABASE)
		self.xdb = xapian.WritableDatabase(self.idxfile, xapian.DB_CREATE_OR_OPEN)
		self.index = xapian.TermGenerator()
		self.index.set_stemmer(xapian.Stem("english"))
		self.startkey = self.xdb.get_metadata("startkey")
		if self.startkey:
			self.startkey = simplejson.loads(self.startkey)
		self.batch_size = 1000
	
	def reindex(self):
		log.info("Reindexing")
		try:
			self.xdb.begin_transaction()
			params = { 'count': self.batch_size }
			if self.startkey:
				params['startkey'] = self.startkey
			docs = db.view('_all_docs_by_seq', **params)
			while len(docs) > 0:
				for doc in docs:
					self.startkey = doc.key
					xuid = "COUCHDB_ID_%s" % doc.id
					if doc.value.get('deleted', False):
						self.xdb.delete_document(doc.id)
					else:
						cdoc = db[doc.id]
						xdoc = xapian.Document()
						xdoc.add_term(xuid)
						xdoc.set_data(doc.id)
						self.index.set_document(xdoc)
						self.index.index_text(' '.join(map(lambda x: str(cdoc.get(x, '')), [k for k in cdoc])))
						self.xdb.replace_document(xuid, xdoc)
				params['startkey'] = self.startkey
				docs = db.view('_all_docs_by_seq', **params)
			self.xdb.set_metadata("startkey", simplejson.dumps(self.startkey))
			self.xdb.commit_transaction()
		except:
			self.xdb.cancel_transaction()
			raise
