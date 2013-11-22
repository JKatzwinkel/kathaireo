#!/usr/bin/python
# -*- coding: utf-8 -*- 
"""\
"""
__docformat__ = "restructuredtext en"

import re

from highlights import color, hilite, col_demo


# colored prompt
#ps = "\001\033[32m\002>>>\001\033[0m\002 "
ps = "\001\033[32m\002>>>{} ".format(color(23))

# tokenizer regex
#_tokex = re.compile('(\"[^\"]*?\"|\'[^\']*?\'|[ ,]+|\S*|\w*|<[^>]*?>|.*)')
_splits = [
	r'[ ,;]+',
	r'!{1,2}[^!]+!{1,2}',
	r'"[^"]*?"',
	r'\'[^\']*?\'',
	r'<[^<>\'"]*?>',
	r'\b[0-9.]{1,}\d\b',
	r'\b\D[a-z0-9:#_./~-]+\b',
	r'\S+?',
	]
_tokex = re.compile('({})'.format('|'.join(_splits)), re.I)


# wait for input
def input():
	line = raw_input(ps)
	print color(0),'\r',
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
		print '',''.join([hilite(t) for t in tokens])



	
