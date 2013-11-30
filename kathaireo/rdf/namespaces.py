#!/usr/bin/python
# -*- coding: utf-8 -*- 
import os
import rdflib

from . import remote

_namespaces={}

class Namespace:
	"""Dokudoku"""
	def __init__(self, name, url):
		self.name = name
		self.url = url
		self.classes = []
		self.properties = []
		self.rdf = rdflib.Graph(identifier=name)
		# try to load namespace source
		try:
			#self.rdf.parse(self.url)
			remote.parse(self.rdf, self.url)
		except Exception: #(rdflib.plugin.PluginException, ImportError):
			#self.rdf.parse(self.url, format="n3")
			remote.parse(self.rdf, self.url, format='n3')
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
		return "<namespace '{}' at {}>: {} triples".format(
			self.name, self.url, len(self.rdf))


# parse source of given namespace
def load(name, url):
	"""Downloads a namespace resource at given url and
	embeds its contents into a new `Namespace` instance."""
	try:
		ns = _namespaces.get(name)
		if not ns:
			ns = Namespace(name, url)
		return ns
	except:
		return None


# download namespaces referenced by given rdf ontology
def provide_for(ontology):
	"""Imports definitions of namespaces a given graph is using."""
  #load referenced namespaces
	rdfns = [n for n in 
			[load(ns, str(ref)) 
				for ns, ref in ontology.namespaces()]
			if n]
	_namespaces.update({n.name:n for n in rdfns})
	globals().update(_namespaces)
	#print "Namespaces:\n--------------"
	#print "\n".join(["{}".format(n) for n in _namespaces.values()])
	return rdfns


# list known namespace names
def get_names():
	return sorted(_namespaces.keys())


# list known namespaces
def spaces():
	return [_namespaces[n] for n in 
		sorted(_namespaces.keys())]
