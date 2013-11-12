#!/usr/bin/python
# -*- coding: utf-8 -*- 
import os
import rdflib
#from rdflib_sqlalchemy.SQLAlchemy import SQLAlchemy

import namespaces as ns





rdfFiles=[fn for fn in os.listdir('.') if fn.endswith(".rdf")]
#store = SQLAlchemy(configuration="sqlite:///newspapers.sqlite")
#g = rdflib.Graph(store, "newspapers")

#print "Trying to load graph {} from store {}.".format(

if len(rdfFiles)>0:
	print '\n'.join(["{}: {}".format(i,fn) for i,fn in enumerate(rdfFiles)])
	c=int(raw_input("Which one of these ontologies would you like to be loaded? "))
	fn=rdfFiles[c]
	g = rdflib.Graph(identifier=''.join(fn.split(".rdf")[:-1]))
	g.parse(rdfFiles[c])

	# download missing namespace sources
	ns.provide_for(g)
