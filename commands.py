#!/usr/bin/python

import re
import os

import rdf

# phrases=["exit", # just leave
# 		"load <graphname> file *.(rdf|owl)", # load existing ontology from current directory
# 		"load <graphname> <url>", # download ontology
# 		"load namespace <namespace> <url>"]

# dictionary holding command term paths to functions,
# like {"exit": {"\n": quit}}
cmdict={}




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
	terms = [t for t in syntax.split(' ')
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


###############################################
###############################################
##############                  ###############
##############     handlers     ###############
##############                  ###############
###############################################
###############################################


def quit(*args, **kwargs):
	"""Simply calls `exit()`."""
	exit()




def create_graph(*args, **kwargs):
	"""
	Creates a new `rdflib.Graph` instance going by
	the identifier passed as first argument.

	:Parameters:

		- `identifier`: Id for the new Graph

	:Returns:

		- The resulting `rdflib.Graph` instance when
		  successful, `None` otherwise.
	"""
	if len(args)>0 and type(args[0]) is str:
		return rdf.create_graph(args[0])




def parse_rdf(*args, **kwargs):
	"""
	Parses the resource at a given location and reads it into
	a `rdflib.Graph` identified by its name.

	:Parameters:

		- `location`: A String specifying the location of 
		  the resource to be read. Can be a path to a local
		  file or a URL.

		- `graphname`: A String identifying an `rdflib.Graph`
		  instance.

	:Returns:

		- `True`, if parsing was successful.
	"""
	location = kwargs.get('resource')
	name = kwargs.get('graphname')
	if None in [location, name]:
		if len(args)>1:
			location, name = args[:2]
	if not(None in [location, name]):
		return rdf.load_into(location, name)




