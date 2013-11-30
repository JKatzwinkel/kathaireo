#!/usr/bin/python
# -*- coding: utf-8 -*- 
"""\
Serves as some kind of a facade for the 'rdflib' library. In addition to
just forwarding rdf operations to the library, the :mod:`.rdf` module also
maintains some useful directories and registers; this allows to, say, have
rdf graphs looked up by their identifier, using the function :func:`.get_graph`
or have the :mod:`.namespaces` module download all namespaces for a certain graph by
calling :func:`.import_ns`.
"""
__docformat__ = "restructuredtext en"
__version__ = "0.0.16c-dev"

import os
import rdflib
#from rdflib_sqlalchemy.SQLAlchemy import SQLAlchemy

import namespaces as ns
import storage
import remote

#store = SQLAlchemy(configuration="sqlite:///newspapers.sqlite")
#g = rdflib.Graph(store, "newspapers")

#print "Trying to load graph {} from store {}.".format(

# directory of existing rdflib.Graph instances, identified
# by name
_graphs={}


# returns a nicer output of this graph than he default
def repr_graph(g):
	"""Returns a string representation of given graph
	indicating name and storage mode."""
	if g != None:
		return '<Graph "{}" with {} triples in store "{}">'.format(
			str(g.identifier), len(g), g.store.__class__.__name__)
	return '-'


# return graph identifier as str or null
def graph_name(g):
	"""Return graph identifier or `'-'`."""
	if g != None:
		return str(g.identifier)
	return '-'


# create and return new graph
def create_graph(name, store='default'):
	"""Returns a new `.rdflib.Graph` instance with the
	given identifier, if said identifier has not already
	been given to an existing graph."""
	#print "attempting to create new graph with name", name
	if not name in _graphs:
		g = rdflib.Graph(store=store, identifier=name)
		_graphs[name] = g
		#print g
		return g
	return "!Warning!: graph '{}' already exists.".format(name)


# find graph known by name
def get_graph(name):
	"""Returns the graph identified by the given name, or `None`
	if no such graph is available."""
	return _graphs.get(name)


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
	return 'Select graph: {}'.format(repr_graph(g))


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
	if g != None and isinstance(g, rdflib.Graph):
		#print 'importing into graph {}'.format(repr_graph(g))
		if os.path.exists(location) and os.path.isfile(location):
			#print 'resource appears to be a local file.'
			# if source is local file, try to autodetect format,
			# then suggest default mimetypes if that fails.
			for mime in [None]+remote.mimetypes[:3]:
				try:
					# call rdflib graph parse method
					#print 'apply format {} to file {}.'.format(mime, location)
					g = g.parse(location, format=mime)
					# register namespaces
					ns.reg_graph(g)
					extract_ns_terms(g)
					return g
				except:
					#print 'source apparently no {}.'.format(mime)
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
		#print "parsed contents at {} into {}.".format(
			#location, g)
	# return graph resource content went in
	return g


# info output templates
rdfinfotempl={"size": "Number of statements in graph '{}': {}",
	"namespaces": "Graph '{}' binds the following namespaces:\n{}",
	"n3": "N3 representation of graph '{}' is {}",
	"types": "Types used in RDF graph '{}' are:\n{}"}
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


#harvest namespace terms from graph
def extract_ns_terms(g):
	"""Collects terms from graph rdf and assigns them
	to the namespaces they come from."""
	for t in g:
		for u in t:
			if u:
				if '#' in u:
					url, term = str(u).rsplit('#',1)
				elif '/' in u:
					url, term = str(u).rsplit('/',1)
				else:
					term = None
				if term:
					nsp = ns.get_ns(url)
					if nsp:
						print url, nsp.name, term
						dest = [nsp.classes, nsp.properties][int(term.islower())]
						if not term in dest:
							dest.append(term)





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

	
