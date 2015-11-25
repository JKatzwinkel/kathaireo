#!/usr/bin/python
# -*- coding: utf-8 -*-
"""\
This package offers a way for convenient registration
of custom commands. By calling its :func:`register` method,
a formal representation of a command syntax can be
bound to a handling function desired to be called for
user input matching said command.
Functions intended to serve as handlers, when declared
like ``def func(*args, **kwargs)`` have access to
their command's arguments marked by surrounding angle
brackets (<>).

The internal representation of the resulting command
language can be found in the :data:`cmdict` member
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
	>>> commands.register("create <graph>", handler)
	Registered handling function handler('args', [...]
	>>> commands.cmdict
	{'create': {'<graph>': {'': <function handler at 0x86c26f4>}}}

Alternativley, one can also use the ``@cmd_handler`` decorator
provided by the :mod:`..kathaireo` package itself and implemented at
:func:`register_handler`:
::

	from kathaireo import cmd_handler
	@cmd_handler
	def handler(*args, **kwargs):
		\"\"\"`create <graph>`\"\"\"
		[...]

...does the same as the snippet above.


"""
__docformat__ = "restructuredtext en"
__version__ = "0.0.24-dev"
#__all__ = ['arguments', 'handlers']

import re
import os

from . import arguments
from . import handlers
from .. import rdf
from .. import util


# argument registry
reg_arg = arguments.register

# command syntax language tree
cmdict={}
"""Assembles a tree (more precisely: a forest) of which each path that
leads from a root all the way down to a leaf, stands for a legal command."""


# define regular expressions for command resolution
# argument placeholder
argex=re.compile('<([a-zA-Z_]\w*)>')
# single term
trmex=re.compile('(\".+\"|\S+)')
# file name TODO: besser
flnex=re.compile('\S+\.(rdf|owl|RDF|OWL|xml|n3)')
# url
urlex = util.urlex


# implementation of decorator @cmd_handler
def register_handler(func):
	"""\
	Decorator for command handler functions.
	Function will be copied into the namespace of :mod:`.commands.handlers`
	and registered as a handler for all commands
	whose syntaxes it specifies in its docstring.
	The package root module, :mod:`..kathaireo`, defines an
	alias of this function, the decorator ``@cmd_handler``.
	This should make it easy to extend ``kathaireo``'s
	functionality, since implementation, invocation syntax definition
	and deployment of custom commands can all be taken
	care of in the same place.

	:param func: function to be registered as a
	command handler in the :mod:`handlers` module
	namespace. Handler functions **must accept** both
	``\*args`` and ``\*\*kwargs`` parameter collections. `(Ist das so, ja?)`

	:returns: function passed on call, i.e. functions
	with ``@cmd_handler`` decorator imported from
	root module (:mod:`..kathaireo``).
	"""
	hnd_ns = handlers.__dict__
	fname = func.__name__
	if fname in hnd_ns:
		print('Overwrite handler module pointer {} with'.format(fname), end='')
		print('new command handler function at {}.'.format(func.__code__.co_filename))
	hnd_ns[fname] = func
	# if `command ...` is defined in doc line, register
	sntxs = handlers.extract_cmd_syntax(fname)
	if sntxs:
		for syntax in sntxs:
			register(syntax, func)
	else:
		print("Couldn't find handler function {}!".format(fname))
	return func




# register a handler function for a command syntax
def register(syntax, function):
	"""\
	Inserts the given command's syntax into a known commands
	dictionary and registers the given function as
	its handler.

	*Note:* this will be called automatically for
	every function with a ``@cmd_handler`` decorator
	satisfying the requirement described below, and
	specifying its invocation command syntax in its
	docstring. See :func:`.register_handler` for details.

	:param syntax: A String containing a formal
		representation of a new command's syntax.
		A command syntax may contain argument identifiers
		s.t. the handling function (and shell-features like
		autocomplete) has access to argument variables
		passed to a command. A command syntax string
		indicating a handler's capability of processing
		command arguments would look something like this,
		for instance:
		::

			'command option <arg1> <arg2> someswitch <arg3>'

	:param function: A function intended to be called when
		said command is to be executed. Should accept
		an unlimited number of both positional and keyword
		arguments and is hence recommended to look sth like
		the following:

			>>> def func(*args, **kwargs):
			...    [...]

		Note that nonetheless, it is not
		tested for fitting this requirement, but one might
		get in trouble when ignoring it.

	:returns: `True`, if function was successfully bound to
		command syntax, `False`, if command syntax
		is already in registry.
	"""
	# initialize at root level of command path tree
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
		# if term is an argument placeholder, register it
		if argex.search(term):
			arg = argex.findall(term)[0]
			arguments.register(arg)
		# walk down one level in command dict tree
		level = down
	# every command syntax string must end w linebreak
	# char (or EOL or whatever) s.t. optional command
	# parameters can be handled later
	# at last, attach leave referring to function(args**,
	# **kwargs) responsible for handling the new command
	# unless, of course, command already exists
	boundf = level.get('')
	if not boundf:
		level[''] = function
		msg=' '.join([
			'Registered handling function {}{}',
			'for command syntax \"{}\".'])
		res = True
	else:
		msg=' '.join(['Failed to register function {}{};',
			'command syntax \"{}\" already binds',
			'function {}'.format(boundf.__name__)])
		res = False
	# print msg.format(function.func_name,
	# 	function.func_code.co_varnames[:2],
	# 	' '.join(terms))
	#TODO: register argument placeholders
	return res



