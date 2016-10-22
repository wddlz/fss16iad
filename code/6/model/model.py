from __future__ import division
import sys
import random
import time
sys.dont_write_bytecode = True

class Model(object):
	def __init__(self, objectives, constraints, decisions):
		self.objectives = objectives
		self.constraints = constraints
		self.decisions = decisions

	def evaluate(self, solution):
		"""
		Calculates the score for a given solution using all objectives
		@params: solution of decisions to be evaluated
		@return: score for solution
		"""
		total = 0
		for obj in self.objectives:
			total = total + obj(solution)
		return total

	def ok(self, solution):
		"""
		Checks if solution is within constraints
		@params: solution of decisions to be evaluated
		@return: boolean valid solution 
		"""
		if self.constraints != None:
			for con in self.constraints:
				if not con(solution):
					return False
		return True

	def any(self):
		"""
		Generates a random solution till one within constraints is found
		@param: None
		@return: solution of decisions
		"""
		valid, soln = self.act_rand_soln()
		while not valid:
			valid, soln = self.act_rand_soln()
		return soln

	def act_rand_soln(self):
		"""
		Generates a solultion and checks if it is within constraints
		@param: None
		@return: boolean valid solution, solution of decisions
		"""
		soln = []
		for dec in self.decisions:
			soln.append(random.randint(dec.low, dec.high))
		return self.ok(soln), soln

class Decision:
	def __init__(self, low, high):
		self.low = low
		self.high = high
