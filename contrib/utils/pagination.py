class Pagination(object):
	"""
	This is the starting of some work on a Pagination utility.
	"""
	def __init__(self, results, per_page, page, endpoint):
		super(Pagination, self).__init__()
		self.results = results
		self.per_page = per_page
		self.page = page
		self.endpoint = endpoint
	
	def count(self):
		return len(self.results)
	
	def entries(self):
		return self.results[((self.page - 1) * self.per_page):(((self.page - 1) * self.per_page) + self.per_page)]
	
	has_previous = property(lambda x: x.page > 1)
	has_next = property(lambda x: x.page < x.pages)
	previous = property(lambda x: url_for(x.endpoint, page=x.page - 1))
	next = property(lambda x: url_for(x.endpoint, page=x.page + 1))
	pages = property(lambda x: max(0, x.count - 1) // x.per_page + 1)
