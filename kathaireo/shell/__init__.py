#!/usr/bin/python
# -*- coding: utf-8 -*- 
"""\
The contents of the `shell` package implement a simple
interactive command-line shell for operating on RDF resources.

Main concern of this package is assisting the user's input, e.g.
by providing autocompletion and feedback like error messages.
Nonetheless, the `shell` package serves merely as an interface 
between user and the actual `kathaireo` functionality, which is
realized in the `rdf` and `commands` packages. In fact, the 
interactive shell is mainly intended to just take care of useful
input/output features. Everything beyond that is delegated 
elsewhere.

Some of the more interesting functions of the package's root 
module are `run` and `execute`. 
By calling `run()`, an 
interactive shell is started which passes user input to the
`commands` package for execution. When called as a script, 
this module will automatically start a shell.
The `execute(line)` function requests execution of a given
command.
"""

__docformat__ = "restructuredtext en"
__version__ = "0.0.2-dev"
__all__ = ['rdf', 'commands']

import readline

import prompt
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
	while True:
		line = prompt.input()
		output = commands.execute(line)
		prompt.display(output)



if __name__=='__main__':
	run()
