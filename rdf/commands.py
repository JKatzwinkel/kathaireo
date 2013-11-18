#!/usr/bin/python

phrases=["exit", # just leave
		"load <graphname> file *.(rdf|owl)", # load existing ontology from current directory
		"load <graphname> <url>", # download ontology
		"load namespace <namespace> <url>"]

cmdict={}
for phrase in phrases:
	level=cmdict
	words = phrase.split(' ')
	for i in words[:-1]:
		down = level.get(i, {})
		if not i in level:
			level[i] = down
		level = down
	level[words[-1]] = None


def register(syntax, function):
	pass