#!/usr/bin/python
# -*- coding: utf-8 -*- 
from setuptools import setup, find_packages
import re
import sys

if (sys.version_info < (2, 7, 0, 'final', 0)):
    print >> sys.stderr, "*** Python 2.7.0 or better required"
    sys.exit(1)

metex = {}
for field in ['version', 'author']:
	metex[field] = re.compile('\A\s*__'+field+'__\s?=\s?[\"\'](\S+)[\"\'].*')

meta = {}
f = open('kathaireo.py')
for line in f:
	for field, rex in metex.items():
		if not field in meta:
			if rex.match(line):
				meta[field] = rex.findall(line)[0]


# setup
setup(
		name="kathaireo",
		version=meta.get('version'),
		description='Interactive tool for managing local and remote RDF resources.',
		long_description = open('README.md').read(), #__doc__.strip(),
		keywords='rdf owl ontology',
		
		url = 'https://github.com/JKatzwinkel/kathaireo',
		author = meta.get('author'),
		author_email = 'dariah-shk@bbaw.de',
		download_url = 'https://github.com/JKatzwinkel/kathaireo/archive/master.zip',
		
		packages=find_packages(),
		scripts=['kathaireo.py', 'shell.sh'],

		install_requires = [
			'rdflib>=4.0.1',
			'rdflib_sqlalchemy>=0.2',
			'sqlalchemy>=0.8.3',
			'html5lib>=1.0',
			'urllib2>=2.7'],
		dependency_links = [
			# rdflib-sqlalchemy
			''.join([
				'git+https://github.com/RDFLib/rdflib-sqlalchemy.git', 
				'@11c2ba6f76399002b68132ed66257a0b61737bd4',
				])
			],

		entry_points = {
			'console_scripts': [
				'kathaireo = kathaireo:main', 
				'shell = kathaireo.shell:run']
			},
		# closing bracket coming up!
	)
