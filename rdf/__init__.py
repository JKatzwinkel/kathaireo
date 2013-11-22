#!/usr/bin/python
# -*- coding: utf-8 -*- 
"""\
Doku doku doku
"""
__docformat__ = "restructuredtext en"
__version__ = "0.0.1-dev"

import os
import rdflib
#from rdflib_sqlalchemy.SQLAlchemy import SQLAlchemy

import namespaces as ns
import storage

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
	if g != None:
		return '<Graph "{}"; stored in "{}">'.format(
			g.identifier, g.store.__class__.__name__)
	return '!nullgraph!'


# create and return new graph
def create_graph(name):
	"""Returns a new `rdflib.Graph` instance with the
	given identifier, if said identifier has not already
	been given to an existing graph."""
	#print "attempting to create new graph with name", name
	if not name in _graphs:
		g = rdflib.Graph(identifier=name)
		_graphs[name] = g
		#print g
		return g
	return "graph {} already exists.".format(name)


# find graph known by name
def get_graph(name):
	"""Returns the graph identified by the given name, or `None`
	if no such graph is available."""
	return _graphs.get(name)


# import rdf data from resource into graph
def load_into(location, name):
	"""Loads rdf graph at location (file/url) and names it.
	Reuses (overwrites?) an existing graph if one going by the given name
	is known, creates a new instance if not.
	Returns whatever graph instance the resource in question
	is being read into.
	If parsing fails, exceptions are not being handled here.
	"""
	# TODO: also handle sql/sqlite?
	# TODO: handle n3!
	if not name in _graphs:
		g = create_graph(name)
	else:
		g = _graphs.get(name)
	if g is None:
		return "graph '{}' is null!".format(name)
	else:
		g.parse(location)
		#print "parsed contents at {} into {}.".format(
			#location, g)
	return g


# info output templates
rdfinfotempl={"size": "Number of statements in graph '{}': {}",
	"namespaces": "Graph '{}'' binds the following namespaces:\n{}",
	"n3": "N3 representation of graph '{}'' is {}",
	"types": "Types used in RDF graph '{}'' are:\n{}"}
# show info
def graph_info(name, attr):
	"""Show info about specified graph.
	Info is available about: size, namespaces, ..."""
	if not name in _graphs:
		return "Failed: No graph {} known.".format(name)
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
		return "Failed: Don't know attribute", attr


# import namespace definitions for graph
def import_ns(name):
	"""Downloads definitions of namespaces used in the rdf
	graph identified by the given name."""
	g = get_graph(name)
	if g:
		return ns.provide_for(g)
	return False


# attach sqlite store
def store_sqlite(name, filename):
	"""Store. Sqlite. database.
	"""
	#g = get_graph(name)
	#if g:
	store = storage.sqlite(filename)
	g = rdflib.Graph(store, name)
	g.store.open(store.configuration)
	_graphs[name] = g
	return (g, store)


# save xml dump
def save_xml(name, filename):
	"""Dumps rdf/xml to file.
	"""
	g = get_graph(name)
	if g:
		return storage.save_xml(g, filename)
	return None

	
