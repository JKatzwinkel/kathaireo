#!/usr/bin/python
# -*- coding: utf-8 -*- 
"""Dokudoku!"""
__docformat__ = "restructuredtext en"
__version__ = "0.0.1-dev"
__author__ = "Dariah-DE"

import getopt

import shell

if __name__=='__main__':
	import html5lib
	import sqlalchemy
	welcome=[
		'This is {}, version {}.'.format(__file__, __version__),
		' rdflib version: {}'.format(shell.rdf.rdflib.__version__),
		' rdflib_sqlalchemy version: {}'.format(
		shell.rdf.storage.rdflib_sqlalchemy.__version__),
		' sqkalchemy version: {}'.format(sqlalchemy.__version__),
		' html5lib version: {}'.format(html5lib.__version__),
		'stats:',
		' default commands ready: {}'.format(
		len(shell.commands.cmdict)),
		' number of known command attributes: {}'.format(
		len(shell.commands.arguments.arghist)),
		'root modules and packages']
	for m in shell.__all__:
		mod = getattr(shell, m)
		welcome.append(' {} at {}: version="{}"'.format(
			mod.__name__, mod.__path__, mod.__version__))
	del sqlalchemy
	del html5lib
	#shell.prompt.col_demo()
	shell.prompt.display(welcome)
	shell.run()

# https://rdfalchemy.readthedocs.org/en/latest/

#TODO: namespace members autocomplete
#TODO: implement rdf commands
#TODO: write setup.py
#TODO: handle command line parameters in here.
#TODO: bash autocompletion
#TODO: default command registration in interactive mode
#TODO: colored output!