#!/usr/bin/python
# -*- coding: utf-8 -*- 
"""Dokudoku!"""
__docformat__ = "restructuredtext en"
__version__ = "0.0.2-dev"
__author__ = "Dariah-DE"

import getopt

import shell

def main():
	import html5lib
	import sqlalchemy
	welcome=[
		'This is {}, version "{}".'.format(__file__, __version__),
		' rdflib version: {}'.format(shell.rdf.rdflib.__version__),
		' rdflib_sqlalchemy version: {}'.format(
		shell.rdf.storage.rdflib_sqlalchemy.__version__),
		' sqlalchemy version: {}'.format(sqlalchemy.__version__),
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


if __name__=='__main__':
	main()

# https://rdfalchemy.readthedocs.org/en/latest/

#TODO: namespace members autocomplete
#TODO: implement rdf commands
#TODO: handle command line parameters in here.
#TODO: bash autocompletion
#TODO: default command registration in interactive mode
#TODO: parsing of remote resources (https://kask.eti.pg.gda.pl/redmine/projects/sova/repository/revisions/00951bd8e28d7bd58facb5a1da3a17ae9df115d4/raw/portalSubsystem/data/pizza.owl)
#TODO: somehow wrap line if input gets too long.

#try to parse these ontologies from the internet:
# https://owlverbalizer.googlecode.com/hg-history/8da67288d6be51f8d635f3bb347bacb1cf74f811/examples/tests.owl
# http://smi-protege.stanford.edu/repos/protege/protege4/libraries/owlapi-extensions/trunk/src/test/resources/pizza01.owl
# http://wise.vub.ac.be/ontologies/restaurant.owl


