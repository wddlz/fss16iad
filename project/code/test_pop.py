import random
from deap import base, creator, tools
import sys
import subprocess
import os,time
import uuid
import logging
import parse
import json

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

prism_path = "/home/adhuri/prism-4.3.1-linux64/bin/prism"
pop_size = 8

NGEN=10
CXPB=0.2
MUTPB=0.01

def aop_decs():
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

pop = toolbox.population(n=pop_size)

print ("Initial Population")
for p in pop:
	print p

def prism(individual):
	global prism_path
	filename = parse.call_prism(prism_path,individual)
	evaluated_results =parse.Parse(filename).get_output()
	#print evaluated_results
	logging.debug (filename +" : "+ str(evaluated_results))
	if evaluated_results:
		return evaluated_results
	else:
		return (0,0,0)


def evaluateInd(individual):
    # Do some computation
	#print "Individual", individual;
	return prism(individual)
	#return random.randint(0,4),random.randint(0,4),random.randint(0,4)



toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutUniformInt, low = 0 , up = 1, indpb=0.01)
toolbox.register("select", tools.selNSGA2)
toolbox.register("evaluate", evaluateInd)


NGEN = 5
MU = 8
CXPB = 0.9

# Evaluate individuals with invalid fitness
if ( 1 == 1):
    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

#print [(ind.fitness.values, i) for i, ind in enumerate(individuals)]

 # Begin the generational process
if ( 1 == 1):
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
        pop = toolbox.select(pop + offspring, MU)
	print pop


print "Final Population"
for p in  pop:
	print p , p.fitness.values

#print dir(pop[0])


