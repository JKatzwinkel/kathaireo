#!/usr/bin/python
# -*- coding: utf-8 -*- 
"""\
This module tries to download rdf contents from places remote
from the hard disk of the machine we're running on.
"""
__docformat__ = "restructuredtext en"
__version__ = "0.0.1-dev"

import urllib2

# attempts to parse rdf resource at a certain location
# by first downloading and then parsing it offline
def parse(g, location, format='application/rdf+xml'):
	conne = urllib2.urlopen(location)
	print conne.headers.dict
	content = conne.read()
	g.parse(data=content, format=format)
