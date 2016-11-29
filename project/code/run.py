import ast
import random
import sys
import subprocess
import os,time
import uuid
import logging
import parse
import json
import array
from contextlib import contextmanager
import numpy
import time

from hypervolume import *

from prism import getObjectives

from savestat import genFileName,insert,insertnl

from math import sqrt

from deap import algorithms
from deap import base
from deap import benchmarks
from deap.benchmarks.tools import diversity, convergence#, hypervolume
from deap import creator
from deap import tools
import matplotlib.pyplot as plt
import numpy

import redis

################################Configurations ##################################################

save_figure = False # To save plots from each graph

simulatePrism = True


#################################################################################################




calls = 0 
hits = 0
hashmap={}
identifier = "temp"

logging.basicConfig(filename='project.log',filemode='w',format='%(asctime)s [%(filename)s:%(lineno)s - %(funcName)s() ] : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

B_RP = (1000,2000)
S_RP = (1,100)
B_IP = S_RP
S_IP = B_RP
Tb = (50,100)
TbB =(20,40)
Ts = (50,100)
TsB = (48,49)
bCinc = (100,200)
bBinc = (1,3)
sCdec = (100,200)
sBdec = (1,3)
Kb = (1,2)
Ks = (8,9)
Offset = (10000,15000)

#prism_path = "/home/adhuri/prism-4.3.1-linux64/bin/prism"
#pop_size = 8

@contextmanager
def duration():
  t1 = time.time()
  yield
  t2 = time.time()
  print("\n" + "-" * 72)
  print("# Runtime: %.3f secs" % (t2-t1))


def ok(decs):
    if(decs[2] >= decs[0]):return False     #B_IP >= B_RP
    if(decs[1] >= decs[3]):return False     #S_RP >= S_IP
    if(decs[4] <= 0):return False           #Tb <= 0
    if(decs[6] <= 0):return False           #Ts <= 0
    if(decs[5] >= decs[4]):return False     # TbB >= Tb
    if(decs[7] >= decs[6]):return False     #TsB >= Ts

    return True

def aop_decs():
    decs = gen_decs()
    while not ok(decs):
        decs = gen_decs()
    return decs

def gen_decs():
	b_rp = random.randint(B_RP[0], B_RP[1])
	s_rp = random.randint(S_RP[0], S_RP[1])
	tb = random.randint(Tb[0], Tb[1])
	tbb = random.randint(TbB[0], TbB[1])
	ts = random.randint(Ts[0], Ts[1])
	tsb = random.randint(TsB[0], TsB[1])
	bcinc = random.randint(bCinc[0], bCinc[1])
	bbinc = random.randint(bBinc[0], bBinc[1])
	scdec = random.randint(sCdec[0], sCdec[1])
	sbdec = random.randint(sBdec[0], sBdec[1])
	kb = random.randint(Kb[0], Kb[1])
	ks = random.randint(Ks[0], Ks[1])
	offset = random.randint(Offset[0], Offset[1])
	return [b_rp, s_rp, s_rp, b_rp, tb, tbb, ts, tsb, bcinc, bbinc, scdec, sbdec,  kb, ks, offset]


creator.create("Fitness", base.Fitness, weights=(4.0, -1.0, 1.0),crowding_dist=None)
creator.create("Individual", list, fitness=creator.Fitness)

toolbox = base.Toolbox()
toolbox.register("decs", aop_decs)
toolbox.register("gen_one", tools.initIterate, creator.Individual, toolbox.decs)
toolbox.register("population", tools.initRepeat, list, toolbox.gen_one)

#pop = toolbox.population(n=pop_size)


def prism(individual):
	global simulatePrism
	r = redis.StrictRedis(host='152.46.19.201', port=6379, db=0)
	#Testing prism call 
	global hashmap,calls,hits
	# Empty individual decisions
	calls += 1

	if individual == []:return 0,0,0
	
	#Create string
	string = repr(individual)
	
	try:
		cache = r.get(string)

		#print cache
		# Put in hashmap
		if cache is not None:
			logging.debug(string + " -Already in hashmap ")
			hits +=1 
			return ast.literal_eval(cache)

		else:
			logging.debug(string + " Adding in hashmap ")
		
			if simulatePrism == False:
				#global prism_path
				#filename = parse.call_prism(prism_path,individual)
				#evaluated_results =parse.Parse(filename).get_output()
				#print evaluated_results
	
				evaluated_results = getObjectives(individual) # online call

				logging.info("Evaluated results :"+repr( evaluated_results) +" ,for :"+repr(individual))
		
			else :
	
				#Simulate evaluate results
				evaluated_results = (1,random.random(),random.random())
	
			if evaluated_results:
				r.set(string, evaluated_results)
			else:
				r.set(string, (0,0,0))

			return ast.literal_eval(r.get(string))
	except Exception as e: 
		print (" Caching is disabled. Start redis on 152.46.19.201 : ",e)
		sys.exit()
		
def evaluateInd(individual):
    # Do some computation
	#print "Individual", individual;
	return prism(individual)
	#return (1,random.randint(0,4),random.randint(0,4))






def main_nsga2(algorithm="NSGA2",seed=None,NGEN=100,MU=100):
    random.seed(seed)
    #NGEN       # Generation
    #MU     # Population Size
    CXPB = 0.9


    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutUniformInt, low = 0 , up = 1, indpb=0.01)
    toolbox.register("select", tools.selNSGA2)
    toolbox.register("evaluate", evaluateInd)

	
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean, axis=0)
    stats.register("std", numpy.std, axis=0)
    stats.register("min", numpy.min, axis=0)
    stats.register("max", numpy.max, axis=0)
    
    logbook = tools.Logbook()
    logbook.header = "gen", "evals", "std", "min", "avg", "max"
    
    pop = toolbox.population(n=MU)
    #algorithm = "NSGA2"
    print "Algorithm = ",algorithm
    print "Generation = ",NGEN
    print "Population Size = ",MU
    referencePoint = (2.0, 0, 0)
    hv = InnerHyperVolume(referencePoint)
    #front = [(1.0, 0.5128205128205128, 195.0),(1.0, 2.7732997481108312, 397.0),(1.0, 0.7787356321839081, 348.0),(1.0, 2.7732997481108312, 397.0),(1.0, 0.5339233038348082, 339.0),(1.0, 0.5128205128205128, 195.0),(1.0, 0.5128205128205128, 195.0),(1.0, 0.5128205128205128, 195.0)]

    global identifier	
    statfile_purchase = genFileName(algorithm,"purchase",NGEN,MU,identifier) # Stat Generation
    insert(statfile_purchase,algorithm+"_gen"+str(NGEN)+"_pop"+str(MU))

  
    statfile_utility = genFileName(algorithm,"utility",NGEN,MU,identifier) # Stat Generation
    insert(statfile_utility,algorithm+"_gen"+str(NGEN)+"_pop"+str(MU))

    statfile_time = genFileName(algorithm,"time",NGEN,MU,identifier) # Stat Generation
    insert(statfile_time,algorithm+"_gen"+str(NGEN)+"_pop"+str(MU))


    #statfile_hypervolume = genFileName(algorithm,"hypervolume",NGEN,MU) # Stat Generation
    #insert(statfile_hypervolume,algorithm+"_gen"+str(NGEN)+"_pop"+str(MU))


    #statfile_spread = genFileName(algorithm,"spread",NGEN,MU,identifier) # Stat Generation
    #insert(statfile_spread,algorithm+"_gen"+str(NGEN)+"_pop"+str(MU))

    #statfile_igd = genFileName(algorithm,"igd",NGEN,MU,identifier) # Stat Generation
    #insert(statfile_igd,algorithm+"_gen"+str(NGEN)+"_pop"+str(MU))

    print ("Initial Population")
    for p in pop:
	print p



    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    # This is just to assign the crowding distance to the individuals
    # no actual selection is done
    pop = toolbox.select(pop, len(pop))
    
    record = stats.compile(pop)
    logbook.record(gen=0, evals=len(invalid_ind), **record)
    print(logbook.stream)

    # Begin the generational process
    for gen in range(1, NGEN):
        # Vary the population
        offspring = tools.selTournamentDCD(pop, len(pop))
        offspring = [toolbox.clone(ind) for ind in offspring]
        
        for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
            if random.random() <= CXPB:
                toolbox.mate(ind1, ind2)
            
            toolbox.mutate(ind1)
            toolbox.mutate(ind2)
            del ind1.fitness.values, ind2.fitness.values
        
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Select the next generation population
        oldpop = pop
	#map(lambda x:insert(statfile_purchase,str(x.fitness.values[0])),oldpop)
	#map(lambda x:insert(statfile_utility,str(x.fitness.values[1])),oldpop)
	#map(lambda x:insert(statfile_time,str(x.fitness.values[2])),oldpop)
	
	#Only final generation required
        #volume = hv.compute([x.fitness.values for x in oldpop if x.fitness.values[0]==1.0])
        #print volume
	#insert(statfile_hypervolume,str(volume))
	#insert(statfile_spread,str(spread(oldpop)))
	#insert(statfile_igd,str(igd(oldpop)))
        

	pop = toolbox.select(pop + offspring, MU)
        record = stats.compile(pop)
        logbook.record(gen=gen, evals=len(invalid_ind), **record)
        print(logbook.stream)
	
	

        if stop_early(oldpop, pop):
            print("Stopping generation early, no purchases")
            break
	
    map(lambda x:insert(statfile_purchase,str(x.fitness.values[0])),pop)
    insertnl(statfile_purchase)	
    map(lambda x:insert(statfile_utility,str(x.fitness.values[1])),pop)
    insertnl(statfile_utility)	
    map(lambda x:insert(statfile_time,str(x.fitness.values[2])),pop)
    insertnl(statfile_time)	
    
    volume = hv.compute([x.fitness.values for x in pop if x.fitness.values[0]==1.0])

    print "Hypervolume = ",volume
    #insert(statfile_hypervolume,str(volume))
    #insert(statfile_spread,str(spread(oldpop)))
    #insertnl(statfile_spread)	
    #insert(statfile_igd,str(igd(oldpop)))
    #insertnl(statfile_igd)	


    r = redis.StrictRedis(host='152.46.19.201', port=6379, db=0)
    r.flushall() # Remove all keys once done 
    

    #print("Final population hypervolume is %f" % hypervolume(pop, [11.0, 11.0]))

    return pop, logbook

