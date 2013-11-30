#!/usr/bin/python
# -*- coding: utf-8 -*- 
"""\
The :mod:`.arguments` module keeps track of command argument usage.

On the one hand, it keeps track of proper values from user
input fitting argument placeholders in typed-in commands.
Every argument placeholder thus has its own input
history.

On the other hand, each argument placeholder gets equipped
with two properties to impose requirements on its legal 
values with: the :meth:`~.ArgValidator.propose` function provides a suggestions 
list of possible values that may replace the placeholder,
and can be used for like autocompletion.
The :attr:`~.ArgValidator.format` list contains regular expressions determining
what input values are allowed. 
"""

__docformat__ = "restructuredtext en"
__version__ = "0.0.18a-dev"

import re
import os
from glob import glob

from .. import rdf
from .. import util

# value history for each known argument placeholder
arghist = {}
"""Dictionary object in which lists of previously submitted values are
stored under assigned argument identifiers."""

# directory of known arguments and their ArgValidator instances
argvals = {}
"""Directory of registered argument identifiers, each one referencing their
assigned :class:`.ArgValidator` instance."""

# default regex for e.g identifiers, names
namex = re.compile('\A[a-zA-Z_]\w*\Z')
# for urls
urlex = util.urlex

###############################################################
####################   arg handling class  ####################
###############################################################
class ArgValidator:
	"""Container class for the two main validity specifiers an argument
	identifier can be assigned to: an autocompletion candidate proposal
	function (default one is :func:`.propose_default`) and a
	:attr:`~.ArgValidator.format` list of regular expressions for checking
	value validity.
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
		


###############################################################
####################    module functions   ####################
###############################################################

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
	"""calls an argument placeholder's :meth:`~.ArgValidator.propose` handler 
	function and returns resulting suggestions.
	"""
	# get validator or assign a new default instance
	validator = argvals.get(name, ArgValidator(name))
	# call it
	suggestions = validator.propose(prefix)
	return suggestions



# validate argument value
def validate(arg, input):
	"""Validates given input string according to specified
	argument's value restrictions.
	Return true if input is ok."""
	validator = argvals.get(arg, ArgValidator(arg))
	return validator.validate(input)


# add to arg history
def to_history(arg, value):
	"""Write a value to an argument's input history stored in :obj:`arghist`."""
	hist = arghist.get(arg, [])
	if not arg in arghist:
		arghist[arg] = hist
	hist.append(value)




