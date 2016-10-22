from __future__ import division
import sys
import random
import operator
import math
from model.schaffer import Schaffer
from model.osyczka2 import Osyczka2
from model.kursawe import Kursawe
sys.dont_write_bytecode = True

k_max = 100
max_min_iters = 100
e_max = 0
e_min = 0

def sa(m):
	"""
	Performs simulated annealing optimization
	@params: model
	@return: None
	"""
	set_max_min(m)
	s = m.any()
	e = m.evaluate(s)
	sb = s
	eb = e
	k = 1
	while k < k_max and e > e_min:
		if k == 1 or k%50 == 0:
			say(sb); say(":"); say(eb); say(", ")
		sn = neighbour(m, s)
		en = m.evaluate(sn)
		if en < eb:
			sb = sn
			eb = en
			say("!")
		if en < e:
			s = sn
			e = en
			say("+")
		elif prob(e, en, k/k_max) < random.random():
			s = sn
			e = en
			say("?")
		say(".")
		k += 1
		if k%50 == 0:
			say(" ,"); say(sb); say(":"); say(eb)
			say("\n")
	print
	print("solution : {}".format(sb))
	print("score : {}".format(eb))

def neighbour(m, s):
	"""
	Generates neighbour solutions within +/- 10 percent of the decision bounds till a valid solution is found
	@params: model, solution
	@return: neighbour solution
	"""
	valid, sn = act_neighbour(m, s)
	while not valid:
		valid, sn = act_neighbour(m, s)
	return sn

def act_neighbour(m, s):
	"""
	Actual neighbour generation solution
	@params: model, solution
	@return: valid solution boolean, neighbour solution
	"""
	sn = []
	for i in xrange(len(m.decisions)):
		d = m.decisions[i]
		dc = (d.high-d.low)/10
		if(random.randint(0,1) == 0):
			dn = s[i] - dc
			if(dn < m.decisions[i].low):
				dn = m.decisions[i].low
		else:
			dn = s[i] + dc
			if(dn > m.decisions[i].high):
				dn = m.decisions[i].high
		sn.append(dn)
	return m.ok(sn), sn

def map_energy(e):
	"""
	Maps energy between 0-1
	@params: energy
	@returns: energy value between 0-1
	"""
	return (e-e_min)/(e_max-e_min)

def prob(e, en, k_ratio):
	"""
	Calculates probability based on new & current energy and temperature k_ratio
	@params: current energy, new energy, temperature ratio
	@return: probabilty between 0-1
	"""
	e = map_energy(e)
	en = map_energy(en)
	return math.exp((e-en)/k_ratio)

def set_max_min(model):
	"""
	Sets max and min energies for mapping energy
	@params: model
	@return: None
	"""
	global max_min_iters
	global e_max, e_min
	ss = []
	for i in xrange(max_min_iters):
		ss.append(model.evaluate(model.any()))
	e_max = max(ss)
	e_min = min(ss)

def say(x):
	"""
	Print to same line
	@param: string to be printed
	@return: None
	"""
	sys.stdout.write(str(x))
	sys.stdout.flush()