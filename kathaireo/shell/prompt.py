#!/usr/bin/python
# -*- coding: utf-8 -*- 
"""\
This module reads user input and responds with pretty and
colorful output.
"""
__docformat__ = "restructuredtext en"
__version__ = "0.0.18-dev"

import re

from .highlights import color, hilite, col_demo, stdcol, urlex
from kathaireo import rdf

# colored prompt
#ps = "\001\033[32m\002>>>\001\033[0m\002 "
ps = "{}\001\033[32m\002[{}{{}}{}] {}{}".format(
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
	gname = rdf.graph_name(rdf.current_graph)
	line = raw_input(ps.format(gname))
	print ''.join([color(0), color(stdcol),'\r']),
	return line


def tokenize(line):
	# replace url locators by ns:term clauses.
	uris = urlex.findall(line)
	for uri in uris:
		#print '\ntry to format:', ''.join(uri)
		#print '\t', ''.join(['<{}>'.format(u) for u in uri])
		uri = ''.join(uri)
		url, term = rdf.struct_uri(uri)
		#print u'\tfiltererd output: {} ending on "{}"'.format(url, term)
		if term:
			nsp = rdf.namespaces.get_ns(url)
			if nsp:
				#print u'\tnamespace:', nsp.name, nsp.url
				line = line.replace(uri, u'{}:{}'.format(nsp.name, term))
		else:
			line = line.replace(uri, u'!{}..{}!'.format(uri[:10],uri[-10:]))
	# tokenize
	return _tokex.split(line)


def display(output):
	# prefer list of strings, so try to force content into one
	if type(output) != unicode:
		if type(output) is not list:
			output = u'{}'.format(output)
	if type(output) is unicode:
		output = output.split('\n')
	# colorize single tokens
	for item in output:
		line = u'{}'.format(item)
		tokens = tokenize(line)
		print ''.join([hilite(t) for t in tokens])


