from __future__ import division
import sys
from model import Model
from model import Decision
sys.dont_write_bytecode = True

class Osyczka2(Model):
	def __init__(self):
		objectives = [obj_one, obj_two]
		constraints = [con_one, con_two, con_three, con_four, con_five, con_six]
		decisions = [Decision(0,10), Decision(0,10), Decision(1,5), Decision(0,6), Decision(1,5), Decision(0,10)]
		Model.__init__(self, objectives, constraints, decisions)

def obj_one(v):
	f1 = (-1 * ((25*((v[0]-2)**2)) + ((v[1]-2)**2) + (((v[2]-1)**2)*((v[3]-4)**2)) + ((v[4]-1)**2)))
	return f1
def obj_two(v):
	f2 = v[0]**2 + v[1]**2 + v[2]**2 + v[3]**2 + v[4]**2 + v[5]**2
	return f2
def con_one(v):
	return (v[0]+v[1]-2) >= 0
def con_two(v):
	return (6-v[0]-v[1]) >= 0
def con_three(v):
	return (2-v[1]+v[0]) >= 0
def con_four(v):
	return (2-v[0]+(3*v[1])) >= 0
def con_five(v):
	return (4-((v[2]-3)**2)-v[3]) >= 0
def con_six(v):
	return (((v[4]-3)**2)+v[5]-4) >= 0