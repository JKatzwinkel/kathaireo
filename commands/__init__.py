#!/usr/bin/python
"""\
This package offers a way for convenient registration
of custom commands. By calling its `register` method,
a formal representation of a command syntax can be
bound to a handling function desired to be called for
user input matching said command. 
Functions intended to serve as handlers, when declared
like `def func(*args, **kwargs)` have access to 
their command's arguments marked by surrounding angle
brackets (<>).

The internal representation of the resulting command
language grammar can be found in the `cmdict` member
of this module, which resembles a syntax tree in which
by traversing down along a command syntax' terms, the
thereby reached leafe refers to the corresponding
handler function.

Example:

	>>> import commands
	>>> def handler(*args, **kwargs):
	... 	name = kwargs.get("graphname") # or = args[0]
	... 	[...]
	...
	>>>	commands.register("create <graphname>", handler)
	Registered handling function handler('args', [...]
	>>> commands.cmdict
	{'create': {'<graphname>': {'\n': <function handler at 0x86c26f4>}}}

"""
__docformat__ = "restructuredtext en"
__version__ = "0.0.1-dev"

import re
import os

import rdf
import commands.arg as arg
import commands.handlers as handlers

# phrases=["exit", # just leave
# 		"load <graphname> file *.(rdf|owl)", # load existing ontology from current directory
# 		"load <graphname> <url>", # download ontology
# 		"load namespace <namespace> <url>"]

# dictionary holding command term paths to functions,
# like {"exit": {"\n": quit}}
cmdict={}

# define regular expressions for command resolution
argex=re.compile('<([a-zA-Z_]\w*)>')



def register(syntax, function):
	"""
	Inserts the given command's syntax into a known commands
	dictionary and registers the given function as
	its handler.

	:Parameters:

		- `syntax`: A String containing a formal 
		  representation of a new command's syntax.
		  A command syntax may contain argument identifiers 
		  s.t. the handling function (and shell-features like 
		  autocomplete) has access to argument variables 
		  passed to a command. A command syntax string 
		  indicating a handler's capability of processing 
		  command arguments would look something like this, 
		  for instance:

			'command option <arg1> <arg2> someswitch <arg3>'

		- `function`: A function intended to be called when
		  said command is to be executed. Should accept 
		  an unlimited number of both positional and keyword 
		  arguments and is hence recommended to look sth like 
		  the following: 

			def func(*args, **kwargs):
				[...]

		  Note that nonetheless, it is not 
		  tested for fitting this requirement, but one might
		  get in trouble when ignoring it.

	:Returns:

		- `True`, if function was successfully bound to
		  command syntax, `False`, if command syntax
		  is already in registry.
	"""
	# anchor at top level of command path dict
	level=cmdict
	# split generic syntax string and append linebreak
	terms = [t for t in re.split('\s', syntax)
			if len(t)>0]
	# insert new command binding into cmd dict tree
	# term-wise
	for term in terms:
		# if no path to current term exists so far, 
		# prepare a new one by attaching empty dict {}
		down = level.get(term, {})
		if not term in level:
			level[term] = down
		# walk down one level in command dict tree
		level = down
	# every command syntax string must end w linebreak
	# char (or EOL or whatever) s.t. optional command
	# parameters can be handled later
	# at last, attach leave referring to function(args**,
	# **kwargs) responsible for handling the new command
	# unless, of course, command already exists
	boundf = level.get('\n')
	if not boundf:
		level['\n'] = function
		msg=' '.join([
			'Registered handling function {}{}',
			'for command syntax \"{}\".'])
		res = True
	else:
		msg=' '.join(['Failed to register function {}{};',
			'command syntax \"{}\" already binds',
			'function {}'.format(boundf.func_name)])
		res = False
	print msg.format(function.func_name, 
		function.func_code.co_varnames[:2],
		' '.join(terms))
	return res




def parse(input):
	"""\
	Tests given input string against currently
	registered command syntaxes. If input turns out
	to be a valid command, a corresponding handler 
	function is called. If matching syntax contains
	argument placeholders (`"command <arg>"`), their
	respective values are extracted from the input and
	passed to the handler function.
	"""
	# split input string into single terms
	terms = [t for t in re.split('\s', input)
			if len(t)>0]
	print '_'.join(terms)
	# check if terms match known commands
	level = cmdict


###############################################
###############################################
##############                  ###############
##############     handlers     ###############
##############                  ###############
###############################################
###############################################





