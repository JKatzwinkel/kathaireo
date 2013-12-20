#!/usr/bin/python
# -*- coding: utf-8 -*-
"""\
Serves as some kind of facade for the rdflib_ library.
Mainly concerned with
just forwarding RDF operations to said backend, the :mod:`.rdf` module also
maintains additional session data; this allows to, say, have
RDF graphs looked up by their identifier, using the function :func:`.get_graph`
or have the :mod:`.namespaces` module download all namespaces for a certain graph by
calling :func:`.import_ns`.

.. _rdflib: https://github.com/RDFLib/rdflib
"""
__docformat__ = "restructuredtext en"
__version__ = "0.0.16c-dev"

import os
import rdflib
import re
import codecs

import namespaces as ns
import storage
import remote


# directory of existing rdflib.Graph instances, identified
# by name
_graphs={}

# TODO: directories of included classes/entities/properties like this?
# *included: per namespace/resource
# struct: {graphname: [term, term, ...], graphname: [...]}
_terms={}


#TODO: offer rdflib set operations using exact same syntax?
# (g1 + g2, g1 += g2, g1 & g2, ...)


################################################################
# reviewed/rewritten parts following
################################################################

# find graph known by name
def get_graph(name):
	"""Returns the graph identified by the given name, or `None`
	if no such graph is available."""
	return _graphs.get(name)


# return graph identifier as str or null
def graph_name(g):
	"""Return graph identifier or `'-'`."""
	if g != None:
		return str(g.identifier)
	return '-'



def set_graph(g):
	"""Sets the given rdf graph as the current default.
	When set, that graph will be the one operated on in interactive
	mode. This should cause input in which a ``<graphname>``
	value is omitted to work on said current default.
	:param g: new default graph. May be ``None``.
	:returns: status message."""
	globals()['current_graph'] = g
	if g is None:
		return 'Unset current graph'
	return u'Select graph: {}'.format(repr_graph(g))



# list all triples in graph
def ls(g=None):
	"""
	Returns a list of strings, each one representing one RDF triple of the given
	graph. Triple's URIs are substituted by their corresponding namespace-relative
	``ns:term`` `qualified name`_ identifiers as returned by
	``Graph.namespace_manager.qname``.
	.. _qualified name: http://www.w3.org/TR/1999/REC-xml-names-19990114/#NT-QName
	:param g: ``rdflib.Graph`` instance
	:returns: list of strings
	"""
	# TODO: this is a generic operation. make retrieval of default graph reusable
	if g is None:
		g = globals().get('current_graph')
	if g is None:
		return ['Error']
	# TODO: test, handle namespaces, handle urls
	res=[] # string list
	trp=[] # list of triples in str repr
	# FIXME: fails on invalid identifiers: with no base url
	# available, rdflib.split_uri throws exception. catch it!
	for triple in g:
		res.append([g.namespace_manager.qname(t) for t in triple])
	if len(trp)>0:
		clmwidths=[ # determine column widths
				max([len(triple[i]) for triple in trp]) for i in [0,1,2]]
		# align triple strings
		tmpl='{{:<{}}} {{:^{}}} {{:>{}}}'.format(*clmwidths)
		for triple in trp:
			res.append('{} {} {}'.format(*triple))
	return res



#################################################################
##################### below: parts to be reviewed ###############
#################################################################


# create and return new graph
def create_graph(name, store='default'):
	"""Returns a new `.rdflib.Graph` instance with the
	given identifier, if said identifier has not already
	been given to an existing graph."""
	# FIXME: if no graph selected so far, select newly created one
	if not name in _graphs:
		g = rdflib.Graph(store=store, identifier=name)
		_graphs[name] = g
		return g
	return "!Warning!: graph '{}' already exists.".format(name)


# returns a nicer output of this graph than he default
def repr_graph(g):
	"""Returns a string representation of given graph
	indicating name and storage mode."""
	if g != None:
		return '<Graph "{}" with {} triples in store "{}">'.format(
			str(g.identifier), len(g), g.store.__class__.__name__)
	return '-'








