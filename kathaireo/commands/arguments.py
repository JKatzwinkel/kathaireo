#!/usr/bin/python
# -*- coding: utf-8 -*- 
"""\
The `arg` module keeps track of command argument usage.

On the one hand, it keeps track of proper values from user
input fitting argument placeholders in typed-in commands.
Every argument placeholder thus has its own input
history.

On the other hand, each argument placeholder gets equipped
with two properties to impose requirements on its legal 
values with: the `propose` function provides a suggestions 
list of possible values that may replace the placeholder,
and can be used for like autocompletion.
The `format` list contains regular expressions determining
what input values are allowed.
"""

__docformat__ = "restructuredtext en"
__version__ = "0.0.1-dev"

import re
import os
from glob import glob

from .. import rdf

# value history for each known argument placeholder
arghist = {}
# directory of known arguments and their ArgValidator instances
argvals = {}

# default regex for e.g identifiers, names
namex = re.compile('\A[a-zA-Z_]\w*\Z')

class ArgValidator:
	"""
	"""
	def __init__(self, name):
		self.name = name
		self.propose_func = propose_default
		self.format = [namex]

	def propose(self, prefix):
		"""Calls this instance's value proposal handler
		and returns all suggestions for the given 
		input prefix."""
		return self.propose_func.__call__(
			self.name, prefix)

	def validate(self, str):
		"""Tests validity of a given string according
		to this argument's value restrictions."""
		valid = any([r.search(str) for r in self.format])
		return valid
		




# default function for value proposal
def propose_default(arg, prefix):
	"""Default function for argument value proposal.
	Looks up previous values for this argument and
	suggests those that match the given prefix.
	Can be overwritten under this premise.
	"""
	hist = arghist.get(arg, [])
	suggestions = [v for v in hist if v.startswith(prefix)]
	return suggestions


# calls an argument placeholder's propose handler and
# returns resulting suggestions
def get_suggestions(name, prefix):
	"""calls an argument placeholder's `propose` handler 
	function and returns resulting suggestions.
	"""
	# get validator or assign a new default instance
	validator = argvals.get(name, ArgValidator(name))
	# call it
	suggestions = validator.propose(prefix)
	return suggestions


# register
def register(name, proposer=propose_default, format=None):
	"""Registers an argument placeholder. This means,
	for an arguments name/identifier, a user input history
	and an `ArgValidator` instance are created.

	The latter is responsible for suggesting appropriate 
	input values for this argument (which might be useful
	in features like autocompletion) and for determining
	wheather a given value is legal for this argument 
	(like variable names are not meant to start with a number,
	urls must satisfy a certain format, and stuff like that.).

	If an argument has been registered before, no changes
	are made unless a custom proposal function or a list
	of regular expressions is being passed in this call.

	:param name: identifier of argument to register
	:param proposer: (optional) input value proposal
		  handling function for this argument. This will
		  be called when autocompletion recognizes that
		  someone is about to input a value for this
		  argument and wants assistance. Any function
		  meant to serve as a proposal handler must take
		  exactly two parameters: 1. the argument placeholder 
		  identifier,  2. the prefix that needs to be
		  autocompleted
	"""
	# create value history 
	if not name in arghist:
		arghist[name] = []
	# create or retrieve validator
	if not name in argvals:
		validator = ArgValidator(name)
		argvals[name] = validator
		# print 'Registered argument \"{}\".'.format(name)
	else:
		validator = argvals.get(name)
	# update validator if necessary
	if not proposer in [propose_default, None]:
		validator.propose_func = proposer
	if type(format) is list:
		validator.format = format


# validate argument value
def validate(arg, input):
	"""Validates given input string according to specified
	argument's value restrictions.
	Return true if input is ok."""
	validator = argvals.get(arg, ArgValidator(arg))
	return validator.validate(input)


# add to arg history
def to_history(arg, value):
	"""Write a value to an argument's input history."""
	hist = arghist.get(arg, [])
	if not arg in arghist:
		arghist[arg] = hist
	hist.append(value)


########################################################
# argument handler functions
########################################################

# list of globs matching potential ontology files
rdfglobs = ["*.rdf", "*.RDF", "*.owl", "*.OWL", "*.n3", "*.xml"]
# list ontology files in current directory (rdf, owl, n3, xml)
def list_files_rdf(arg, prefix):
	"""Returns a list of local files with extensions .rdf, .owl, .n3 and .xml,
	matching given prefix."""
	files = []
	path = os.sep.join(prefix.split(os.sep)[:-1])
	for rdfglob in rdfglobs:
		files.extend(glob(os.path.join(path,rdfglob)))
	suggestions = [fn for fn in files if fn.startswith(prefix)]
	suggestions.extend(propose_default(arg, prefix))
	return suggestions # TODO: +[None] ??

# suggest local sqlite files
def list_files_sqlite(arg, prefix):
	"""Returns a list of local files with extensions .sqlite and .sqlite3."""
	files = []
	path = os.sep.join(prefix.split(os.sep)[:-1])
	for glb in ['*.sqlite', '*.sqlite3']:
		files.extend(glob(os.path.join(path,glb)))
	suggestions = [fn for fn in files if fn.startswith(prefix)]
	suggestions.extend(propose_default(arg, prefix))
	return suggestions # TODO: +[None] ??



# propose rdf graph attribute ids
def graph_attrs(arg, prefix):
	"""Returns a list of names matching the given prefix and identifying
	RDF graphs registered by the `rdf` module."""
	attrs = rdf.rdfinfotempl.keys()
	suggestions = [a for a in attrs if a.startswith(prefix)]
	suggestions.extend(propose_default(arg, prefix))
	return suggestions


