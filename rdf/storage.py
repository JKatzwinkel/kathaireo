#!/usr/bin/python
# -*- coding: utf-8 -*- 
import rdflib
import rdflib_sqlalchemy
from rdflib_sqlalchemy.SQLAlchemy import SQLAlchemy


# assign sqlite databse to graph
def sqlite(g, filename):
	"""Assigns an sqlite databse resource for an rdf graph 
	as a persistent store.
	Will overwrite? existing graph."""
	# TODO: test filename validity
	store = SQLAlchemy(configuration="sqlite:///{}".format(filename))
	return store


def save_xml(g, filename):
	xmlrdf = g.serialize()
	print 'Write {} lines of XML dump to {}.'.format(
		len(xmlrdf.split('\n')), filename)
	# TODO: test filename, if existing, etc.
	xmlfile = open(filename, 'w+')
	xmlfile.write(xmlrdf)
	xmlfile.close()
	print 'done.'
	
	
