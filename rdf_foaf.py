#!/usr/bin/python

import rdflib
from rdflib_sqlalchemy.SQLAlchemy import SQLAlchemy

store = SQLAlchemy(configuration="sqlite:///foaf.sqlite")
g = rdflib.Graph(store, "foaf")

print "Trying to load graph {} from store {}.".format(
	g.n3(), store.configuration)
g.store.open(store.configuration)

if len(g)<1:
	rdfurl="http://bigasterisk.com/foaf.rdf"
	print "Loading failed. Parse {0} instead.".format(rdfurl)
	g.parse(rdfurl)

print "n3 id:", g.n3()
print "number of predicates", len(g)
print "namespaces:"
for ns in g.namespaces():
	print ns
#print list(g)[:2]
for s,p,o in g.triples((None, rdflib.RDF.type, None)):
	print s,o

for s,o in g.subject_objects(rdflib.RDF.type):
	print s,o
