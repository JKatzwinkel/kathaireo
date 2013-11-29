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
__version__ = "0.0.9-dev"


import re

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
	
	handles:
	`create <graphname>`
	"""
	if "graphname" in kwargs:
		g = rdf.create_graph(kwargs.get("graphname"))
	else:
		return "!!Error!!: Wrong number of arguments: {}.".format(
			len(args))
	if type(g) is str:
		return g
	return rdf.repr_graph(g)


# select graph to work on
def set_graph(*args, **kwargs):
        """Select default graph for rdf operations.
        handles:
        `use <graphname>`"""
        name = kwargs.get('graphname')
        if name:
                g = rdf.get_graph(name)
                if g != None:
                        return rdf.set_graph(g)
                else:
                        return '!Fail:! No graph "{}"!'.format(name)
        else:
                return '!!Error!!: No graph specified.'


# return list of graph registry entry str reprs.
def show_graphs(*args, **kwargs):
	"""Returns a list of strings representing all 
	graph instances currently registered.
	handles:
	`show graphs`
	`list`
	`ls`"""
	reg = rdf._graphs.items()
	print rdf._graphs
	return ['{}: {}'.format(name, rdf.repr_graph(g)) for
		name, g in sorted(reg, key=lambda t:t[0])]



# load resource content into graph
def parse_rdf(*args, **kwargs):
	"""\
	Parses the resource at a given location and reads it into
	a `rdflib.Graph` identified by its name.

	:param location: A String specifying the location of the 
		resource to be read. Can be a path to a local file or a URL.
	:param graphname: A String identifying an `rdflib.Graph` instance.
	:returns: `True`, if parsing was successful.

	handles:
	`load <resource>`
	"""
	location = kwargs.get('resource')
	name = kwargs.get('graphname')
	if None in [location, name]:
		if len(args)>1:
			location, name = args[:2]
		#else:
			#name = rdf.graph_name(rdf.current_graph)
	# FIXME: why does this lead to an additional graph instance with a 
	# rdflib.RDFUriRef identifier????
	#if not(None in [location, name]):
	if location:
		# try to parse local file first,
		# then remote source on failure.
		# try for multiple rdf formats in both
		g = rdf.load_resource(location, name=name)
		if g:
			# return success indicator msg
			return 'Succesfully read {} rdf statements from {} into graph "{}".'.format(
				len(g), location, name)
		else:
			# if parse attempt failed,
			# return failure msg
			return '!Error!: Could not import resource at {}.'.format(location)
	# if no location was given
	# return failure msg
	return "!Didn't read source:! No location specified."


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
	"""Create new graph by given name and clone contents
	of another graph into it.
	handles:
	`cp <graphname> <graphname>`
	`cp <graphname>`"""
	# use parameters
	if len(args) == 2:
		name1, name2 = args[:2]
		g1 = rdf.get_graph(name1)
		g1, g2 = [rdf.get_graph(n) for n in args[:2]]
	elif len(args) == 1:
		g1 = rdf.current_graph
		name2 = kwargs.get('graphname')
		g2 = rdf.get_graph(name2)
	else:
		return '!!Error!!: Parameter count mismatch ({}).'.format(
			len(args))
	# do copying
	if not g2:
		g2 = rdf.create_graph(name2)
	else:
		return "!Didn't copy!: Graph {} exists. Delete it first.".format(name2)
	if not None in [g1, g2]:
		contents = g1.serialize(format='pretty-xml')
		g2.parse(data=contents)
		return ''.join([
			"Created copy of graph '{}' under name '{}' ".format(
				rdf.graph_name(g1), name2),
			" with {} triples.".format(len(g2)),
			'\n{}'.format(rdf.repr_graph(g2))])
	else:
		return "!!Error!!: Couldn't copy graph '{}' to name '{}'!".format(
			rdf.graph_name(g1), name2)

# insert one graph into another
def merge_graph(*args, **kwargs):
	"""merge graph into :data:`.rdf.current_graph`.
	handles:
	`merge <graphname>`
	`insert <graphname> into <graphname>`"""
	if len(args) > 0:
		# currently selected graph, command probably was merge
		if len(args) < 2:
			g = rdf.current_graph
			name = kwargs.get('graphname')
			if name:
				# graph specified by parameter
				g2 = rdf.get_graph(name)
		# two specified graphs, command probably was insert
		else: 
			g2, g = [rdf.get_graph(n) for n in args[:2]]
		# in case of wrong graphname(s), print warning.
		if None in [g,g2]:
			for g in [g for g in [g, g2] if g is None]:
				msg = 'Could not find graph "{}"'.format(name)
		else:
			# actual merge:
			# copy triples from g2 into currently active graph
			for triple in g2:
				g.add(triple)
			# TODO: merge namespaces as well!
			return 'Merged {} triples from {} into {}, resulting in {}.'.format(
				len(g2), g2.identifier, g.identifier, len(g))
	# not enough parameters?
	else:
		msg = 'Parameter count mismatch ({}).'.format(len(args))
	return "!Couldn't merge graphs!: {}".format(msg)



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


# Returns a list of `command` syntax specifications
# in docstring of a function identified by their name.
def extract_cmd_syntax(fname):
	"""Extract command syntax definition from handler function
	docstring.
	:param fname: the function's name. Expected to be known by
	this (:mod:`.`) module, either because the function's 
	implementation in the module source code anyway, or due
	to previous calls of :func:`.commands.register_handler`
	invoked by the ``@cmd_handler`` decorator."""
	func = globals().get(fname)
	if func != None:
		res = []
        # command syntax extraction from __doc__
        fdoc = func.func_doc
        if fdoc:
	        for line in fdoc.split('\n'):
	        	sntxs = re.findall('^\s*`([^`]+)`', line)
	        	res.extend(sntxs)
        return res


