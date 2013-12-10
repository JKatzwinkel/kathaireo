#!/usr/bin/python
# -*- coding: utf-8 -*- 
import os
import rdflib

from . import remote
from ..util import log

# TODO: write smarter global namespace registry!
_namespaces={}
"""Directory of instantiated namespaces."""
_prefixes={}
"""Directory of namespace names, filed under their url."""

# namespace class serving as a rdflib graph container
class Namespace:
	"""Dokudoku"""
	def __init__(self, name, url):
		self.name = name
		self.url = u'{}'.format(url)
		self.classes = []
		self.properties = []
		#print 'instantiate namespace {} at {}!'.format(name, url)
		self.rdf = rdflib.Graph(identifier=name)
		# try to load namespace source
		#self.rdf.parse(self.url)
		try:
			remote.parse(self.rdf, self.url, guesses=[])
			# Part of speech stuff
			for s,p,o in self.rdf:
				if s.startswith(self.url):
					if o.endswith("Property"):
						self.properties.append(str(s))
					else:
						self.classes.append(str(s))
			self.properties = list(set(self.properties))
			self.classes = [i for i in set(self.classes) 
											if not i in self.properties] # TODO
		except:
			pass
		#_namespaces[name] = self

	def __repr__(self):
		return u"<namespace '{}' at {}>: {} triples".format(
			self.name, self.url, len(self.rdf))





# parse source of given namespace
def load(name, url):
	"""Downloads a namespace resource at given url and
	embeds its contents into a new `Namespace` instance."""
	# TODO: write smarter global namespace registry!
	try:
		ns = _namespaces.get(name)
		if not ns:
			ns = Namespace(name, url)
		return ns #TODO: overwrite url?
	except Exception as e:
		print e
		return None


def create(name, url):
	"""Creates and registers new namespace."""
	ns = load(name, str(url))
	if ns:
		_namespaces[name] = ns
		_prefixes[str(url).rstrip('/#')] = ns
		return ns
	return None



def get_ns(url):
	"""Looks up ns name for given url."""
	#print '\n'.join(_prefixes.keys())
	log('Look up ns for {}.'.format(url))
	res = None
	i = 0
	while res is None and i < 5:
		res = _prefixes.get(url)
		if res:
			#print '\tfound namespace!', '{}..{}'.format(url[:20],url[-10:]), res.name
			break
		if i < 3:
			url = url[:-1]
		else:
			url = url.rsplit('/',1)[0]
		i += 1
	if res:
		log('Found namespace: {}! ({})'.format(res.name, res.url[-10:]))
	else:
		log('No namespace found.')
	return res


# register namespaces bound by graph
def reg_graph(g):
	"""Copies a graph's collection of namespaces to the
	:mod"`.namespaces` module, so that all namespaces bound
	by loaded graphs are stored at a common location.
	"""
	if g:
		rdfns = {ns:load(ns,str(url)) for ns, url in g.namespaces() 
			if not ns in _namespaces}
		# insert namespace directory into global registry
		_namespaces.update(rdfns)
		# cross file names under urls
		prfxs = {unicode(url).rstrip('/#'):get(n) 
						for n, url in g.namespaces()}
		_prefixes.update(prfxs)
		# copy namespace references to module variable namespace
		#globals().update(rdfns)



# download namespaces referenced by given rdf ontology
def provide_for(ontology):
	"""Imports definitions of namespaces a given graph is using."""
	#load referenced namespaces
	# TODO: write smarter global namespace registry!
	rdfns = [load(ns, str(ref)) for ns, ref in ontology.namespaces()]
	# filter
	ns = [n for n in rdfns if n]
	ns = {n.name:n for n in ns if not n.name in _namespaces}
	_namespaces.update(ns)
	# copy ns pointers to module global variable namespace
	#globals().update(ns)
	#print "Namespaces:\n--------------"
	#print "\n".join(["{}".format(n) for n in _namespaces.values()])
	return ns


# list known namespace names
def get_names():
	return sorted(_namespaces.keys())


# list known namespaces
def spaces():
	return [_namespaces[n] for n in 
		sorted(_namespaces.keys())]


def get(name):
	return _namespaces.get(name)




_namespaces['rdf'] = Namespace('rdf', 
	'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
_namespaces.get('rdf').properties.extend(['type'])
_namespaces.get('rdf').classes.extend(['Property', 'Class'])

_namespaces['rdfs'] = Namespace('rdfs', 
	'http://www.w3.org/2000/01/rdf-schema#')
_namespaces.get('rdfs').properties.extend(['domain', 'range', 
	'label', 'comment', 'subClassOf'])
_namespaces.get('rdfs').classes.extend([])

_namespaces['owl'] = Namespace('owl', 'http://www.w3.org/2002/07/owl#')
_namespaces.get('owl').properties.extend(['equivalentClass',
	'disjointWith'])
_namespaces.get('owl').classes.extend(['Thing', 'Class', 'Ontology'])