# import rdf data from resource into graph
def load_resource(location, name=None):
	"""Loads rdf graph at location (file/url) and names it.
	Reuses (overwrites?) an existing graph if one going by the given name
	is known, creates a new instance if not.
	Returns whatever graph instance the resource in question
	is being read into.
	If parsing fails, a new attempt is made using another mimetype
	(:data:`.remote.mimetypes`). If `location` does not seem to
	point to a local file, an attempt is made to start a download from that
	location via :func:`.remote.parse`.
	If everything fails, `None` is returned.
	"""
	# TODO: write smarter global namespace registry!
	# TODO: also handle sql/sqlite?
	# TODO: handle n3!
	# if a graphname is given, retrieve corresponding graph
	if name:
		g = get_graph(name)
		# if name is wrong/no graph is found, create one.
		if not g:
			g = create_graph(name)
	# if no name is given, operate on active graph selected by set_graph
	else:
		g = globals().get('current_graph')
	# if no graph could be found to load into, abort
		#return "!Oh no!: graph '{}' is null!".format(graph_name(g))
	# if graph is ready,
	# begin attempts to retrieve resource
	#TODO: we need better indication of function call results
	if g != None and isinstance(g, rdflib.Graph):
		#print 'importing into graph {}'.format(repr_graph(g))
		#TODO: make use of `publicID`: the logical URI to use as the document base.
		if os.path.exists(location) and os.path.isfile(location):
			#print 'resource appears to be a local file.'
			# if source is local file, try to autodetect format,
			# then suggest default mimetypes if that fails.
			for mime in [None]+remote.mimetypes[:3]:
				try:
					# call rdflib graph parse method
					#print 'apply format {} to file {}.'.format(mime, location)
					print 'parsing attempt using mimetype:', mime
					#f = codecs.open(location, encoding='utf-8', mode='rb')
					g = g.parse(location, format=mime)
					#f.close()
				except:
					pass
				if g:
					try:
						# register namespaces
						print 'register namespaces bound by graph'
						ns.reg_graph(g)
					except Exception as e:
						print e.message
						print e
					try:
						print 'populate namespace container with terms discovered in graph.'
						extract_ns_terms(g)
						return g
					except Exception as e:
						#print 'source apparently no {}.'.format(mime)
						print e.message
						print e
						pass
			# if none of the default formats could be recognized in
			# source, return None
			return None
		# if source is not a file on disk:
		else:
			# try to load from internet
			#print 'resource is no local file! download from {}.'.format(location)
			g = remote.parse(g, location)
			ns.reg_graph(g)
			extract_ns_terms(g)
		#print "parsed contents at {} into {}.".format(
			#location, g)
	# return graph resource content went in
	return g


# info output templates
rdfinfotempl={"size": "Number of statements in graph '{}': {}",
	"namespaces": "Graph '{}' binds the following namespaces:\n{}",
	"n3": "N3 representation of graph '{}' is {}",
	"types": "Types used in RDF graph '{}' are:\n{}",
	'xml': 'XML serialization of {}:\n{}'}
# show info
def graph_info(name, attr):
	"""Show info about specified graph.
	Info is available about: size, namespaces, ..."""
	if not name in _graphs:
		return "!!Failed!!: No graph {} known.".format(name)
	else:
		g = _graphs.get(name)
	if attr in rdfinfotempl:
		template = rdfinfotempl.get(attr)
		if attr == "size":
			return template.format(name, len(g))
		elif attr == "namespaces":
			return template.format(name,
				'\n'.join(['"{}": {}'.format(ns, ref)
				for ns,ref in g.namespaces()]))
		elif attr == "n3":
			return template.format(name, g.n3())
		elif attr == 'xml':
			return template.format(name, g.serialize())
		elif attr == "types":
			# TODO: maybe keep information like this globally in this module
			types = set()
			for s,o in g.subject_objects(rdflib.RDF.type):
				types.add(o)
			return template.format(name,
				'\n'.join([t for t in types]))
	else:
		return "!Failed!: Don't know attribute", attr


# import namespace definitions for graph
def import_ns(g):
	"""Downloads definitions of :mod:`.namespaces` used in the rdf
	specified graph. This is done by function
	:func:`.namespaces.provide_for`."""
	if g:
		res = ns.provide_for(g)
		if res:
			return res
		else:
			return '!!ERROR!! while downloading namespaces.'
	return False


# FIXME: rewrite this entirely, using rdflib methods and some
# brains this time
# TODO rdflib.Namespace, rdflib.NamespaceManager
# URIRef.n3(g.namespace_manager)
def bind_ns(g, name, url):
	"""Create new namespace binding."""
	if g is None:
		g = globals().get('current_graph')
	if not None in [g, name, url]:
		nns = ns.create(name, url)
		g.bind(name, rdflib.namespace.Namespace(url))
		return nns
	return '!Error!: could not bind new namespace.'



