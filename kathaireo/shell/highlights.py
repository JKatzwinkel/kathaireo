#!/usr/bin/python
# -*- coding: utf-8 -*- 
"""\
Syntax highlighting.
"""
__docformat__ = "restructuredtext en"

import re
import os.path
from random import randrange as rnd

from ..commands import arguments as argdir
from ..rdf import namespaces
from .. import util

# errors
errex = re.compile('!![^!]+!!')
# warnings
wrnex = re.compile('![^!]+?!')
# emphasized
bldex = re.compile('\*[^*]+?\*')
# angle brackets
angex = re.compile('<[^>]*>')
# single/double quots
qutex = re.compile('(\'[^\']*\'|\"[^\"]*\")')
# square brackets
sqrex = re.compile('\[[^[]]*\]')
# uri
#urlex = re.compile('[a-z]{3,6}:///?[a-z0-9.-]+\.[a-z]{2,}(:\d+)?(/\S+)*')
#urlex = re.compile('([a-z]{3,6}:///?[a-z0-9.-]+\.[a-z]{2,})(:\d+)?(/\S+?)*(\?[a-z0-9]+=[a-z_0-9-]*&)*(#\w*)?\s')
# urlex = re.compile(''.join([
# 	'([a-z]{3,6}:///?)',
# 	'([a-z0-9.-]+(?:\.[a-z]{2,})?)',
# 	'(:\d+)?',
# 	'((?:/[^/ #]+)*)',
# 	'(\?[a-z0-9]+=[a-z_0-9-]*&)*',
# 	'(#\w*|/\S*)?']))
urlex = util.urlex
# filenames
flnex = re.compile('.*?\.[a-z0-9~_]{1,6}', re.I)
# numbers
nmrex = re.compile('[-]?\d*\.?\d{1,}')
# keywords
_kw = ' '.join([
	'namespaces? triples? graph rdf xml sqlite sql',
	'commands? attributes? n3'])
_kw = [k+'$' for k in _kw.split()]
keyex = re.compile('({})'.format('|'.join(_kw)), re.I)


# bind color ids to regexes
_colscheme = {
	errex: 14, # white text on red background
	wrnex: 22, # red
	bldex: 1,  # bold
	qutex: 4,  # red
	angex: 7,  # blue
	urlex: (1,2,8),  # underscore
	sqrex: 23, # bright green
	nmrex: 6,  # yellow
	flnex: 9,  # turquois
	keyex: 27  # bright blue 
	}

_rexorder = [errex, wrnex, bldex, qutex, angex, urlex, 
			sqrex, nmrex, flnex, keyex]

#print '\n'.join(['{}:{}'.format(k.pattern,v) 
	#for k,v in _colscheme.items()])

_colors=[
'\033[0m', # normal      0
'\033[1m', # bright white
'\033[4m', # underscored
'\033[7m', # white background
'\033[31m', # red
'\033[32m', # green      5
'\033[33m', # yellow
'\033[34m', # blue
'\033[35m', # purple
'\033[36m', # turquoid
'\033[37m', # normal    10
'\033[38m',
'\033[39m',
'\033[40m', # white on dark grey bg
'\033[41m', # red bg
'\033[42m', # green bg  15
'\033[43m', # yellow bg
'\033[44m', # blue bg
'\033[45m', # pink bg
'\033[46m', # turq bg
'\033[47m', # grey bg   20
'\033[90m', # grey text
'\033[91m', # bright red
'\033[92m', # green 
'\033[93m', # yellow
'\033[94m', # blue      25
'\033[95m', # pink
'\033[96m', # turq
'\033[97m',
'\033[98m',
'\033[99m',          #  30
'\033[100m', # white on grey
'\033[101m', # white on bright red
'\033[102m', # on bright green
'\033[103m', # yellow
'\033[104m', # blue     35
'\033[105m', # pink
'\033[106m', # turq
'\033[107m', # white on white
'\033[108m'	]



# returns ith color code
def color(i):
	return _colors[i]

# demonstrates how applied color codes look
def col_demo():
	for i,col in enumerate(_colors):
		print '{}{:2}{}'.format(color(i), i, color(0)),
		if i % 8 > 6:
			print


# returns a colored representation of a given token
def hilite(token):
	#cid = rnd(13)
	#return '{}'.format(color(cid)+token+color(0))
	#
	#rexorder = _rexorder[:]
	#rexorder.insert(5,re.compile('({})'.format(
		#'|'.join(namespaces.get_names()))))
	for rex in _rexorder:
		if rex.match(token):
			cid = _colscheme.get(rex)
			if hasattr(cid, '__len__'):
				cid = u''.join([color(i) for i in cid])
			else:
				cid = color(cid)
			# error and warning markups must be removed
			if rex in [wrnex, errex, bldex]:
				if rex is errex:
					i = 2
				else:
					i = 1
				token = u'{}{}{}{}'.format(
					cid, token[i:-i], color(0), color(stdcol))
			# if filename matches, check if such file exists
			elif rex is flnex:
				if not(os.path.exists(token) 
					and os.path.isfile(token)):
					cid = color(7)
					continue
			return u'{}'.format(cid+token+color(0)+color(stdcol))
		else:
			# hilight ns:term clauses
			fields = token.split(':',1)
			if len(fields)<2:
				fields.append(None)
			nsn, term = fields
			if nsn in namespaces._namespaces:
				if term == None or re.match('[a-z][a-z0-9_-]*', term, re.I):
					token = u'{}{}{}'.format(color(8), token, color(0))
					continue
	return u'{}'.format(token)


########
stdcol=0
print u'{}\r'.format(color(stdcol)),
