#!/usr/bin/python
# -*- coding: utf-8 -*- 
from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages
import re
import sys
import os

if (sys.version_info < (2, 7, 0, 'final', 0)):
    print >> sys.stderr, "*** Python 2.7.0 required, not compatible to Python 3"
    sys.exit(1)

metex = {}
for field in ['version', 'author']:
	metex[field] = re.compile('\A\s*__'+field+'__\s?=\s?[\"\'](\S+)[\"\'].*')

meta = {}
f = open(os.path.join('kathaireo','__init__.py'))
for line in f:
	for field, rex in metex.items():
		if not field in meta:
			if rex.match(line):
				meta[field] = rex.findall(line)[0]


# setup
setup(
		name = "Kathaireo",
		version = meta.get('version'),
		description = 'Interactive RDF shell',
		long_description = open('README.md').read(), #__doc__.strip(),
		keywords = 'rdf owl ontology',
    classifiers=['Environment :: Console',
    	'Operating System :: OS Independent',
    	'Programming Language :: Python :: 2.7',
    	'Programming Language :: Python :: 2 :: Only'],
		
		url = 'https://github.com/JKatzwinkel/kathaireo',
		author = meta.get('author'),
		author_email = 'dariah-shk@bbaw.de',
		download_url = 'https://github.com/JKatzwinkel/kathaireo/archive/master.zip',
		
		src_root = '',
		packages = find_packages(),
		scripts = ['kathaireo-shell', #'rdfshell'
			],
		#py_modules = ['kathaireo-shell'],

		install_requires = [
			'rdflib>=4.0.1',
			'rdflib-sqlalchemy>=0.2',
			'sqlalchemy>=0.8.3',
			],
		dependency_links = [
			# rdflib-sqlalchemy
			'https://github.com/RDFLib/rdflib-sqlalchemy',
			''.join([
				'https://github.com/RDFLib/rdflib-sqlalchemy.git',
				#'#egg=rdflib-sqlalchemy', 
				#'@11c2ba6f76399002b68132ed66257a0b61737bd4',
				]),
			],

		entry_points = {
			'console_scripts': [
				#'kathaireo-shell = kathaireo:main', 
				#'rdfshell = kathaireo.shell:run'
				]
			},
		# closing bracket coming up!
	)