# TODO: lieber regexe?
# FIXME: we dont need this. rdflib
# URIRef.n3(g.namespace_manager)
def struct_uri(u):
	if '#' in u:
		url, term = u.rsplit('#',1)
	elif '/' in u:
		url, term = u.rsplit('/',1)
	else:
		url, term = u, None
	return (url, term)


# FIXME: we dont need this. rdflib
# URIRef.n3(g.namespace_manager)
def shorten_url(url):
	"""Shortens a given url by collapsing it to a pair
	of identifiers denoting namespace and term, like
	``rdfs:label``."""
	#TODO: impl
	base, term = struct_uri(url)
	nspc = ns.get_ns(base)
	if nspc:
		return '{}:{}'.format(nspc.name, term)
	# TODO: if no namespace is present, shorten shomehow else
	return url

# FIXME: we dont need this. rdflib
def expand_term(token):
	"""Un-shorten url."""
	nn, term = token.rsplit(':',1)
	nsp = ns.get(nn)
	if nsp:
		return rdflib.URIRef('{}{}'.format(nsp.url, term))
	return rdflib.URIRef(token)



#harvest namespace terms from graph
def extract_ns_terms(g):
	"""Collects terms from graph rdf and assigns them
	to the namespaces they come from."""
	# TODO: filtern, so dasz einzelne namespaces bearbeitet weden
	# koennen; self.rdf in namespace klasse damit befuellen.
	for t in g:
		for u in t:
			if u:
				url, term = struct_uri(u)
				if term:
					nsp = ns.get_ns(url)
					if nsp:
						#print '\n\nextract namespace term from rdf data:',
						#print '{}..{}'.format(url[:10],url[-10:]), nsp.name, term
						dest = [nsp.classes, nsp.properties][int(term.islower())]
						if not term in dest:
							dest.append(term)

# TODO: we dont need this. rdflib
# URIRef.n3(...)
def ls_rdf(g=None):
	"""Returns rdf content of graph line by line as tuples."""
	if not g:
		g = globals().get('current_graph')
	if g:
		stms = []
		for trp in g:
			stm = ()
			for t in trp:
				if re.match('^((?:\S*\"[^"]+\")+|\S+)$', t):
					stm += (t,)
				else:
					stm += (u'"{}"'.format(t),)
			stms.append(stm)
		return stms




# TODO: check out rdflib.
# FIXME: either use slicing: g[:foaf.knows]
# or functions like g.subject_objects(pred), ...
def find_term(term, nsp=None, g=None):
	"""Shows triple containing given term."""
	if not g:
		g = globals().get('current_graph')
	if g:
		res = []
		if nsp != None and nsp in ns.get_names():
			res.extend(['Search for occurences of resouce id {}:{} in {}'.format(
				ns.get(nsp).name, term, graph_name(g))])
			prefix = ns.get(nsp).url
			nsp = None
		else:
			prefix = '\S*'
		pttn = '{}[#/]?{}'.format(prefix, term)
		query = re.compile(pttn)
		#print query.pattern
		# substitution string for query matches
		if nsp:
			if term:
				subst = u'*{}:{}*'.format(nsp,term)
			else:
				subst = u'*{}*'.format(nsp)
		else:
			subst = u'*:{}*'.format(term)
		# serach through triple list
		for trp in ls_rdf(g=g):
			stm = u'{} {} {}'.format(*trp)
			#if stm.find('Glenys Stacey') > 0:
				#print stm
				#res.append(stm)
			# occurence of desired ref entity?
			occ = query.findall(stm)
			if len(occ)>0:
				for o in occ:
					stm = re.sub(pttn, subst, stm)
				res.append(stm)
		return res




# attach sqlite store
def store_sqlite(name, filename):
	"""Store. Sqlite. database. Uses the :mod:`.storage` module.
	Overwites graph referenced by `name`.
	"""
	#g = get_graph(name)
	#if g:
	store = storage.sqlite(filename)
	g = rdflib.Graph(store, name)
	g.open(store.configuration)
	_graphs[name] = g
	return (g, store)


# save xml dump
def save_xml(g, filename):
	"""Dumps rdf/xml to file.
	If no `graphname` parameter is passed, try to use
	:data:`current_graph` instead.
	"""
	if g:
		return storage.save_xml(g, filename)
	return None


