kathaireo
=========

Kathaireo is intended to become an interactive shell 
for operating on RDF and stuff. Its makes use of `rdflib` and
`rdflib_sqlalchemy`. 

Main goal is to provide a fast and slim tool
for easier work on RDF, OWL, etc. ontologies, including imports local 
and remote sources, persistent storage with Sqlite etc., 
namespace support and convenience features like context-aware 
autocompletion and reference resolution.

Custom commands can easily be added to extend the list of predefined ones.
This might make it easier to hack specialized plugins at some point.

Registration of a new command works like this:

  import commands
  import rdf
  
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
  
