#!/usr/bin/python
# -*- coding: utf-8 -*- 
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

# sammel types ein:
types={}
for s,p,o in g.triples((None, rdflib.RDF.type, None)):
	#print s,o
	instances=types.get(o, [])+[s]
	types[o] = instances

# dasselbe in grün:
#for s,o in g.subject_objects(rdflib.RDF.type):
	#print s,o

# printe typen und ausprägungen
for t,ii in types.items():
	cap="Instances of type {}:".format(t)
	print "\n{}\n{}".format(cap, '-'*len(cap))
	for n,i in enumerate(ii):
		print "{}. {}".format(n+1,i)

print "\nAha. Who is Nathan?"
print "-------------------"
print "\n".join(["{} {}".format(p,o) 
				for s,p,o in g 
				if str(s) == "http://collectivesource.com/foaf.rdf#nathan"])

print "Write xml dump to foaf.rdf"
xmldumpfile=open("foaf.rdf", "w")
xmldumpfile.write(g.serialize())
xmldumpfile.close()
