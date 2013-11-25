#!/usr/bin/python
# -*- coding: utf-8 -*- 
"""\
Contains implementations of handler functions for 
standard commands in interactive shell mode.

Functions intended to serve as handlers, when declared
like ``def func(*args, **kwargs)``, can be registered
using the :mod:`.commands` module:
::

	>>> commands.register("create <graphname>", handler)

"""
__docformat__ = "restructuredtext en"
__version__ = "0.0.1a-dev"


from .. import rdf

# quit
def quit(*args, **kwargs):
	"""Simply calls :func:`exit`."""
	exit()


# return rdf graph
def create_graph(*args, **kwargs):
	"""\
	Creates a new :class:`.rdf.rdflib.Graph` instance going by
	the identifier passed as first argument.
	
	:param identifier: Id for the new Graph
	:returns: The resulting `rdflib.Graph` instance when 
		successful, `None` otherwise.
	
	"""
	if len(args)>0 and type(args[0]) is str:
		g = rdf.create_graph(args[0])
	elif "graphname" in kwargs:
		g = rdf.create_graph(kwargs.get("graphname"))
	else:
		return "!!Error!!: wrong number of arguments."
	if type(g) is str:
		return g
	return rdf.repr_graph(g)



# load resource content into graph
def parse_rdf(*args, **kwargs):
	"""\
	Parses the resource at a given location and reads it into
	a `rdflib.Graph` identified by its name.

	:param location: A String specifying the location of the 
		resource to be read. Can be a path to a local file or a URL.
	:param graphname: A String identifying an `rdflib.Graph` instance.
	:returns: `True`, if parsing was successful.
	"""
	location = kwargs.get('resource')
	name = kwargs.get('graphname')
	if None in [location, name]:
		if len(args)>1:
			location, name = args[:2]
	if not(None in [location, name]):
		if rdf.load_into(location, name) != None:
			g = rdf.get_graph(name)
			return 'Succesfully read {} rdf statements from {} into graph "{}".'.format(
				len(g), location, name)
		else:
			return '!Error!: Could not import resource at {}.'.format(location)


# show info about given graph
def graph_info(*args, **kwargs):
	"""Display information about certain rdf graph.
	Possible keywords: size, ...
	"""
	field = kwargs.get('attribute')
	name = kwargs.get('graphname')
	if None in [field, name]:
		return "!!Error!!. Can't find attribute {} for graph {}".format(
			field, name)
	else:
		info = rdf.graph_info(name, field)
		return info


# copy graph 
def cp_graph(*args, **kwargs):
	name1, name2 = args[:2]
	g1 = rdf.get_graph(name1)
	g2 = rdf.create_graph(name2)
	contents = g1.serialize(format='pretty-xml')
	g2.parse(data=contents)
	return ''.join([
		"Created copy of graph '{}' under the name '{}': ".format(
			name1, name2),
		rdf.repr_graph(g2),
		" with {} triples.".format(len(g2))])


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
	g, store = rdf.store_sqlite(name, filename)
	msg = rdf.repr_graph(g)+' at '+ store.configuration
	return msg + ' updated. Size: {}.'.format(len(g))


	

def store_xml(*args, **kwargs):
	"""Save contents of a graph to an `xml` file."""
	name = kwargs.get('graphname')
	filename = kwargs.get('filename')
	return rdf.save_xml(name, filename)

