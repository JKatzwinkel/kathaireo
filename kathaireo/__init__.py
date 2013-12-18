#!/usr/bin/python
# -*- coding: utf-8 -*-
"""\
kathaireo
=========
Package structure
-----------------
**kathaireo** consists of three subpackages: :mod:`.shell` implements an interctive
command-line interface, including colorized output and autocompletion.
The :mod:`commands` package contains interpreter functionality like command recognition and
input value validation, and both syntax specifications and handler functions of default
commands. The :mod:`rdf` package puts a facade in front of the underlying RDF library,
rdflib_, and provides additional information about the operating context it is used in,
like the identifiers given to open RDF graphs in an active shell session or lists of
resources used by graphs or their bound namespaces.

.. _rdflib https://github.com/RDFLib/rdflib

Shell mode
----------
An interactive interpreter can be started by calling
:func:`.shell.run`. It can be equipped with additional custom
commands for which handler functions are implemented. To write
one of those, the :mod:`.rdf` package might be useful.


Command definition
------------------
Registration of new commands and their handlers goes like in
this (not really useful) example:
::

	from kathaireo import commands, rdf, cmd_handler

	@cmd_handler
	def handler(**kwargs):
		\"\"\"Handles the command `command` with syntax:
		`command <param1> <param2> <title>`\"\"\"
		graphname = kwargs.get('param1')
		arg = kwargs.get('param2')
		title = kwargs.get('title')
		g = rdf.get_graph(graphname)
		resource = rdf.rdflib.term.URIRef(arg)
		title = rdf.rdflib.term.Literal(title)
		g.add((resource, rdf.rdflib.namespace.DC.title, title))

The above example handler function is decorated by the
:func:`cmd_handler` decorator, pointing to the function
:func:`.commands.register_handler`. Functions decorated
like this are automatically copied to the :mod:`.commands.handlers`
module namespace and registered for any command syntax defined
within their docstring like demonstrated. Instead of the
decorator, one might as well use:
::

	syntax = 'command <param1> <param2> <title>'
	commands.register(syntax, handler)

Like this, the kathaireo shell can easily be extended. Arguments can
be configured in a similar manner thanks to the :mod:`.commands.arguments`
module.


"""

__docformat__ = "restructuredtext en"
__version__ = "0.0.11-dev"
__all__ = ['rdf', 'commands', 'shell']

import rdf
import commands
import shell

# decorator for command handler functions
cmd_handler=commands.register_handler
"""Decorator for command handler functions.
Functions decorated by this will be copied
to the global namespace of the
:mod:`commands.handlers` module and optionally
be registered for any command syntax declared
within their docstring."""

import extended
