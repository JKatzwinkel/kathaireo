#!/usr/bin/python
# -*- coding: utf-8 -*- 
import os
import rdflib

class Namespace:
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
def load(name, url):
	try:
		ns = _namespaces.get(name)
		if not ns:
			ns = Namespace(name, url)
		return ns
	except:
		return None

# download namespaces referenced by given rdf ontology
def provide_for(ontology):
	# load referenced namespaces
	rdfns = [n for n in 
			[load(ns, str(ref)) 
				for ns, ref in ontology._namespaces()]
			if n]
	globals()["_namespaces"] = {n.name:n for n in rdfns}
	globals().update(_namespaces)
	print "Namespaces:\n--------------"
	print "\n".join(["{}".format(n) for n in _namespaces.values()]) 
