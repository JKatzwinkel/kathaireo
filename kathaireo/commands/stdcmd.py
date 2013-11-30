#!/usr/bin/python
# -*- coding: utf-8 -*- 
"""\
Bindings between command handler functions and command syntaxes.
"""
__docformat__ = "restructuredtext en"
__version__ = "0.0.1b-dev"

# bind handler functions to command syntax specifications
# a
add_stm=['add <rdfentity> <rdfrelation> <rdfentity>']
# c
create_graph=['create <graphname>']
# i
import_namespaces=['load namespaces <graphname>',
	'load namespaces',
	'import ns']
# m
merge_graph=['merge <graphname>']
# s
set_graph=['use <graphname>']
show_graphs=['ls']
store_xml=['save xml <filename>', 
					'save <graphname> to xml <filename>']
# q
quit=['exit', ':q', 'quit']

#TODO: arguments