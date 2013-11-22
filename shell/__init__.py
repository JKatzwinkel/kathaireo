#!/usr/bin/python
# -*- coding: utf-8 -*- 
__docformat__ = "restructuredtext en"
__version__ = "0.0.1-dev"

import readline

import rdf
import commands


def complete(input, state):
	# http://stackoverflow.com/a/5638688/1933494
	buf = readline.get_line_buffer()
	#line = readline.get_line_buffer().split()
	sgst = [s+' ' for s in commands.choices_left(buf)]+[None]
	return sgst[state]


# init readline module
readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
readline.set_completer(complete)

line=''
while True:
	line = raw_input('>>> ')
	commands.parse(line)
