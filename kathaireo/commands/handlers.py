#!/usr/bin/python
# -*- coding: utf-8 -*-
"""\
Contains implementations of handler functions for
standard commands in interactive shell mode.

Functions intended to serve as handlers, when declared
like ``def func(*args, **kwargs)``, can be registered
using the :mod:`.commands` module:
::

	>>> commands.register("create <graph>", handler)

"""
__docformat__ = "restructuredtext en"
__version__ = "0.0.92-dev"


import re

from .. import rdf

###############################################################
#################          stuff            ###################
###############################################################

# Returns a list of `command` syntax specifications
# in docstring of a function identified by their name.
def extract_cmd_syntax(fname):
	"""Extract command syntax definition from handler function
	docstring. The resulting syntax list is used
	by :func:`.commands.init` and :func:`.commands.register_handler`,
	for calls of :func:`.commands.register`.
	:param fname: the function's name. Expected to be known by
	this (:mod:`.`) module, either because the function's
	implementation in the module source code anyway, or due
	to previous calls of :func:`.commands.register_handler`
	invoked by the ``@cmd_handler`` decorator."""
	#NOTE: this is a very good feature, just to say sth positive..
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


# retrieve standard stuff like <graph>
def res_arg(**kwargs):
	"""
	Takes a kwargs dict from any handler and does whatever is possible
	to replace argument placeholder type identifiers by appropriate
	values. For instance: an argument <graph> should be resolved
	so that the actual RDF graph instance identified by the given name
	is returned, or at least the currently selected default graph or
	an error message instead.
	"""
	#TODO: unfortunately, I didnt think this through.
	#TODO: this thing could end up causing more work than it can even
	#TODO save from. For instance: If <graph> reification fails,
	#TODO: what are we gonna return instead? a nullpointer, so that calling
	#TODO: handlers have no way left to craft proper error messages? or
	#TODO: just return the original graphname string, so that handler has to
	#TODO: check the parameter type before being halfway save using it?
	#TODO: We might actually be better off having seperate arg resv functions
	#TODO: for every single argument in use (which on its part will make argument
	#TODO: declaration much worse...). Handlers then can individually ask
	#TODO: for resolution of single argument value fields.
	# resolve <graph> arg
	name = kwargs.get('graphname')
	if name:
		g = rdf.get_graph(name)
	else:
		g = rdf.__dict__.get('current_graph')
	kwargs['graphname'] = g
	# return kwargs dict with arg names resolved to objects
	# unpacked as collection of positional parameters
	return kwargs


###############################################################
###############################################################
###############################################################
###################       handlers           ##################
###############################################################
###############################################################
###############################################################

