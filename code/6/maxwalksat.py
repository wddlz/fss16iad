from __future__ import division
import sys
import math
import random
import time

from model.osyczka2 import Osyczka2
from model.kursawe import Kursawe
sys.dont_write_bytecode = True

MAX_TRIES = 15;
MAX_CHANGES = 50;
P = 0.5

"""
Performs maxwalksat optimization
"""

def mws(m):
    best_soln = m.any()
    for i in xrange(MAX_TRIES):
        new_soln = m.any()
        say(new_soln); say(":"); say(m.evaluate(new_soln)); say(", ")
        say("?")
        for j in xrange(MAX_CHANGES):
            if(m.evaluate(new_soln) < m.evaluate(best_soln)):
                say("!")
                best_soln = new_soln[:]
            if P < random.random():
                old_soln = new_soln[:]
                new_soln = part_mutate(m, new_soln)
            else:
                old_soln = new_soln[:]
                new_soln = mutate_soln(m, new_soln)
            if(m.evaluate(new_soln) < m.evaluate(best_soln)):
                say("!")
                best_soln = new_soln[:]
            elif(m.evaluate(new_soln) < m.evaluate(old_soln)):
                say("+")
            else:
                say(".")
        say(" ,"); say(best_soln); say(":"); say(m.evaluate(best_soln))
        say("\n")
    print("solution : %s\nscore : %s" %(str(best_soln), str(m.evaluate(best_soln))))

"""
Mutates one decision in the solution
"""
def part_mutate(m, soln):
    decs = m.decisions
    i = random.randint(0, len(soln)-1)
    soln[i] = random.randint(decs[i].low, decs[i].high)
    if m.ok(soln):
    	return soln
    return part_mutate(m, soln)

"""
Mutates the entire solution
"""
def mutate_soln(m, soln):
    for i in xrange(len(soln)):
        soln[i] = dec_mutate(m, soln, i)
        while not m.ok(soln):
            soln[i] = dec_mutate(m, soln, i)
    return soln

"""
Mutates the i-th decision of the solution
"""
def dec_mutate(m, soln, i):
    d = soln[i]
    dc = (m.decisions[i].high - m.decisions[i].low)/10

    if(random.randint(0,1) == 0):
        d = d - dc
        if(d < m.decisions[i].low):
            d = m.decisions[i].low
    else:
        d = d + dc
        if(d > m.decisions[i].high):
            d = m.decisions[i].high
    return d

def say(x):
    sys.stdout.write(str(x))
    sys.stdout.flush()