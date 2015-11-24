#!/usr/bin/python
# -*- coding: utf-8 -*-
"""\
This module tries to download rdf contents from places remote
from the hard disk of the machine we're running on.
"""
__docformat__ = "restructuredtext en"
__version__ = "0.0.1b-dev"

import urllib.request as urllib2

mimetypes = ['application/rdf+xml', 'text/n3', 'text/turtle',
	'application/n-triples','application/x-trig', 'text/owl-functional']
"""List of mimetypes used for parsing of resources whose rdf format can't
be detected automatically."""
# oha: http://www.w3.org/TR/owl2-syntax/

# attempts to parse rdf resource at a certain location
# by first downloading and then parsing it offline
def parse(g, location, format=None, guesses=mimetypes[:3]):
	"""\
	Attempts to parse an RDF resource at a certain location
	by first downloading and then parsing it offline.
	Choice of parsing implementation depends on `format`
	parameter; By default, source format autodetection is
	applied, followed by a few attempts on forcing
	specific format parsers to process the source, determined
	by frequent mimetypes listed in :data:`.mimetypes`.

	Whilst this behaviour will handle RDF sources reliably
	in most cases, the episode of wild guessing beginning
	whenever autodetection fails can cause a serious delay.
	Passing `guesses=None` mitigates this inefficiency,
	but possibly with the downside of parsing failure at
	common RDF expression formats.

	:param g: Graph to write content to
	:param location: URL of remote RDF source.
	:param format: string identifying a specific format which
		the resource is expected to express its RDF contents in.
		Default is `None`, getting the parser to autodetect
		the source's format, which goes well in most cases.
		If autodetection is likely to err, one can pass
		a mimetype like those in :data:`.mimetypes`, but no
		promise can be made that a correct format parameter
		will lead to parsing success.
	:param guesses: List of mimetypes used for wild guessing
		of the input format in case autodetection fails. Set to
		`None` in order to trade time for chance.
	"""
	#print 'parse remote resource {} into graph {}.'.format(location, g)
	# connect to URL
	try:
		conne = urllib2.urlopen(location)
	except Exception as e:
		if 'Errno -2' in '{}'.format(e):
			# netz nicht erreichbar
			print('Can\'t get {}: network unreachable!'.format(location))
		else:
			print('Can\'t get {}.'.format(location))
		return None

	# print conne.headers.dict
	# download content
	content = conne.read()
	try:
		# try to parse source as specified format
		# or more likely autodetecting format
		g = g.parse(data=content, format=format)
		return g
	except:
		# if (autodetect) parsing fails,
		# try again a few times, guessing the right format
		if len(guesses)>0:
			if format in guesses:
				guesses.remove(format)
			for mime in guesses:
				try:
					# try to parse for specified format and return
					# graph on success
					g = g.parse(data=content, format=mime)
					return g
				except:
					# output debug msg
					print('mimetype {} failed.'.format(mime))
		# if nothing worked at all, return None
		return None


# status internet
def is_internet_available():
	"""Tries to establish socket towards google dns server."""
	try:
		response = urllib2.socket.gethostbyaddr('8.8.8.8')
		if 'google.com' in response[0]:
			return True
		print(response)
		return False
	except:
		return False


# try to determine if internet connection is available
web_access=is_internet_available()
