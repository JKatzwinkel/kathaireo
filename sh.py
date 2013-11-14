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
#print("\033[6;3HHello")

class Prompter:
	def __init__(self):
		self.history=[]
		self.buf=[]
		self.keylvl=keypaths
		self.currIn=""
		self.suggestions=[]

	def waitForInput(self):
		ch = getch()
		if ord(ch) in self.keylvl:
			self.buf.append(ord(ch))
			self.keylvl=self.keylvl[ord(ch)]
		else:
			self.keylvl=keypaths
			self.buf=[]
		if len(self.buf)<1:
			print ch
		if not self.keylvl:
			self.keylvl=keypaths
			self.buf=[]


	def onCombo(ch):
		level=keypaths
		if not buf:
			globals()["buf"] = [ord(ch)]
		for k in buf:
			if type(level) is dict:
				level = level.get(k)
		if not level:
			globals()["buf"] = None
			return False
		if type(level) != dict:
			globals()["buf"] = None
		else:
			buf.append(ord(ch))
		return True




prompt = Prompter()

#while True:
	#inp = prompt.waitForInput()

# input completion:
# http://stackoverflow.com/q/5637124/1933494
# http://stackoverflow.com/a/7821956/1933494
# http://docs.python.org/2/library/readline.html

import readline, glob
def complete(text, state):
    return (glob.glob(text+'*')+[None])[state]

readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
readline.set_completer(complete)
raw_input('file? ')
