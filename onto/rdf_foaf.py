#!/usr/bin/python
# -*- coding: utf-8 -*- 
import rdflib
from rdflib_sqlalchemy.SQLAlchemy import SQLAlchemy

filenamerdf="newspapers.rdf"
store = SQLAlchemy(configuration="sqlite:///newspapers.sqlite")
g = rdflib.Graph(store, "newspapers")

print "Trying to load graph {} from store {}.".format(
	g.n3(), store.configuration)
g.store.open(store.configuration)

if len(g)<1:
	#rdfurl="http://bigasterisk.com/foaf.rdf"
	rdfurl="http://chroniclingamerica.loc.gov/newspapers.rdf"
	#rdfurl="newspapers.rdf.1"
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
	for n,i in enumerate(ii[:10]):
		print "{}. {}".format(n+1,i)
	if len(ii)>10:
		print "..."

#FOAF = rdflib.Namespace("http://xmlns.com/foaf/0.1/")
#g.add((rdflib.term.URIRef("http://bigasterisk.com/foaf.rdf#drewp"),
			#FOAF['knows'],
			#rdflib.term.URIRef("http://collectivesource.com/foaf.rdf#nathan")))
#g.add((rdflib.term.URIRef("http://collectivesource.com/foaf.rdf#nathan"),
			#FOAF['knows'],
			#rdflib.term.URIRef("http://bigasterisk.com/foaf.rdf#drewp")))
#g.add((rdflib.term.URIRef("http://collectivesource.com/foaf.rdf#nathan"),
			#FOAF["interest"],
			#rdflib.term.URIRef("http://fantasyfamegame.com/")))

#print "\nAha. Who is Nathan?"
#print "-------------------"
#print "\n".join(["{} {}".format(p,o) 
				#for s,p,o in g 
				#if str(s) == "http://collectivesource.com/foaf.rdf#nathan"])


print "Write xml dump to", filenamerdf
xmldumpfile=open(filenamerdf, "w")
xmldumpfile.write(g.serialize())
xmldumpfile.close()
