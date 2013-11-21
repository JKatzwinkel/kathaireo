#!/usr/bin/python
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
	"""
	Creates a new `rdflib.Graph` instance going by
	the identifier passed as first argument.

	:Parameters:

		- `identifier`: Id for the new Graph

	:Returns:

		- The resulting `rdflib.Graph` instance when
		  successful, `None` otherwise.
	"""
	if len(args)>0 and type(args[0]) is str:
		return rdf.create_graph(args[0])


# load resource content into graph
def parse_rdf(*args, **kwargs):
	"""
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