# message: incomplete input string
def msg_incomplete_cmd(keywords):
	"""Returns a formatted (see :module:`..shell/highlights`) string
	representation of a list, separating its items with commata.
	Intended use is the assembly of helpful error messages in case an input string
	resembles only an incomplete command, and the parser is terminating at
	the end of the input line or an unknown term, while still
	expecting one or more keywords to come up.
	"""
	keywords = ['*{}*'.format(k) for k in keywords]
	if len(keywords)>1:
		msg = ' or '.join([', '.join(keywords[:-1]),
			keywords[-1]])
	else:
		msg = keywords[0]
	msg = "!Incomplete command!: expecting {} instead of EOL.".format(
		msg)
	return msg


# execute input string, if command matches
def execute(input):
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
	# return message
	msg = ''
	# check if terms match known commands:
	# begin at language tree root
	level = cmdict
	# walk down as long as input seems to be
	# a valid command language word, i.e. input
	# term reachable by walking along its predecessors
	term = ''
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
				# path lost -> input not in language
				# not a valid command
				msg = term
				term = None
				break
	# do we have a match? or not?
	if term is None:
		return '!!Syntax error!!: term "{}" not recognized.'.format(msg)
	else:
		# if EOL code terminates term sequence, we are good.
		# if not, input is incomplete
		if level.get('') is None:
			msg = msg_incomplete_cmd(level.keys())
			# return a hint on expected input
			return msg
		else:
			# we have a match!
			# command is valid! get handler!
			# print ' '.join(path)
			func = level.get('')
			#print 'Calling {}'.format(func.__name__)
			ret = func(*args, **kwargs)
			# log argument values
			for arg,v in kwargs.items():
				arguments.to_history(arg,v)
			return ret



# what can possibly be typed in given certain prefix?
def choices_left(input, csrange):
	"""Assembles a list of terms that allow a valid input line
	given the prefix passed as `input` has been typed in so far.
	Those terms can include command keywords and argument values
	and depend on the command syntax to which the input line so far
	typed in matches, as well as legal argument values for that
	incomplete input line.
	The resulting list will only contain keywords or argument values
	that either have been started typing in, or those that may legally
	extend the current prefix, in case the latter doesn't end with
	an incomplete keyword or argument value.
	"""
	# TODO: read carefully for potential logical flaws!
	# TODO: read carefully for potential logical flaws!
	# TODO: read carefully for potential logical flaws!
	if not input:
		input = ''
	# range of relevant input (beginning of incomplete word
	#	and cursor position)
	beg, end = csrange
	# begin traversing language tree as long as it matches current input
	level = cmdict
	level_down = level
	# split input string into single terms
	# BUT only up to cursor position!
	terms = trmex.findall(input[:end])
	# append empty string if line ends on whitespace. thus the next
	# keyword/value in order can be determined later
	if re.match('.*\s+\Z', input[:end]) or end-beg<1:
		terms.append('')
	util.log('autocomplete: detected tokens are {}'.format(terms))
	#print '\nfind choices for:',terms
	# #########################3
	# parse incomplete input
	# word by word
	for term in terms:
		# walk downwards
		level = level_down
		if term in level:
			#print 'fitting:', term
			level_down = level.get(term)
		else:
			# if not a keyword, term might be an attribute value
			argnames = [t for t in level.keys()
				if argex.search(t)]
			resolved = False
			if len(argnames)>0:
				# check if term satisfies any attribute value requirements
				# TODO: auch hier das problem, dasz sich mit dem erstbesten
				# TODO zufrieden gegeben wird..?
				for a in argnames:
					if not resolved:
						arg = argex.findall(a)[0]
						# print '(argument to match is {})'.format(a)
						if arguments.validate(arg, term):
							# value matches attribute. proceed
							level_down = level.get(a)
							resolved=True
			if not resolved:
				# here is probably where the input breaks up.
				# also possibly where input goes on invalidly
				# nevertheless, we have to proceed until there
				# is no input left at all. otherwise, we might
				# end up with autocomplete suggestions for terms
				# in the middle of nowhere. If an input turns out
				# to be invalid way before it is done parsing,
				# then we simply can't provide autocompletion
				# for that input.
				# TODO: or can we? how exactly is cursor position
				# handled by readline module???
				break
	# incomplete input line has been matched against known
	# commands as far as possible. what do we have here?
	# possibility 1): input ends w potential or partly typed keyword
	# possibility 2): input ends where a value should follow
	# or is partly typed in
	#print 'fragment, keys:', term, level.keys()
	choices1 = [k for k in level.keys()]
	util.log('autocomplete: possible input is {}.'.format(choices1))
	#print term, ':', choices1
	choices = []
	for c in choices1:
		# resolve argument, if any
		if argex.search(c):
			a = argex.findall(c)[0]
			util.log('Apply for completion candidates for arg {}.'.format(a))
			choices.extend(arguments.get_suggestions(a, term))
		else:
			# if not expecting argument: check if keyword can be
			# completed
			if c.startswith(term):
				choices.append(c)
	# by default, append whitespace behind completion choice
	# if completion is ultimate (e.g. command names).
	# If choice ends on ;, this means it can possibly be
	# extended further, but is not meant to stay like it is
	# (e.g. directory names: even if completed, you can still
	# go deeper in file structure)
	choices = [''.join(c[:-1])+[c[-1]+' ',''][int(c[-1]==';')]
							for c in choices if len(c) > 0]
	util.log('Suggest {} completion candidates:'.format(len(choices)))
	util.log(', '.join(choices))
	#print 'suggestions:',choices, ''
	return choices







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
	#'exit': handlers.quit,
	#':q': handlers.quit,
	#'create <graph>': handlers.create_graph,
	'create <graph> store sqlite <sqlite>': handlers.store_sqlite,
	'load <resource> <graph>': handlers.parse_rdf,
	'show <graph> <attribute>': handlers.graph_info,
	#'load namespaces <graph>': handlers.import_namespaces,
	'connect <graph> to sqlite <sqlite>': handlers.store_sqlite,
	#'save <graph> to xml <filename>': handlers.store_xml,
	#'save xml <filename>': handlers.store_xml,
	'copy <graph> <graph>': handlers.cp_graph,
	#'merge <graph>': handlers.merge_graph,
	#'use <graph>': handlers.set_graph,
	#'add <namespace>:<rdfentity> <namespace>:<rdfproperty> <namespace>:<rdfentity>':None
	#'namespace <namespace> classes': handlers.ns_classes,
	#'namespace <namespace> properties': handlers.ns_properties,
	}

