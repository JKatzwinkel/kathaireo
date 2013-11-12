#!/usr/bin/python
# -*- coding: utf-8 -*- 
import os
import rdflib
#from rdflib_sqlalchemy.SQLAlchemy import SQLAlchemy



class RdfNamespace:
	def __init__(self, name, url):
		self.name = name
		self.url = url
		self.classes = []
		self.properties = []
		self.rdf = rdflib.Graph(identifier=name)
		# try to load namespace source
		try:
			self.rdf.parse(self.url)
		except (rdflib.plugin.PluginException, ImportError):
			self.rdf.parse(self.url, format="n3")
		except Exception as e:
			raise e
		# Part of speech stuff
		for s,p,o in self.rdf:
			if s.startswith(self.url):
				if o.endswith("Property"):
					self.properties.append(str(s))
				else:
					self.classes.append(str(s))
		self.properties = list(set(self.properties))
		self.classes = [i for i in set(self.classes) 
										if not i in self.properties]

	def __repr__(self):
		return "{}: {}".format(self.name, self.url)


# parse source of given namespace
def rdfNamespace(name, url):
	try:
		ns = RdfNamespace(name, url)
		return ns
	except:
		return None



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

	# load referenced namespaces
	rdfns = [n for n in 
								[rdfNamespace(ns, str(ref)) for ns, ref in g.namespaces()]
								if n]
	namespaces = {n.name:n for n in rdfns}
	print "Namespaces:\n--------------"
	print "\n".join(["{}".format(n) for n in namespaces.values()]) 

