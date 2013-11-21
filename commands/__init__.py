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
import commands.arguments as arguments
import commands.handlers as handlers

reg_arg = arguments.register

# command syntax language grammar tree
cmdict={}

# define regular expressions for command resolution
# argument placeholder
argex=re.compile('<([a-zA-Z_]\w*)>')
# single term
trmex=re.compile('(\".+\"|\S+)')
# file name TODO: besser
flnex=re.compile('\S+\.rdf')
# url TODO: verbessern
urlex=re.compile('(https?|ftp)://\w+\.[a-z]+(/.*)*')

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
	terms = trmex.findall(syntax)
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
	#TODO: register argument placeholders
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
	terms = trmex.findall(input)
	# init path log for recreation of generic command
	path = []
	args = []
	kwargs = {}
	# check if terms match known commands:
	# begin at grammar tree root
	level = cmdict
	# walk down as long as input seems to be
	# a valid command language word, i.e. input
	# term reachable by walking along its predecessors
	for term in terms:
		#print ' '.join(level.keys())
		# still on track?
		if term in level:
			level = level.get(term)
			path.append(term)
		else:
			# might be just an argument value that we
			# need to recognize, validate and extract
			# first, get all argument ids that
			# might be applicable
			argnames = [t for t in level.keys()
				if argex.search(t)]
			resolved = False
			if len(argnames)>0:
				# then test if found input is valid for
				# at least one of them
				#TODO: we will probably have to recurse
				#TODO here, because we might get on the
				# wrong track by picking just any matching
				# placeholder here
				for a in argnames:
					if not resolved:
						arg = argex.findall(a)[0]
						if arguments.validate(arg, term):
							#print 'reading value for argument',
							#print '{}: {}.'.format(a,term)
							# input valid! collect value
							args.append(term)
							kwargs[arg] = term
							# proceed
							level = level.get(a)
							path.append(a)
							resolved=True
			if not resolved:
				# path lost -> input not in language/not
				# a valid command
				print 'Error at term', term
				term = None
				break
	# do we have a match? or not?
	if term is None:
		print 'Syntax error!'
		return False
	else:
		# if EOL code terminates term sequence, we are good.
		# if not, input is incomplete
		if level.get('\n') is None:
			print "Error: command is incomplete."
			# print simple help
			print "Previous input should be extended by",
			suggestions = level.keys()
			if len(suggestions)>1:
				print ' or '.join([', '.join(suggestions[:-1]), 
					suggestions[-1]])
			else:
				print suggestions[0]
			return False
		else:
			# command is valid! get handler
			print ' '.join(path)
			func = level.get('\n')
			#print 'Calling {}'.format(func.__name__)
			func(*args, **kwargs)
			return True






###############################################
###############################################
##############                  ###############
##############     default      ###############
##############     commands     ###############
##############        +         ###############
##############     handlers     ###############
##############                  ###############
###############################################
###############################################

default_cmds = {
	'exit': handlers.quit,
	'create <graphname>': handlers.create_graph,
	'load <resource> <graphname>': handlers.parse_rdf,
	'show <graphname> <attribute>': handlers.graph_info
	}

for command, handler in default_cmds.items():
	register(command, handler)

print 'Number of default commands registered:',
print len(default_cmds)

#################################################
# command argument placeholder handling

# <resources>
#TODO: proposer ueberschreiben (dateinamen globs!)
reg_arg("resource", format=[flnex, urlex])

# <attribute>
reg_arg("attribute", format=[re.compile('(size|source)')])
