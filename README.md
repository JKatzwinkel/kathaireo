## kathaireo ##

Kathaireo is intended to become an interactive shell 
for operating on RDF and stuff. Its makes use of 
[`rdflib`][rdflib] and
[`rdflib-sqlalchemy`][rdflib-sqlalchemy]. 

Main goal is to provide a fast and slim tool
for easier work on RDF, OWL, etc. ontologies, including imports local 
and remote sources, persistent storage with Sqlite etc., 
namespace support and convenience features like context-aware 
autocompletion and reference resolution.


### command declaration ###

Custom commands can easily be added to extend the list of predefined ones.
This might make it easier to hack specialized plugins at some point.

Registration of a new command works like this:

```python
from kathaireo import commands
from kathaireo import rdf

def triples_with_object(*args, **kwargs):
	name = kwargs.get("graphname") # access argument values as defined
	objid = kwargs.get("ontoclass") # in command syntax
	o = rdf.rdflib.URIRef(objid)
	g = rdf.get_graph(name)
	for s,p in g.subject_predicates(o):
		print s,p
	g.subject_predicates(rdf.rdflib.URIRef()):

commands.register("triples <graphname> object <ontoclass>", triples_with_object)
commands.parse("create g") # create a new RDF graph with identifier 'g'
commands.parse("load file.rdf g") # import contents of local RDF file
commands.parse("triples g object http://www.w3.org/2000/01/rdf-schema#Class")
```

Thanks to the decorator `@cmd_handler`, handler functions can be
implemented wherever convenient, without worrying about additionally binding
commands syntaxes. Binding and registration can be let done automatically
by having said decorator take care of introducing the handler to the `commands.handlers` module's
namespace, and fixing its invocation for user input satisfying command syntax specifications
simply placed anywhere the docstring:

```python
from kathaireo import cmd_handler

@cmd_handler
def triples_with_object(*args, **kwargs):
	"""Returns list of triples with a specified identifier as object.
	handles:
	`triples <graphname> object <ontoclass>`"""
	[...]
```

That's it.


#### parameter configuration ####

Whenever a new command argument type is introduced by submitting an 
`<argument>` placeholder, it may also be desirable to configure its possible 
values, rather than having those determined by default value constraints. This is what the `kathaireo.commands.arguments` module is for. 
Its function `register(name, proposer=function, format=list)` adds an argument's name to a registry
and assigns to it a handler function for user input autocompletion proposals and a list
of regular expressions for value validation.

A function to be registered as an argument's autocompletion provider must 
accept two parameters: the argument's name and the prefix to be completed. It is
expected to return a list of autocompletion candidates, i.e. of legal values fitting the currently prepared user input.

When calling `commands.register(arg)` whithout passing any values for 
`proposer` or `format`, the default behaviour in autocompletion of `<arg>` 
values will be that of looking up previously entered values for `<arg>`, and
validation will merely check if input qualifies as a legal variable name, i.e. 
consists only of alphanumeric characters and underscores. To complete the above
example code, we subscribe to those default features for the argument
introduced by command `triples` as `<ontoclass>`:

```python
	commands.arguments.register('ontoclass')
```

Of course, other commands can make use of the same argument placeholder, if the
assigned configurations fit their purpose as well.

The following code is an example of overwriting the default handling. It 
implements and specifies autocompletion and validation for input submitted as
a value of `filename` arguments:

```python
import os
import re
from glob import glob

def list_files(arg, prefix):
	path = prefix.split(os.sep)[:-1]
	files = glob(os.path.join(os.sep.join(path), '*'))
	compl = [[fn for fn in files if fn.startswith(prefix)]
	arghist = commands.arguments.propose_default(arg, prefix)
	compl.extend(arghist) # suggest previous values
	return compl

commands.arguments.register('filename', proposer=list_files, 
	format=[re.compile(''(/?[^/\s]+/)*\w*\.\w+')])
```

[rdflib]: https://github.com/RDFLib/rdflib
[rdflib-sqlalchemy]: https://github.com/RDFLib/rdflib-sqlalchemy
