#!/usr/bin/python
# -*- coding: utf-8 -*- 
"""\
Bindings between command handler functions and command syntaxes.
"""
__docformat__ = "restructuredtext en"
__version__ = "0.0.1a-dev"

# bind handler functions to command syntax specifications
# c
create_graph=['create <graphname>']
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