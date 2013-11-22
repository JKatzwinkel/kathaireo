#!/usr/bin/python
# -*- coding: utf-8 -*- 
"""\
"""
__docformat__ = "restructuredtext en"

import re

from highlights import color, hilite


# colored prompt
ps = "\001\033[32m\002>>>\001\033[0m\002 "

# tokenizer regex
tokex = re.compile('(\"[^\"]*?\"|\'[^\']*?\'|\S*|\w*|<[^>]*?>|.*)')



# wait for input
def input():
	line = raw_input(ps)
	return line



def display(output):
	# prefer list of strings, so try to force content into one
	if type(output) != str:
		if type(output) is not list:
			output = '{}'.format(output)
	if type(output) is str:
		output = output.split('\n')

	for item in output:
		line = '{}'.format(item)
		tokens = tokex.split(line)
		print '',''.join([hilite(t) for t in tokens])



	