#=======SPEA2=======#
def main_spea2(algorithm="SPEA2",seed=None,NGEN=100,MU=100):
    random.seed(seed)
    #NGEN       # Generation
    #MU     # Population Size
    CXPB = 0.9


    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutUniformInt, low = 0 , up = 1, indpb=0.01)
    toolbox.register("select", tools.selSPEA2)
    toolbox.register("evaluate", evaluateInd)



    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean, axis=0)
    stats.register("std", numpy.std, axis=0)
    stats.register("min", numpy.min, axis=0)
    stats.register("max", numpy.max, axis=0)
    
    logbook = tools.Logbook()
    logbook.header = "gen", "evals", "std", "min", "avg", "max"
    
    pop = toolbox.population(n=MU)
    #algorithm = "NSGA2"
    print "Algorithm = ",algorithm
    print "Generation = ",NGEN
    print "Population Size = ",MU
    referencePoint = (2.0, 0, 0)
    hv = InnerHyperVolume(referencePoint)
    #front = [(1.0, 0.5128205128205128, 195.0),(1.0, 2.7732997481108312, 397.0),(1.0, 0.7787356321839081, 348.0),(1.0, 2.7732997481108312, 397.0),(1.0, 0.5339233038348082, 339.0),(1.0, 0.5128205128205128, 195.0),(1.0, 0.5128205128205128, 195.0),(1.0, 0.5128205128205128, 195.0)]

    global identifier	
    statfile_purchase = genFileName(algorithm,"purchase",NGEN,MU,identifier) # Stat Generation
    insert(statfile_purchase,algorithm+"_gen"+str(NGEN)+"_pop"+str(MU))

  
    statfile_utility = genFileName(algorithm,"utility",NGEN,MU,identifier) # Stat Generation
    insert(statfile_utility,algorithm+"_gen"+str(NGEN)+"_pop"+str(MU))

    statfile_time = genFileName(algorithm,"time",NGEN,MU,identifier) # Stat Generation
    insert(statfile_time,algorithm+"_gen"+str(NGEN)+"_pop"+str(MU))


    #statfile_hypervolume = genFileName(algorithm,"hypervolume",NGEN,MU) # Stat Generation
    #insert(statfile_hypervolume,algorithm+"_gen"+str(NGEN)+"_pop"+str(MU))


    #statfile_spread = genFileName(algorithm,"spread",NGEN,MU,identifier) # Stat Generation
    #insert(statfile_spread,algorithm+"_gen"+str(NGEN)+"_pop"+str(MU))

    #statfile_igd = genFileName(algorithm,"igd",NGEN,MU,identifier) # Stat Generation
    #insert(statfile_igd,algorithm+"_gen"+str(NGEN)+"_pop"+str(MU))

    print ("Initial Population")
    for p in pop:
	print p



    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    # This is just to assign the crowding distance to the individuals
    # no actual selection is done
    pop = toolbox.select(pop, len(pop))
    
    record = stats.compile(pop)
    logbook.record(gen=0, evals=len(invalid_ind), **record)
    print(logbook.stream)

    # Begin the generational process
    for gen in range(1, NGEN):
        # Vary the population
        offspring = tools.selTournamentDCD(pop, len(pop))
        offspring = [toolbox.clone(ind) for ind in offspring]
        
        for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
            if random.random() <= CXPB:
                toolbox.mate(ind1, ind2)
            
            toolbox.mutate(ind1)
            toolbox.mutate(ind2)
            del ind1.fitness.values, ind2.fitness.values
        
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Select the next generation population
        oldpop = pop
	#map(lambda x:insert(statfile_purchase,str(x.fitness.values[0])),oldpop)
	#map(lambda x:insert(statfile_utility,str(x.fitness.values[1])),oldpop)
	#map(lambda x:insert(statfile_time,str(x.fitness.values[2])),oldpop)
	
	#Only final generation required
        #volume = hv.compute([x.fitness.values for x in oldpop if x.fitness.values[0]==1.0])
        #print volume
	#insert(statfile_hypervolume,str(volume))
	#insert(statfile_spread,str(spread(oldpop)))
	#insert(statfile_igd,str(igd(oldpop)))
        

	pop = toolbox.select(pop + offspring, MU)
        record = stats.compile(pop)
        logbook.record(gen=gen, evals=len(invalid_ind), **record)
        print(logbook.stream)
	
	

        if stop_early(oldpop, pop):
            print("Stopping generation early, no purchases")
            break
	
    map(lambda x:insert(statfile_purchase,str(x.fitness.values[0])),pop)
    insertnl(statfile_purchase)	
    map(lambda x:insert(statfile_utility,str(x.fitness.values[1])),pop)
    insertnl(statfile_utility)	
    map(lambda x:insert(statfile_time,str(x.fitness.values[2])),pop)
    insertnl(statfile_time)	
    
    volume = hv.compute([x.fitness.values for x in pop if x.fitness.values[0]==1.0])

    print "Hypervolume = ",volume
    #insert(statfile_hypervolume,str(volume))
    #insert(statfile_spread,str(spread(oldpop)))
    #insertnl(statfile_spread)	
    #insert(statfile_igd,str(igd(oldpop)))
    #insertnl(statfile_igd)	


    r = redis.StrictRedis(host='152.46.19.201', port=6379, db=0)
    r.flushall() # Remove all keys once done 
    

    #print("Final population hypervolume is %f" % hypervolume(pop, [11.0, 11.0]))

    return pop, logbook


