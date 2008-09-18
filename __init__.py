VERSION = (0, 1, 'pre-alpha')

def get_version():
	v = '.'.join([str(i) for i in VERSION[:-1]])
	return v