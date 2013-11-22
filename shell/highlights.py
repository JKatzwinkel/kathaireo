#!/usr/bin/python
# -*- coding: utf-8 -*- 
"""\
"""
__docformat__ = "restructuredtext en"

import re

import commands.arguments as argdir

# warnings
wrnex = re.compile('![^!]+?!')
# angle brackets
angex = re.compile('<[^>]*>')
# single/double quots
qutex = re.compile('(\'[^\']*\'|\"[^\"]*\")')
# square brackets
sqrex = re.compile('\[[^]]*\]')
# uri
urlex = re.compile('[a-z]{3,6}://[a-z0-9.-]+\.[a-z]{2,4}(/\S+)*')
# filenames
flnex = re.compile('\A.*?\.[a-zA-Z0-9]{2,6}\Z')
# numbers
nmrex = re.compile('\A-?[0-9]*\.?[0-9]+\Z')


# bind color ids to regexes
_colscheme = {
	wrnex: 22, # red
	angex: 4,  # red
	qutex: 5,  # green
	urlex: 1,  # bright white
	sqrex: 23, # bright green
	flnex: 9,  # turquois
	nmrex: 6   # yellow
	}

_colors=[
'\033[0m', # normal      0
'\033[1m', # bright white
'\033[4m', # normal
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

# returns a colored representation of a given token
def hilite(token):
	for rex, cid in _colscheme.items():
		if rex.match(token):
			return '{}'.format(color(cid)+token+color(0))
	return '{}'.format(token)
