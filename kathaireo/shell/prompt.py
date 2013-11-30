#!/usr/bin/python
# -*- coding: utf-8 -*- 
"""\
This module reads user input and responds with pretty and
colorful output.
"""
__docformat__ = "restructuredtext en"
__version__ = "0.0.1-dev"

import re

from .highlights import color, hilite, col_demo, stdcol
from kathaireo import rdf

# colored prompt
#ps = "\001\033[32m\002>>>\001\033[0m\002 "
ps = "{}\001\033[32m\002-[{{}}]#{}{} ".format(color(0), color(23), color(1))

# tokenizer regex
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
	return _tokex.split(line)

def display(output):
	# prefer list of strings, so try to force content into one
	if type(output) != str:
		if type(output) is not list:
			output = '{}'.format(output)
	if type(output) is str:
		output = output.split('\n')
	# colorize single tokens
	for item in output:
		line = '{}'.format(item)
		tokens = tokenize(line)
		print ''.join([hilite(t) for t in tokens])


