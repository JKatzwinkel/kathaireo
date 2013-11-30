#!/usr/bin/python
# -*- coding: utf-8 -*- 
"""Doku
"""
__docformat__ = "restructuredtext en"
__version__ = "0.0.24-dev"

import re

urlex = re.compile(''.join([
	'([a-z]{3,6}://)',
	'(/?[a-z0-9.-]+(?:\.[a-z]{2,})?)',
	'(:\d+)?',
	'((?:/[^/ #]+)*)',
	'(\?[a-z0-9]+=[a-z_0-9-]*&)*',
	'(#\w*|/\S*)?']))
