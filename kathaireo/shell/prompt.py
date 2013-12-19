#!/usr/bin/python
# -*- coding: utf-8 -*-
"""\
This module echoes a prompt, reads user input and does output with
automatic syntax highlighting for better decipherability. Before printing,
given output messages are
"""
__docformat__ = "restructuredtext en"
__version__ = "0.0.18-dev"

import re

from .highlights import color, hilite, col_demo, stdcol
from kathaireo import rdf
from ..util import urlex, log

# colored prompt
#ps = "\001\033[32m\002>>>\001\033[0m\002 "
PS = "{}\001\033[32m\002[{}{{}}{}] {}{}".format(
	color(0), color(7), color(5), color(23), color(1))

# tokenizer regex
# TODO: is this redundant?
#_tokex = re.compile('(\"[^\"]*?\"|\'[^\']*?\'|[ ,]+|\S*|\w*|<[^>]*?>|.*)')
_splits = [
	r'[ ,;]+',
	r'!{1,2}[^!]+!{1,2}',
	r'\*[^*]+\*',
	r'"[^"]*?"',
	r'\'[^\']*?\'',
	r'<[^<>\'"]*?>',
	r'\b[0-9.]{1,}\d\b',
	r'\b\D[a-z0-9:#_./~-]+\b',
	r'\S+?',
	]
_tokex = re.compile('({})'.format('|'.join(_splits)), re.I)

# if no working graph is selected for rdf module, select None
# until further notice
if not hasattr(rdf, 'current_graph'):
	rdf.set_graph(None)

# wait for input
def input():
	"""
	Displays a single prompt, indicating the RDF
	graph currently selected for operation, then waits for user input.
	This calls standard function ``raw_input``, but given the enhancements
	that were made using the ``readline`` module at execution of
	:func:`.shell.run` with startup of the interactive interpreter.
	Thanks to these, the entity in front of the keyboard will experience
	convenience features like advanced cursor navigation and
	automatic keyword completion.
	"""
	gname = rdf.graph_name(rdf.current_graph)
	line = raw_input(PS.format(gname))
	print ''.join([color(0), color(stdcol),'\r']),
	return line


def tokenize(line):
	"""
	Dissolves a given string into its single tokens, based on
	a collection of regular expressions. Character sequences thus being recognized
	contain those within quotation marks, angle or square brackets, text
	representing numeric (decimal) values and single words marked for emphasizing
	with surrounding ``*`` or ``!``.
	:param line: single line of text to be printed to stdout
	:returns: list of single tokens
	"""
	# replace url locators by ns:term clauses.
	uris = urlex.findall(line)
	for uri in uris:
		#print '\ntry to format:', ''.join(uri)
		#print '\t', ''.join(['<{}>'.format(u) for u in uri])
		#if uri[0].startswith('file://'):
			#uri = uri[1:]
		#TODO: wahrscheinlich unnoetig:
		#genauso gut kann der rdflib namespacemanager eingesetzt werden
		#https://rdflib.readthedocs.org/en/latest/utilities.html#serializing-a-single-term-to-n3
		uri = ''.join(uri)
		url, term = rdf.struct_uri(uri) #FIXME nein!
		log('Prompt output: Split uri {} into "..{}", "{}".'.format(uri,
			url[-10:], term))
		#print u'\tfiltererd output: {} ending on "{}"'.format(url, term)
		if term:
			nsp = rdf.ns.get_ns(url)
			if nsp:
				log('substitute with {}:{}'.format(nsp.name, term))
				#print u'\tnamespace:', nsp.name, nsp.url
				line = line.replace(uri, u'{}:{}'.format(nsp.name, term)) #FIXME: nicht hier!
		else:
			line = line.replace(uri, u'!{}..{}!'.format(uri[:20],uri[-20:])) #TODO: ok, vielleicht
	# tokenize
	return _tokex.split(line)


def display(output):
	"""
	Print a given output message to stdout (active shell) linewise.
	Tokenizes each line in message and passes single tokens
	to :func:`.highlights.hilite` before reassemblage of resulting,
	possibly color-coded text parts.
	:param output: output message to be printed. Can be either one
	single string variable (linebreaks will be interpreted) or a
	list of strings (linebreaks are ignored). Unicode is preferred.
	"""
	# prefer list of strings, so try to force content into one
	if type(output) != unicode:
		if type(output) is not list:
			output = u'{}'.format(output)
	else:
		output = unicode(output)
	if type(output) is unicode:
		output = output.split('\n')
	# colorize single tokens
	for item in output:
		line = u'{}'.format(item)
		tokens = tokenize(line)
		print ''.join([hilite(t) for t in tokens])