# FIXME: every single handler expecting a <graph> argument
# reinvents the same retrievals and error checkings. Might argument
# resolving be better off at commands.execute or somewhere in commands.arguments?
# FIXME: at least write some default arg resolv functions in here,
# reusable by similar commands.

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
	`create <graph>`
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
	`use <graph>`"""
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
	# perform standard arg resv operations, like reifying graph from graphname
	# TODO: maybe this should even be called beforehand, by the commands parser
	# TODO: that way, we could already have an actual parameter variable 'graph',
	# TODO: pointing to an actual graph instance and available in this very
	# local namespace!
	kwargs = res_args(**kwargs)
	location = kwargs.get('resource')
	g = kwargs.get('graphname')
	#name = kwargs.get('graphname')
	if None in [location, g]:
		if len(args)>1:
			location, name = args[:2]
			# FIXME: processing *args list should be left to functions
			# that expect more than one value for the same argument name...
			if name:
				g = rdf.get_graph(name)
			if not g:
				return '!Failed! to address RDF graph!'
		#else:
			#name = rdf.graph_name(rdf.current_graph)
	# FIXME: why does this lead to an additional graph instance with a
	# rdflib.RDFUriRef identifier????
	#if not(None in [location, name]):
	if location:
		before = 0
		# try to parse local file first,
		# then remote source on failure.
		# try for multiple rdf formats in both
		if g:
			before = len(g)
		# do the stuff!
		g = rdf.load_resource(location, name=name)
		if g:
			# return success indicator msg
			# if no graph is selected, use this one
			if rdf.__dict__.get('current_graph') is None:
				rdf.set_graph(g)
			return u'Succesfully read {} rdf statements from {} into graph "{}".'.format(
				len(g)-before, location, name)
		else:
			# if parse attempt failed,
			# return failure msg
			return u'!Error!: Could not import resource at {}; operation returned "None"!'.format(location)
	# if no location was given
	# return failure msg
	return u"!Didn't read source:! No location specified."


# show info about given graph
#FIXME: this was nice as a lorem ipsum interaction dummy, but seriously...
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


# list namespaces of single namespace infos
def show_ns(*args, **kwargs):
	"""List loaded namespaces.
	handles:
	`ls ns`
	`list namespaces`
	`ls ns <namespace>`
	ls ns <graph>""" # TODO: make sure this works!
	# TODO: write smarter global namespace registry!
	#FIXME: we can keep a directory of namespaces and which graphs bind them,
	#but apart from that, namespace managing should be left to rdflib namespace
	#manager!!
	head = 'currently bound namespaces:'
	if not 'namespace' in kwargs:
		g = rdf.get_graph(kwargs.get('graphname'))
		if g:
			res = ['{}:{}'.format(ns, url) for ns,url in g.namespaces()]
		else:
			res = ['{}:{}'.format(n, ns.url) for n, ns in
				rdf.namespaces._namespaces.items()]
		#g = rdf.__dict__.get('current_graph')
		#if g:
			#res.extend(['{}: {}'.format(ns, url) for
				#ns,url in g.namespaces()])
	else:
		# specific namespace?
		ns = rdf.namespaces.get(kwargs.get('namespace'))
		if ns:
			head = 'Terms in namespace {} ("{}""):'.format(ns.name, ns.url)
			terms = ['*classes*:']+ns.classes+['*properties*:']+ns.properties
			res = ['{}:{}'.format(ns.name, t) for t in terms]
		else:
			res = ['!Error!.']
	return '\n'.join([head]+res)


# find triples containing specific term
#FIXME: come on!
def find_term_ls(*args, **kwargs):
	"""Find triples with the given term.
	handles:
	`find <rdfentity>`
	`find <rdfentity> <graph>`
	`ls <graph>`"""
	rdfentity = kwargs.get('rdfentity')
	g = rdf.get_graph(kwargs.get('graphname'))
	# `find` command
	if rdfentity:
		if ':' in rdfentity:
			ns, term = rdfentity.split(':')
		else:
			ns, term = None, rdfentity
		return '\n'.join(rdf.find_term(term, nsp=ns, g=g))
	else:
		# `ls` command
		res = rdf.ls_rdf(g=g)
	return '\n'.join([u'({} {} {})'.format(*t) for t in res])


# bind a new namespace
#TODO: do this properly
def bind_ns(*args, **kwargs):
	"""Creates a new namespace binding in the current graph.
	handles:
	`bind <namespace> <nsurl>`
	`bind <namespace> <nsurl> <graph>`"""
	nsn = kwargs.get('namespace')
	url = kwargs.get('nsurl')
	g = rdf.get_graph(kwargs.get('graphname'))
	if not g:
		g = rdf.__dict__.get('current_graph')
	if g:
		nns = rdf.bind_ns(g, nsn, url)
		if type(nns) != str:
			nns = 'Bound namespace {}:{} to graph {}.'.format(nns.name,
				nns.url, rdf.graph_name(g))
		rdf.ns.reg_graph(g)
		rdf.extract_ns_terms(g)
		return nns




# copy graph
def cp_graph(*args, **kwargs):
	"""Create new graph by given name and clone contents
	of another graph into it.
	handles:
	`cp <graph> <graph>`
	`cp <graph>`"""
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
		# format MUST be pretty-xml, since xml ignores triples
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
# TODO: look at rdflib graph set operations
# https://rdflib.readthedocs.org/en/latest/intro_to_graphs.html#set-operations-on-rdflib-graphs
def merge_graph(*args, **kwargs):
	"""merge graph into :data:`.rdf.current_graph`.
	handles:
	`merge <graph>`
	`insert <graph> into <graph>`"""
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
			for ns,url in g2.namespaces():
				g.bind(ns, str(url))
			# copy triples from g2 into currently active graph
			for triple in g2:
				g.add(triple)
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
	if name:
		g = rdf.get_graph(name)
	else:
		g = rdf.__dict__.get('current_graph')
	if g:
		res = rdf.import_ns(g)
	else:
		return '!Abort!: no graph specified.'
	if res:
		return res
	return '!!Error!!: could not import namespaces bound by graph {}.'.format(
		rdf.graph_name(g))


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
	if name:
		g = rdf.get_graph(name)
	else:
		g = rdf.__dict__.get('current_graph')
	return rdf.save_xml(g, filename)



# add triple
def add_stm(*args, **kwargs):
	"""Add triple.
	handles:
	`add <rdfentity> <rdfrelation> <rdfentity>`
	`add <rdfentity> <rdfrelation> <rdfentity> <graph>`"""
	if len(args)>3:
		name, subj, prop, obj = args
		g = rdf.get_graph(name)
	else:
		subj, prop, obj = args
		g = rdf.__dict__.get('current_graph')
	if g:
		triple = tuple([rdf.expand_term(i) for i in (subj,prop,obj)])
		g.add(triple)
		# TODO: implement!
		return triple
