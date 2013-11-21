#!/usr/bin/python
# -*- coding: utf-8 -*- 
import os
import rdflib
#from rdflib_sqlalchemy.SQLAlchemy import SQLAlchemy

import namespaces as ns


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


def create_graph(name):
	"""Returns a new `rdflib.Graph` instance with the
	given identifier, if said identifier has not already
	been given to an existing graph."""
	print "attempting to create new graph with name", name
	if not name in _graphs:
		g = rdflib.Graph(identifier=name)
		_graphs[name] = g
		print g
		return g
	print "graph {} already existing!".format(name)


def get_graph(name):
	"""Returns the graph identified by the given name, or `None`
	if no such graph is available."""
	return _graphs.get(name)


def load_into(location, name):
	"""Loads rdf graph at location (file/url) and names it.
	Reuses (overwrites?) an existing graph if one going by the given name
	is known, creates a new instance if not.
	Returns whatever graph instance the resource in question
	is being read into.
	If parsing fails, exceptions are not being handled here.
	"""
	if not name in _graphs:
		g = create_graph(name)
	else:
		g = _graphs.get(name)
	if g is None:
		print "graph '{}' is null!".format(name)
	else:
		g.parse(location)
		print "parsed contents at {} into {}.".format(
			location, g)
	return g


# info output templates
rdfinfotempl={"size": "Number of statements in graph {}: {}"}
# show info
def graph_info(name, attr):
	"""Show info about specified graph.
	Info is available about: size, source, ..."""
	if not name in _graphs:
		return "Failed: No graph {} known.".format(name)
	else:
		g = _graphs.get(name)
	if attr in rdfinfotempl:
		template = rdfinfotempl.get(attr)
		if attr == "size":
			return template.format(name, len(g))
	else:
		return "Failed: Don't know attribute", attr
