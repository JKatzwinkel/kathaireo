#!/usr/bin/python
# -*- coding: utf-8 -*- 
"""Doku
"""
__docformat__ = "restructuredtext en"
__version__ = "0.0.24-dev"

import re
import logging

# urlex = re.compile(''.join([
# 	'([a-z]{3,6}://)', # protocol prefix
# 	'(/?[a-z0-9.-]+(?:\.?[a-z]{2,})?)', # domain or root directory
# 	'(:\d+)?', # port number
# 	'((?:/[^/ #.]+)*/)', # url host path
# 	#'(\?[a-z0-9]+=[a-z_0-9-]*&)*', # parameter fields
# 	'([^/# ]+)(/|#)?',
# 	'([^#]*)/?'])) # anchor or fresource name

urlex = re.compile(''.join([
	'([a-z]{3,6}://)', # protocol prefix
	'(/?[a-z0-9.-]+(?:\.?[a-z]{2,})?)', # domain or root directory
	'(:\d+)?', # port number
	'((?:/[^/ #.]+)*/)', # url host path
	#'(\?[a-z0-9]+=[a-z_0-9-]*&)*', # parameter fields
	'([^/# ]+(?:/|#)?)', # terminate directory or resource file name
	'([^/# ]*)/?'])) # anchor

logging.basicConfig(filename='.kathaireo.log', level=logging.DEBUG,
	format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
log=logging.info