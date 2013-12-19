#!/usr/bin/python
# -*- coding: utf-8 -*-
"""\
Package structure
-----------------
**kathaireo** consists of three subpackages: :mod:`.shell` implements an interctive
command-line interface, including colorized output and autocompletion.
The :mod:`.commands` package contains interpreter functionality like command recognition and
input value validation, and both syntax specifications and handler functions of default
commands. The :mod:`.rdf` package puts a facade in front of the underlying RDF library,
rdflib_, and provides additional information about the operating context it is used in,
like the identifiers given to open RDF graphs in an active shell session or lists of
resources used by graphs or their bound namespaces.

.. _rdflib: https://github.com/RDFLib/rdflib

Shell mode
----------
The ``shell`` subpackage implements a simple user interface based on
python standard library readline_, mostly because of the autocompletion feature.
Its module :mod:`.shell.prompt` echoes a prompt, reads and returns user input
and can display possibly resulting commands output using simple syntax
highlighting, provided by module :mod:`.shell.highlights` based on regular expressions.

An interactive interpreter can be started by calling
:func:`.shell.run`. It will execute the default commands as defined in
the :mod:`.commands` package (see below), but can also be equipped
with additional custom
commands, for which to use handler functions are needed to be implemented.
To write one of those, the :mod:`.rdf` package might be useful.

.. _readline: http://docs.python.org/2/library/readline.html


Commands
--------
The :mod:`.commands` subpackage is responsible for syntax definitions and
input interpretion. Its module :mod:`.commands.handlers` contains handler functions for
builtin commands like ``create <graph>`` or ``exit``. For an explaination of
the ways in which custom commands can be defined,
see below. Builtin bindings of command syntaxes and handler functions are listed
in :mod:`.commands.stdcmd`, where lists of command aliases are assigned to
variables with the names as the command's handler functions, properly declared
as such elsewhere. For the function :func:`.commands.handlers.quit`, it looks like this:
::

    quit=['exit', ':q', 'quit']

Actually binding of these standard commands is done
by the :func:`.commands.init` function, which is called on first import of
the ``commands`` module, but not before :mod:`.commands.handlers` has been
imported. That way, the builtin handler functions implemented by the latter
are already in the package namespace and binding of standard commands works
like just described. However, any attempt to extend the list in :mod:`.commands.stdcmd` to
bind handler functions implemented by foreign code (e.g. plugins)
is likely to fail.


Defining commands
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

RDF facade
----------
TODO

"""

__docformat__ = "restructuredtext en"
__version__ = "0.0.12-dev"
__all__ = ['rdf', 'commands', 'shell', 'cmd_handler']

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

# demo module showing example custom command declaration
import extended
