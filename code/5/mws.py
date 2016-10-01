from __future__ import division
import sys
import math
import random
import time

__author__="Karan Jadhav"

"""
Output:
<random-solution>:<score>, ?(random-jump) !(better-than-best) +(better-than-current) .(worse-than-current) ,<best-solution>:<score>
"""

MAX_TRIES = 15;
MAX_CHANGES = 50;
MAX_MUTATES = 10;
P = 0.5
DECISIONS = [[0,10],[0,10],[0,5],[0,6],[0,5],[0,10]]

"""
Performs maxwalksat optimization
"""
def maxwalksat():
    best_soln = random_soln()
    for i in xrange(MAX_TRIES):
        new_soln = random_soln()
        say(new_soln); say(":"); say(score(new_soln)); say(", ")
        say("?")
        for j in xrange(MAX_CHANGES):
            if(score(new_soln) < score(best_soln)):
                say("!")
                best_soln = new_soln[:]
            if P < r():
                old_soln = new_soln[:]
                new_soln = part_mutate(new_soln)
            else:
                old_soln = new_soln[:]
                new_soln = mutate_soln(new_soln)
            if(score(new_soln) < score(best_soln)):
                say("!")
                best_soln = new_soln[:]
            elif(score(new_soln) < score(old_soln)):
                say("+")
            else:
                say(".")
        say(" ,"); say(best_soln); say(":"); say(score(best_soln))
        say("\n")
    print("solution : {}\nscore : {}".format(best_soln, score(best_soln)))

"""
Mutates one decision in the solution
"""
def part_mutate(soln):
    max_muts = MAX_MUTATES
    i = random.randint(0, len(soln)-1)
    soln[i] = random.randint(DECISIONS[i][0], DECISIONS[i][1])
    while not withinConstr(soln):
        max_muts -= 1
        soln[i] = random.randint(DECISIONS[i][0], DECISIONS[i][1])
    return soln
    
"""
Mutates the i-th decision of the solution
"""
def dec_mutate(soln, i):
    d = soln[i]
    dc = (DECISIONS[i][1]-DECISIONS[i][0])/10
    if(random.randint(0,1) == 0):
        d = d - dc
        if(d < DECISIONS[i][0]):
            d = DECISIONS[i][0]
    else:
        d = d + dc
        if(d > DECISIONS[i][1]):
            d = DECISIONS[i][1]
    return d
    
"""
Mutates the entire solution
"""
def mutate_soln(soln):
    for i in xrange(len(soln)):
        max_muts = MAX_MUTATES
        soln[i] = dec_mutate(soln, i)
        while not withinConstr(soln):
            max_muts -= 1
            soln[i] = dec_mutate(soln, i)
    return soln
                    
"""
Generates a random solution within constraints
"""
def random_soln():
    soln = []
    for i in xrange(len(DECISIONS)):
        r = DECISIONS[i]
        soln.append(random.randint(r[0], r[1]))
    if withinConstr(soln):
        return soln
    return random_soln()
    
"""
Checks if solution is within constraints
"""
def withinConstr(soln):
    if(soln[0]+soln[1]-2) < 0:
        return False
    if(6-soln[0]-soln[1]) < 0:
        return False
    if(2-soln[1]+soln[0]) < 0:
        return False
    if(2-soln[0]+(3*soln[1])) < 0:
        return False
    if(4-((soln[2]-3)**2)-soln[3]) < 0:
        return False
    if(((soln[4]-3)**3)+soln[5]-4) < 0:
        return False
    return True
    
"""
Calculates score based on the 2 model functions
"""
def score(soln):
    return f1(soln[0],soln[1],soln[2],soln[3],soln[4]) + f2(soln[0],soln[1],soln[2],soln[3],soln[4],soln[5])
    
def f1(x1, x2, x3, x4, x5):
    return (-1 * ((25*((x1-2)**2)) + ((x2-2)**2) + (((x3-1)**2)*((x4-4)**2)) + ((x5-1)**2)))
    
def f2(x1,x2,x3,x4,x5,x6):
    return (x1**2 + x2**2 + x3**2 + x4**2 + x5**2 + x6**2)
    
def r():
    return random.random()
    
def say(x):
    sys.stdout.write(str(x))
    sys.stdout.flush()
        
if __name__=="__main__":
    maxwalksat()