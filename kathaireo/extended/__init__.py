#!/usr/bin/python
# -*- coding: utf-8 -*- 
"""\
Some additional functionality, e.g. for debugging reasons."""
__docformat__ = "restructuredtext en"
__version__ = "0.0.2-dev"


from .. import commands, cmd_handler

@cmd_handler
def ls_cmd(*args, **kwargs):
	"""List all registered commands.
	handles:
	`commands`
	`show commands`"""
	cmds = []
	heads = {k:v for k,v in commands.cmdict.items()}
	going = True
	while going:
		deeper = {}
		for path, head in heads.items():
			for k, v in head.items():
				np = ' '.join([path, k])
				if type(v) is dict:
					deeper[np] = v
					#print path, k
				else:
					cmds.append(np)
			del heads[path]
		heads.update(deeper)
		going = len(deeper)>0
	return '\n'.join(sorted(cmds))



