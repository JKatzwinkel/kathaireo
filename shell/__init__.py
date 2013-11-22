#!/usr/bin/python
# -*- coding: utf-8 -*- 
"""\
Doku doku doku.
"""
__docformat__ = "restructuredtext en"
__version__ = "0.0.1-dev"
__all__ = ['rdf', 'commands']

import readline

import rdf
import commands


def complete(input, state):
	# http://stackoverflow.com/a/5638688/1933494
	buf = readline.get_line_buffer()
	#line = readline.get_line_buffer().split()
	sgst = [s+' ' for s in commands.choices_left(buf)]
	return sgst[state]


def execute(line):
	return commands.execute(line)


def run():
	print 'ok.\n'
	# init readline module
	readline.set_completer_delims(' \t\n;')
	readline.parse_and_bind("tab: complete")
	readline.set_completer(complete)
	#TODO: naja...
	# go!
	line=''
	prompt = "\001\033[32m\002>>>\001\033[0m\002 "
	while True:
		line = raw_input(prompt)
		commands.execute(line)


if __name__=='__main__':
	run()
