from __future__ import print_function, division

import time
import sys,math,random
from time import gmtime, strftime


from model.osyczka2 import Osyczka2
from model.kursawe import Kursawe
sys.dont_write_bytecode = True

from model.schaffer import Schaffer

sys.dont_write_bytecode = True
__author__ = 'ANIKETDHURI'


"""
Usage :     python SimulatedAnnealing.py                    # Here seed =1 , k=500

      :     python SimulatedAnnealing.py 30                 # Here seed=30 , k=1000

      :     python SimulatedAnnealing.py 900 1500           # Here seed=900 , k=1000
"""
kmax = 100
x0 = [0,0,0,0,0]
emax = -1
seed = 1
def sa(m):
    random.seed(seed)
    #say(m.evaluate( m.any() ) )
    #say(m.decisions[0].low)
    #say(m.ok([100000000,0,0]) )
    #m.any() give any solution on the bound

    x= x0
    e= energy(x)

    say("Initial state %i  , Initial Energy %s" %(x[0],e))

    xb = x              #Initial Best state
    eb = e              #Initial Best Energy
    k = kmax       #Reduce the temperature

    say("\n, %04d, :%3.1f " %( kmax - k , eb ))

    while k > 0 and e > emax :
        xn = neighbor( m,x )
        en = energy( xn )

        if e < eb :
            xb = xn
            eb = en
        if    en < e:
            x = xn
            e = en
        elif p(e, en, k/kmax) < random.random():
            x = randomNeighbor(m,xn)
            e = energy(x)

        k = k - 1

        if k % 25 == 0: say ("\n, %04d, :%3.1f " %(kmax-k,eb))

    #All done
    say ("\n\n:e %s \n:x %s" %(eb,xb))




def p(e, en, t):
    """
    :param e:   Current Energy
    :param en:  New Energy
    :param t:   Temperature
    :return:    P function
    """
    return pow(math.e,((e-en)/t))

def neighbor(m,s):
    """
    Jump to neighbour +- Jump value
    :param s:   Current state
    :return:    New State
    """
    jump=20
    while True:
        s=[ ( i + random.randint(-1*jump,jump)) for i in s]
        if  m.ok(s):return s

def randomNeighbor(m,s):
    """
    Random jump within the boundary
    :param s:   Current state
    :return:    New State
    """
    s=m.any()
    if  m.ok(s):return s




def energy(s):
    """
    Calculate Energy
    :param s:   Current state
    :return:    Energy at current state
    """
    #Min and Max Calculated over 10000 samples
    #min=87364.0
    #max=19702713034.0

    #Working Min Max Calculated over series of experiments
    min=80000
    max=10000000
    s=s[0]
    def f1(s):
        return pow(s,2)


    def f2(s):
        return pow((s-2),2)

    #print  (((f1(s)+ f2(s))- min) / (max - min))
    return ((f1(s)+ f2(s))- min) / (max - min)


def say(x):
    sys.stdout.write(str(x))
    sys.stdout.flush()

if __name__ == "__main__":
        sa(Schaffer())
