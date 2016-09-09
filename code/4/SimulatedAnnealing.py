from __future__ import print_function, division
import sys,math,random
from time import gmtime, strftime
sys.dont_write_bytecode = True
__author__ = 'ANIKETDHURI'


"""
Usage :     python SimulatedAnnealing.py                    # Here seed =1 , k=500

      :     python SimulatedAnnealing.py 30                 # Here seed=30 , k=1000

      :     python SimulatedAnnealing.py 900 1500           # Here seed=900 , k=1000
"""


class SimulatedAnnealing():

    def __init__(self ,seed=1,kmax = 100.0, x0 = 0  ,emax = -1 ):

      random.seed(seed)
      print ( "Seed = %s" % (seed))
      self.x0=x0
      self.kmax=kmax
      self.emax=emax

    @staticmethod
    def p(e, en, t):
        """
        :param e:   Current Energy
        :param en:  New Energy
        :param t:   Temperature
        :return:    P function
        """
        return pow(math.e,((e-en)/t))


    @staticmethod
    def neighbor(self,s):
        """
        Jump to neighbour +- Jump value
        :param s:   Current state
        :return:    New State
        """
        jump=20
        while True:
            s+=random.randint(-1*jump,jump)
            if  s < pow(10,5) and s > pow(10,-5):return s

    @staticmethod
    def randomNeighbor(s):
        """
        Random jump within the boundary
        :param s:   Current state
        :return:    New State
        """
        s=random.randint( int(pow(10,-5)), int(pow(10,5)))
        return s




    @staticmethod
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

        def f1(s):
            return pow(s,2)


        def f2(s):
            return pow((s-2),2)

        #print  (((f1(s)+ f2(s))- min) / (max - min))
        return ((f1(s)+ f2(s))- min) / (max - min)

    def worker (self):
        """
        Actual Simulate Annealing
        :return: xb Best state
        """
        debug=True

        x = self.x0 #Initial State
        e = self.energy(x)

        print("Initial state %i  , Initial Energy %s" %(x,e))

        xb = x              #Initial Best state
        eb = e              #Initial Best Energy
        k = self.kmax       #Reduce the temperature

        print ("\n, %04d, :%3.1f " %(self.kmax-k,eb),end="")

        while k > 0 and e > self.emax :      #While energy good enough and temperature enough
            xn = self.neighbor(self,x)
            en = self.energy(xn)
            #print ("New state %i New energy %s" %(xn,en))
            if    en < eb:
                xb = xn
                eb = en
                if ( debug ): print ("!",end="")
            if    en < e:
                x = xn
                e = en
                if ( debug ):print ("+",end="")
            elif self.p(e, en, k/self.kmax) < random.random():

                #Initial Algorithm had this step but removed for efficiency of jumps
                #x = xn
                #e = en


                x=self.randomNeighbor(xn)
                e=self.energy(x)

                if ( debug ): print ("?",end="")
            if ( debug ):print  (".",end="")
            k = k - 1

            if k % 25 == 0: print ("\n, %04d, :%3.1f " %(self.kmax-k,eb),end="")

        #All done
        print ("\n\n:e %s \n:x %s" %(eb,xb))

print("#########saDemo############")
print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print ("!!! Schaffer")



if len(sys.argv)>2:
    SimulatedAnnealing(int(sys.argv[1]), int(sys.argv[2]),random.randint(int(pow(10,-5)),int(pow(10,5) ))).worker()
elif len(sys.argv)>1:
     SimulatedAnnealing(int(sys.argv[1]), 1000,random.randint(int(pow(10,-5)),int(pow(10,5) ))).worker()
else:
     SimulatedAnnealing(1, 700,random.randint(int(pow(10,-5)),int(pow(10,5) )),).worker()


