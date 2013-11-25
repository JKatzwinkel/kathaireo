#!/usr/bin/python
# -*- coding: utf-8 -*- 
"""\
An interactive interpreter can be started by calling 
:func:`.shell.run`. It can be equipped with additional custom
commands for which handler functions are implemented. To write 
one of those, the :mod:`.rdf` package might be useful.

Registration of new commands and their handlers goes like in
this (not really useful) example:
::

	from kathaireo import commands, rdf

	def handler(**kwargs):
		graphname = kwargs.get('param1')
		arg = kwargs.get('param2')
		title = kwargs.get('title')
		g = rdf.get_graph(graphname)
		resource = rdf.rdflib.term.URIRef(arg)
		title = rdf.rdflib.term.Literal(title)
		g.add((resource, rdf.rdflib.namespace.DC.title, title))

	syntax = 'command <param1> <param2> <title>'
	commands.register(syntax, handler)

Like this, the kathaireo shell can easily be extended. Arguments can
be configured in a similar manner thanks to the :mod:`.commands.arguments`
module.
"""

__docformat__ = "restructuredtext en"
__version__ = "0.0.1b-dev"
__all__ = ['rdf', 'commands', 'shell']

import rdf
import commands
import shell
