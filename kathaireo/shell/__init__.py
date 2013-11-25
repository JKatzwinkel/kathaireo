#!/usr/bin/python
# -*- coding: utf-8 -*- 
"""\
The contents of the :mod:`.shell` package implement a simple
interactive command-line shell for operating on RDF resources.

Main concern of this package is assisting the user's input, e.g.
by providing autocompletion and feedback like error messages.
Nonetheless, the :mod:`.shell` package serves merely as an interface 
between user and the actual `kathaireo` functionality, which is
realized in the :mod:`.rdf` and :mod:`.commands` packages. In fact, the 
interactive shell is mainly intended to just take care of useful
input/output features. Everything beyond that is delegated 
elsewhere.

The more interesting functions of the package's root 
module is :func:`run`. 
By calling :func:`run`, an 
interactive shell is started which passes user input to the
:mod:`.commands` package for execution. When called as a script, 
this module will automatically start a shell.
"""

__docformat__ = "restructuredtext en"
__version__ = "0.0.2a-dev"
__all__ = ['prompt', 'highlights', 'complete', 'run']

import readline

from . import prompt
from .. import rdf, commands


def complete(input, state):
	"""Performs generic autocompletion action for whatever incomplete
	input string has been typed into the shell so far. Will be 
	automatically called from somewhere in the `readline` module.
	
	Depending on the current content of `readline.get_line_buffer()`,
	this function retrieves a list of input terms which are
	considered likely to be in mind of the typing user, for instance
	because they begin with what the user has typed in so far.
	This list of candidate terms is put together by the :func:`~.commands.choices_left`
	function in the :mod:`.commands` module. Read its documentation for
	more information.
	"""
	# http://stackoverflow.com/a/5638688/1933494
	buf = readline.get_line_buffer()
	# http://doughellmann.com/2008/11/pymotw-readline.html
	# begin = readline.get_begidx()
	# end = readline.get_endidx()
	sgst = [s+' ' for s in commands.choices_left(buf)]
	return sgst[state]



# http://stackoverflow.com/questions/9468435/look-how-to-fix-column-calculation-in-python-readline-if-use-color-prompt

def run():
	"""Once entered, this function won't necessarily return within
	foreseeable future. It is where the main loop of `kathaireo's` shell
	runs. In every repetition, an input line is retrieved from the
	:mod:`.prompt` module, and passed over to the :func:`~.commands.execute` function of
	module :mod:`.commands`, whose returning status message or command response
	is again given to the :mod:`.prompt` module for printing.
	"""
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
		readline.redisplay()
		output = commands.execute(line)
		prompt.display(output)



if __name__=='__main__':
	run()
