#!/usr/bin/python
# -*- coding: utf-8 -*- 
"""\
Contains implementations of handler functions for 
standard commands in interactive shell mode.

Functions intended to serve as handlers, when declared
like `def func(*args, **kwargs)`, can be registered
using the `commands` module:

>>>	commands.register("create <graphname>", handler)
"""
__docformat__ = "restructuredtext en"
__version__ = "0.0.1-dev"


import rdf

# quit
def quit(*args, **kwargs):
	"""Simply calls `exit()`."""
	exit()


# return rdf graph
def create_graph(*args, **kwargs):
	"""\
	Creates a new `rdflib.Graph` instance going by
	the identifier passed as first argument.

	:Parameters:

		- `identifier`: Id for the new Graph

	:Returns:

		- The resulting `rdflib.Graph` instance when
		  successful, `None` otherwise.
	"""
	print args, kwargs
	if len(args)>0 and type(args[0]) is str:
		return rdf.create_graph(args[0])
	elif "graphname" in kwargs:
		return rdf.create_graph(kwargs.get("graphname"))
	else:
		print "Error: wrong number of arguments."


# load resource content into graph
def parse_rdf(*args, **kwargs):
	"""\
	Parses the resource at a given location and reads it into
	a `rdflib.Graph` identified by its name.

	:Parameters:

		- `location`: A String specifying the location of 
		  the resource to be read. Can be a path to a local
		  file or a URL.

		- `graphname`: A String identifying an `rdflib.Graph`
		  instance.

	:Returns:

		- `True`, if parsing was successful.
	"""
	location = kwargs.get('resource')
	name = kwargs.get('graphname')
	if None in [location, name]:
		if len(args)>1:
			location, name = args[:2]
	if not(None in [location, name]):
		return rdf.load_into(location, name)


# show info about given graph
def graph_info(*args, **kwargs):
	"""Display information about certain rdf graph.
	Possible keywords: size, ...
	"""
	field = kwargs.get('attribute')
	name = kwargs.get('graphname')
	if None in [field, name]:
		print "Error. Can't find attribute {} for graph {}".format(
			field, name)
	else:
		info = rdf.graph_info(name, field)
		print info
		return info



# download namespaces for given graph name
def import_namespaces(*args, **kwargs):
	"""Download namespaces for given graph name.
	"""
	name = kwargs.get('graphname')
	return rdf.import_ns(name)


# set sqlite resource as persistent store
def store_sqlite(*args, **kwargs):
	"""Set sqlite as store for graph."""
	name = kwargs.get('graphname')
	filename = kwargs.get('sqlite')
	return rdf.store_sqlite(name, filename)
	

def store_xml(*args, **kwargs):
	name = kwargs.get('graphname')
	filename = kwargs.get('filename')
	return rdf.save_xml(name, filename)

