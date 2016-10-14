from __future__ import division
import sys
from model import Model
from model import Decision
sys.dont_write_bytecode = True

class Schaffer(Model):
	def __init__(self):
		objectives = [obj_one, obj_two]
		decisions = [Decision(-100000, 100000)]
		Model.__init__(self, objectives, None, decisions)

def obj_one(s):
	return s[0]**2

def obj_two(s):
	return (s[0]-2)**2