#=======DE========#

def main_de(algorithm="DE",seed=None,NGEN=100,MU=100):
    random.seed(seed)
    #NGEN       # Generation
    #MU     # Population Size
    # Differential evolution parameters
    CR = 0.3
    F = 0.75
    # Problem dimension
    NDIM = 3

    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutUniformInt, low = 0 , up = 1, indpb=0.01)
    toolbox.register("select", tools.selRandom, k=3)
    toolbox.register("evaluate", evaluateInd)

    hof = tools.HallOfFame(MU)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean, axis=0)
    stats.register("std", numpy.std, axis=0)
    stats.register("min", numpy.min, axis=0)
    stats.register("max", numpy.max, axis=0)
    
    logbook = tools.Logbook()
    logbook.header = "gen", "evals", "std", "min", "avg", "max"
    
    pop = toolbox.population(n=MU)
    #algorithm = "NSGA2"
    print "Algorithm = ",algorithm
    print "Generation = ",NGEN
    print "Population Size = ",MU
    referencePoint = (2.0, 0, 0)
    hv = InnerHyperVolume(referencePoint)
    #front = [(1.0, 0.5128205128205128, 195.0),(1.0, 2.7732997481108312, 397.0),(1.0, 0.7787356321839081, 348.0),(1.0, 2.7732997481108312, 397.0),(1.0, 0.5339233038348082, 339.0),(1.0, 0.5128205128205128, 195.0),(1.0, 0.5128205128205128, 195.0),(1.0, 0.5128205128205128, 195.0)]

    global identifier	
    statfile_purchase = genFileName(algorithm,"purchase",NGEN,MU,identifier) # Stat Generation
    insert(statfile_purchase,algorithm+"_gen"+str(NGEN)+"_pop"+str(MU))

  
    statfile_utility = genFileName(algorithm,"utility",NGEN,MU,identifier) # Stat Generation
    insert(statfile_utility,algorithm+"_gen"+str(NGEN)+"_pop"+str(MU))

    statfile_time = genFileName(algorithm,"time",NGEN,MU,identifier) # Stat Generation
    insert(statfile_time,algorithm+"_gen"+str(NGEN)+"_pop"+str(MU))


    print ("Initial Population")
    for p in pop:
	print p



    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    record = stats.compile(pop)
    logbook.record(gen=0, evals=len(invalid_ind), **record)
    print(logbook.stream)

    # Begin the generational process
    for gen in range(1, NGEN):
	oldpop = pop
        for k, agent in enumerate(pop):
            a,b,c = toolbox.select(pop)
            y = toolbox.clone(agent)
            index = random.randrange(NDIM)
            for i, value in enumerate(agent):
                if random.random() < CR:
                    y[i] = a[i] + F*(b[i]-c[i])
            y.fitness.values = toolbox.evaluate(y)
            if y.fitness > agent.fitness:
                pop[k] = y

        hof.update(pop)
        record = stats.compile(pop)
        logbook.record(gen=gen, evals=len(pop), **record)
        print(logbook.stream)

        if stop_early(oldpop, hof):
            print("Stopping generation early, no purchases")
            break
    
    map(lambda x:insert(statfile_purchase,str(x.fitness.values[0])),hof)
    insertnl(statfile_purchase)	
    map(lambda x:insert(statfile_utility,str(x.fitness.values[1])),hof)
    insertnl(statfile_utility)	
    map(lambda x:insert(statfile_time,str(x.fitness.values[2])),hof)
    insertnl(statfile_time)	
    
    volume = hv.compute([x.fitness.values for x in hof if x.fitness.values[0]==1.0])

    print "Hypervolume = ",volume
    #insert(statfile_hypervolume,str(volume))
    #insert(statfile_spread,str(spread(oldpop)))
    #insertnl(statfile_spread)	
    #insert(statfile_igd,str(igd(oldpop)))
    #insertnl(statfile_igd)	


    r = redis.StrictRedis(host='152.46.19.201', port=6379, db=0)
    r.flushall() # Remove all keys once done 
    

    #print("Final population hypervolume is %f" % hypervolume(pop, [11.0, 11.0]))

    return hof, logbook





