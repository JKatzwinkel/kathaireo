#!/usr/bin/python
# -*- coding: utf-8 -*- 
"""\
This module tries to download rdf contents from places remote
from the hard disk of the machine we're running on.
"""
__docformat__ = "restructuredtext en"
__version__ = "0.0.1-dev"

import urllib2

mimetypes = ['application/rdf+xml', 'text/n3', 'application/n-triples',
	'text/turtle', 'application/x-trig', 'text/owl-functional']
"""List of mimetypes used for parsing of resources whose rdf format can't
be detected automatically."""
# oha: http://www.w3.org/TR/owl2-syntax/

# attempts to parse rdf resource at a certain location
# by first downloading and then parsing it offline
def parse(g, location, format=None):
	"""attempts to parse rdf resource at a certain location
	by first downloading and then parsing it offline."""
	conne = urllib2.urlopen(location)
	print conne.headers.dict
	content = conne.read()
	try:
		g.parse(data=content)
	except:
		for mime in mimetypes:
			try:
				g.parse(data=content, format=mime)
				return g
			except:
				print 'mimetype {} failed.'.format(mime)
		return None
