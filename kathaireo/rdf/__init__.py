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
__version__ = "0.0.15-dev"

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

def suggest_and_load_files():
	"""Displays a list of *.rdf files in the current
	directory and lets choose one of those to be
	loaded into an rdf graph, which is then returned.

	Namespaces referenced in the chosen file are also
	loaded, parsed and put in separate graph instances.
	"""
	rdfFiles=[fn for fn in os.listdir('.') if fn.endswith(".rdf")]
	if len(rdfFiles)>0:
		print '\n'.join(["{}: {}".format(i,fn) 
			for i,fn in enumerate(rdfFiles)])
		c=int(raw_input(
			"Which one of these ontologies would"+
			" you like to be loaded? "))
		fn=rdfFiles[c]
		name = ''.join(fn.split(".rdf")[:-1])
		# create or retrieve graph id'd by filename 
		g = create_graph(name)
		load_into(rdfFiles[c], name)
		# download missing namespace sources
		ns.provide_for(g)
		return g


# returns a nicer output of this graph than he default
def repr_graph(g):
        """Returns a string representation of given graph
        indicating name and storage mode."""
	if g != None:
		return '<Graph "{}" with {} triples in store "{}">'.format(
			g.identifier, len(g), g.store.__class__.__name__)
	return '-'

# return graph identifier or null
def graph_name(g):
        """Return graph identifier or `'-'`."""
        if g != None:
                return g.identifier
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
def load_into(location, name=None):
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
	# TODO: also handle sql/sqlite?
	# TODO: handle n3!
	if name != None:
		if not name in _graphs:
			g = create_graph(name)
		else:
			g = _graphs.get(name)
	else:
		g = globals().get('current_graph')
	if g is None:
		return "!Oh no!: graph '{}' is null!".format(graph_name(g))
	else:
		if os.path.exists(location) and os.path.isfile(location):
			for mime in [None]+remote.mimetypes:
				try:
					g.parse(location, format=mime)
					return g
				except:
					pass
			return None
		else:
			# try to load from internet
			if remote.parse(g, location) is None:
				return None
		#print "parsed contents at {} into {}.".format(
			#location, g)
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
def import_ns(name):
	"""Downloads definitions of :mod:`.namespaces` used in the rdf
	graph identified by the given name. This is done by function
	:func:`.namespaces.provide_for`."""
	g = get_graph(name)
	if g:
		return ns.provide_for(g)
	return False


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
def save_xml(name, filename):
	"""Dumps rdf/xml to file.
	If no `graphname` parameter is passed, try to use
	:data:`current_graph` instead.
	"""
	if name:
		g = get_graph(name)
	else:
		g = __dict__.get(name)
	if g:
		return storage.save_xml(g, filename)
	return None

	