# register
def register(name, proposer=propose_default, format=None):
	"""Registers an argument placeholder. This means,
	for an arguments name/identifier, a user input history
	and an :class:`.ArgValidator` instance are created.

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
	:param proposer: input value proposal
		handling function for this argument (optional). This will
		be called when autocompletion recognizes that
		someone is about to input a value for this
		argument and wants assistance. Any function
		meant to serve as a proposal handler must take
		exactly two parameters: 
	
			1. the argument placeholder identifier,
			2. the prefix that needs to be autocompleted
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


########################################################
########################################################
########################################################
############ argument handler functions
########################################################
########################################################
########################################################

def lsdir(prefix, filetypes):
	"""List contents of whatever directory can be
	dereived from given prefix. Result contains
	subdirectories and files whose extensions and
	names match the prefix. filetypes are passed
	as a list of globs (``['*.rdf', '*.owl', ...]``).
	"""
	# extract path locator (relative)
	if os.sep in prefix:
		if prefix.count(os.sep)>1 or prefix[0] != os.sep:
			path = os.sep.join(prefix.split(os.sep)[:-1])
		else:
			path = os.sep.join(['']+prefix.split(os.sep)[:-1])
		rpth = path
	else:
		path = '.'
		rpth = ''
	# initialize sugg list with subdirs
	# terminate string w no space char ; to let commands
	# module know that this would be still to be
	# extended, and hence not decorated by a trailing
	# space, like completions normally do
	files = ['{}{};'.format(fn, os.sep) for fn in os.listdir(path) 
						if os.path.isdir(fn)]
	# extend by files matching extensions
	for ext in filetypes:
		files.extend(glob(os.path.join(rpth,ext)))
	# make sure files match prefix
	files = [fn for fn in files if fn.startswith(prefix)]
	return files


# list of globs matching potential ontology files
rdfglobs = ["*.rdf", "*.RDF", "*.owl", "*.OWL", "*.n3", "*.xml"]
# list ontology files in current directory (rdf, owl, n3, xml)
def list_files_rdf(arg, prefix):
	"""Returns a list of local files with extensions `.rdf, .owl, .n3` and `.xml`,
	matching given prefix.
	"""
	suggestions = lsdir(prefix, rdfglobs)
	suggestions.extend(propose_default(arg, prefix))
	return suggestions # TODO: +[None] ??


# suggest local sqlite files
def list_files_sqlite(arg, prefix):
	"""Returns a list of local files with extensions `.sqlite` and 
	`.sqlite3`.
	"""
	suggestions = lsdir(prefix, ['*.sqlite', '*.sqlite3'])
	suggestions.extend(propose_default(arg, prefix))
	return suggestions # TODO: +[None] ??



# propose rdf graph attribute ids
def graph_attrs(arg, prefix):
	"""Returns a list of names matching the given prefix and identifying
	RDF graphs registered by the :mod:`.rdf` module."""
	attrs = rdf.rdfinfotempl.keys()
	suggestions = [a for a in attrs if a.startswith(prefix)]
	suggestions.extend(propose_default(arg, prefix))
	return suggestions


# autocomplete namespaces
def ls_ns(arg, prefix):
	"""Returns currently loaded namespaces."""
	suggestions = [s for s in rdf.namespaces.get_names()
		if s.startswith(prefix)]
	g = rdf.__dict__.get('current_graph')
	#if g:
		#suggestions.extend([ns for ns,_ in g.namespaces()
			#if ns.startswith(prefix)])
	suggestions.extend(propose_default(arg, prefix))
	return suggestions


def ls_rdf_ent(arg, prefix):
	"""Returns rdf entities (classes, properties)."""
	suggestions = []
	#print '\b\b{}>{}>\b'.format('\b'*len(prefix), prefix),
	if ':' in prefix:
		#print 'YEAH\b\b\b\b\b',
		nn, ent = prefix.split(':', 1)
		#print nn,'-',ent
		ns = rdf.namespaces.get(nn)
		if ns:
			#print 'found ns:', nn,
			terms = ns.properties[:] #make deep copy or cry.
			if arg == 'rdfentity':
				terms.extend(ns.classes)
			suggestions.extend(['{}:{}'.format(nn,t) for 
				t in  terms if t.startswith(ent)])
			#print suggestions
	else:
		suggestions.extend([s+':;' for s in rdf.namespaces.get_names()
			if s.startswith(prefix)])
	#suggestions = [s for s in suggestions if s.startswith(prefix)]
	suggestions.extend(propose_default(arg, prefix))
	return suggestions


def resolve_local_url(url):
	"""Converts from `file:///` URL to absolute path."""
	#TODO: implement
	return url.split('/',1)[1]


# propose namespace locations
def ls_ns_urls(arg, prefix):
	"""Namespace locators."""
	suggestions = lsdir(prefix, rdfglobs)
	# try to extract URIs from rdf data
	for trp in rdf.ls_rdf():
		uris = urlex.findall('{} {} {}'.format(*trp))
		uris = [uri[int(uri[0].startswith('file:/')):] for
					uri in uris]
		suggestions.extend([rdf.struct_uri(''.join(uri))[0] 
			for uri in uris
			if any([field.startswith(prefix) for field in uri[:2]])])
	suggestions.extend(propose_default(arg, prefix))
	return suggestions
