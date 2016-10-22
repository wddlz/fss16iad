from __future__ import division
import sys
import math
from model import Model
from model import Decision
sys.dont_write_bytecode = True

class Kursawe(Model):
	def __init__(self):
		objectives = [obj_one, obj_two]
		decisions = [Decision(-5,5), Decision(-5,5), Decision(-5,5)]
		Model.__init__(self, objectives, None, decisions)

def obj_one(s):
	total = 0
	for i in xrange(len(s)-1):
		sqrt_part = ((s[i])**2) + ((s[i+1])**2)
		pow_part = (-0.2 * sqrt_part)
		exp_part = math.exp(pow_part)
		value = -10 * exp_part
		total += value
	return total

def obj_two(s):
	a = 0.8
	b = 1
	total = 0
	for i in xrange(len(s)):
		term1 = abs(s[i])**a
		term2 = 5 * math.sin((s[i])**b)
		value = term1 + term2
		total += value
	return total