# read, compile, register command syntaxes
def init():
	"""Read, compile and register default commands.
	These are those contained by :data:`.default_cmds`
	plus those defined by the :mod:`.commands.stdcmd` module,
	parse docstrings of all functions in :mod:`.handlers` namespace
	for `command ...` syntax specifications and :func:`.register`
	those that have some.
	"""
	# default_cmds dictionarty
	for command, handler in default_cmds.items():
		register(command, handler)
	# functions in handlers-namespace
	# for all functions within this namespace, parse
	# docstrings for `command` specification and register
	# functions as handlers in case of matches.
	funcs = [(n,f) for n,f in handlers.__dict__.items()
		if hasattr(f, '__call__')]
	for fname, func in funcs:
		sntxs = handlers.extract_cmd_syntax(fname)
		if sntxs != None:
			for syntax in sntxs:
				register(syntax, func)
		else:
			print("Not found!")
	# read, compile, register stdcmd.py
	# ok. read commands from stdcmd.py
	from . import stdcmd
	print('parse', stdcmd.__file__)
	for fn, cc in stdcmd.__dict__.items():
		if hasattr(handlers, fn):
			f = handlers.__dict__.get(fn)
			if hasattr(f, '__call__'):
				for c in cc:
					#print fn, 'invoked by:', c
					register(c, f)
	# TODO: arguments!
	del stdcmd
	print('done.')



# read, compile, register command syntaxes
init() #TODO: sure this shouldnt be called by application modules
# like the shell instead of here?
# registering bindings in stdcmds.py might fail if
# handler functions with @cmd_handler decorator are in
# modules that haven't been imported yet



#################################################
# command argument placeholder handling

# TODO: write decorator to handle arguments like commands
# <resources>
reg_arg("resource", proposer=arguments.list_files_rdf,
	format=[flnex, urlex])

# <attribute>
attrs='|'.join(rdf.rdfinfotempl.keys())
reg_arg("attribute", proposer=arguments.graph_attrs,
	format=[re.compile('({})'.format(attrs)) ])
del attrs

# <sqlite>
reg_arg("sqlite", proposer=arguments.list_files_sqlite,
	format=[re.compile('.*\.sqlite3?')])

# <filename>
reg_arg("filename", proposer=arguments.list_files_rdf,
	format=[flnex])

# <namespace>
reg_arg('namespace', proposer=arguments.ls_ns)

# <rdfentity>
# TODO: !!!
reg_arg('rdfentity', proposer=arguments.ls_rdf_ent,
	format=[urlex, flnex, re.compile('\w+:\S+'),
	re.compile('\w+:(\"[^"]+\")?'),
	re.compile('\"[^"]+\"'),
	re.compile('\w+')]) #TODO: format definieren
reg_arg('rdfrelation', proposer=arguments.ls_rdf_ent,
	format=[urlex, re.compile('\w+:\S+'),
	re.compile('\w+:')]) #TODO: format definieren

# <nsurl> (namespace locator)
reg_arg('nsurl', proposer=arguments.ls_ns_urls,
	format=[urlex, flnex])
