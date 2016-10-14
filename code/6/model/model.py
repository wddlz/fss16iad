from __future__ import division
import sys
import random
sys.dont_write_bytecode = True

class Model(object):
	def __init__(self, objectives, constraints, decisions):
		self.objectives = objectives
		self.constraints = constraints
		self.decisions = decisions

	def evaluate(self, solution):
		total = 0
		for obj in self.objectives:
			total = total + obj(solution)
		return total

	def ok(self, solution):
		if self.constraints != None:
			for con in self.constraints:
				if not con(solution):
					return False
		return True

	def any(self):
		flag, soln = self.act_rand_soln()
		while not flag:
			flag, soln = self.act_rand_soln()
		return soln

	def act_rand_soln(self):
		soln = []
		for dec in self.decisions:
			soln.append(random.randint(dec.low, dec.high))
		return self.ok(soln), soln

class Decision:
	def __init__(self, low, high):
		self.low = low
		self.high = high