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
create_graph=['create <graph>']
# i
import_namespaces=['load namespaces <graph>',
	'load namespaces',
	'import ns']
# m
merge_graph=['merge <graph>']
# s
set_graph=['use <graph>']
show_graphs=['ls']
store_xml=['save xml <filename>', 
					'save <graph> to xml <filename>']
# q
quit=['exit', ':q', 'quit']

#TODO: arguments