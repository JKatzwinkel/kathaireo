#!/usr/bin/python
# -*- coding: utf-8 -*- 
"""Dokudoku!"""
__docformat__ = "restructuredtext en"
__version__ = "0.0.1-dev"
__author__ = "Dariah-DE"

import getopt

import shell

if __name__=='__main__':
	print 'This is {}, version {}.'.format(__file__, __version__)
	print ' rdflib version: {}'.format(shell.rdf.rdflib.__version__)
	print ' rdflib_sqlalchemy version: {}'.format(
		shell.rdf.storage.rdflib_sqlalchemy.__version__)
	import sqlalchemy
	print ' sqkalchemy version: {}'.format(sqlalchemy.__version__)
	del sqlalchemy
	import html5lib
	print ' html5lib version: {}'.format(html5lib.__version__)
	del html5lib
	print 'stats:'
	print ' default commands ready: {}'.format(
		len(shell.commands.cmdict))
	print ' number of known command attributes: {}'.format(
		len(shell.commands.arguments.arghist))
	print 'root modules and packages'
	for m in shell.__all__:
		mod = getattr(shell, m)
		print ' {} at {}: version={}'.format(
			mod.__name__, mod.__path__, mod.__version__)
	shell.run()

# https://rdfalchemy.readthedocs.org/en/latest/

#TODO: namespace members autocomplete
#TODO: implement rdf commands
#TODO: write setup.py
#TODO: handle command line parameters in here.
#TODO: bash autocompletion
#TODO: default command registration in interactive mode
#TODO: colored output!