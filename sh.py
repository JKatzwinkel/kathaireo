#!/usr/bin/python
from getch import getch
import rdflib
from rdflib_sqlalchemy.SQLAlchemy import SQLAlchemy


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

while True:
	input = recvInput()
