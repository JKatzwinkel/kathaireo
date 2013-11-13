#!/usr/bin/python
from getch import getch
import rdflib
from rdflib_sqlalchemy.SQLAlchemy import SQLAlchemy


combos=[([27,91,65], None), # up
				([27,91,66], None), # down
				([27,91,68], None), # left
				([27,91,67], None), # right
				([9], None), # tab
				([10], None),
				([27,91,49,59,53,67], None), # ctrl+right
				([27,91,49,59,53,66], None), # ctrl+down
				([27,91,49,59,53,68], None), # ctrl+left
				([27,91,49,59,53,65], None), # ctrl+up
				([127], None), #backspace
				([27,91,51,126], None), #delete
				([11], None), # ctrl+k
				([24], None), # ctrl+x
				([22], None), # ctrl+v
				]

keypaths={}
for k,f in combos:
	level=keypaths
	for i in k[:-1]:
		down = level.get(i, {})
		if not i in level:
			level[i] = down
		level = down
	level[k[-1]] = f

#https://pypi.python.org/pypi/getch

class Prompter:
	def __init__(self):
		self.history=[]
		self.buffer=None
		self.currIn=""
		self.suggestions=[]


history=[]

inputStr=""
buffer=None

def recvInput():
	global inputStr
	global buffer
	ch=getch()
	print ch
	if ord(ch) == 10:
		print "\r{}".format(inputStr)
		ret=inputStr
		inputStr=""
		return ret
	elif ord(ch) == 27:
		buffer=[27]
	elif buffer:
		buffer.append(ord(ch))
	else:
		inputStr+=ch
	print "\r{}".format(inputStr), ord(ch),
	return None

#while True:
	#input = recvInput()