def plotGraph(pop):

    global save_figure
    #plotGraph


    front = numpy.array([ind.fitness.values for ind in pop if ind.fitness.values[0]== 1 ])
    #optimal_front = numpy.array(pop)
    #plt.scatter(optimal_front[:,0], optimal_front[:,1], c="r")
    #plt.scatter(front[:,0], front[:,1], c="b")

    if front == []:
	print "Nothing to plot"
	sys.exit()   
    #print "Front ",front
    plt.scatter(front[:,2] , front[:,1],c=front[:,0])
    plt.axis("tight")
    plt.xlabel('time', fontsize=18)
    plt.ylabel('utility', fontsize=16)
    #plt.show()

    if save_figure : 
	fname = str(uuid.uuid4())
	plt.savefig(fname)
	print "Saved Plot at ", fname ,".PNG"
    else:
	print "Saving Plot disabled. No Plot saved"    

def plotHitRatio(algorithm,main):

    global hits,calls
    x_axis = []
    y_axis = []
    for i in xrange(0,300,10):
	p,s = main(1,i,100)  
    	hit_ratio = 0
    	if calls != 0 :
		hit_ratio = float(hits) / calls

    	#print "Hit ratio ", hit_ratio
	
	x_axis.append(i)
	y_axis.append(hit_ratio)


	#Reset Counter
	hits =0
	calls=0
    with open("hit_ratio.txt", "a") as myfile:
    	myfile.write(algorithm+":"+repr(x_axis)+":"+repr(y_axis)+"\n")	

    """
    plt.plot(x_axis,y_axis,'ro-')
    plt.axis("tight")
    plt.xlabel('Generations', fontsize=18)
    plt.ylabel('Cache Hit Ratio', fontsize=16)
    plt.show()
    """


# function to exit early based on lack of purchases made
# if purchases made == 0, decisions are overtuned and buyer/seller cannot reach an agreement
def stop_early(oldPop, curPop):
    purchase_count = 0.0

    for p in curPop:
        purchase_count += p.fitness.values[0]

    if purchase_count < 1.0:
        return True

    return False
    

if __name__ == "__main__":
    identifier = str(uuid.uuid4())	

    from scoop import futures

    toolbox.register("map", futures.map)

    algo = [main_nsga2 , main_spea2 ]
    #algo = [ main_de]

    for algorithm in algo:
	#plotHitRatio("NSGA2",main_nsga2)

	with duration():
		NGEN=100
		MU=100
        	pop, stats = algorithm(NGEN=NGEN,MU=MU) # Population multiple of 4
    
    
    		print " Final Population "
    		for i in pop :
			print i,i.fitness.values

    		print "Generate stats for objectives using `sh printStat.sh -u "+str(identifier)+"`" 

    		#print "Total Calls ", calls
    		#print "Hit Count" , hits

    		plotGraph(pop)
