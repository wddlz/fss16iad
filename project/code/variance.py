import random
from deap import base, creator, tools
import sys
import subprocess
import os,time
import uuid
import parse
import json

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

prism_path = "/ase/final_project/prism-4.3.1-src/bin/prism"
pop_size = 1

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
        decs = gen_decs
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

def prism(individual):
	global prism_path
	filename = parse.call_prism(prism_path,individual)
	evaluated_results =parse.Parse(filename).get_output()
	if evaluated_results:
		return evaluated_results
	else:
		return (0,0,0)


def evaluateInd(individual):
	return prism(individual)


creator.create("Fitness", base.Fitness, weights=(4.0, -1.0, 1.0))
creator.create("Individual", list, fitness=creator.Fitness)
toolbox = base.Toolbox()
toolbox.register("decs", aop_decs)
toolbox.register("gen_one", tools.initIterate, creator.Individual, toolbox.decs)
toolbox.register("population", tools.initRepeat, list, toolbox.gen_one)
toolbox.register("evaluate", evaluateInd)
pop = toolbox.population(n=pop_size)

for p in pop:
	print p;print "\nmulti runs...\n"
	succ_runs = 0
	f1, f2, f3 = [], [], []
	for x in xrange(10):
		p.fitness.values = toolbox.evaluate(p)
		if p.fitness.valid:
			print p.fitness.values
			f1.append(p.fitness.values[0])
			f2.append(p.fitness.values[1])
			f3.append(p.fitness.values[2])
			succ_runs += 1
	print ""
	mean = [sum(f1)/succ_runs, sum(f2)/succ_runs, sum(f3)/succ_runs]
	print "mean...";print mean;print ""
	ds1 = ds2 = ds3 = 0
	for run in xrange(succ_runs):
		ds1 += (mean[0]-f1[run])**2
		ds2 += (mean[1]-f2[run])**2
		ds3 += (mean[2]-f3[run])**2
	print "var..."
	var = [ds1/succ_runs, ds2/succ_runs, ds3/succ_runs]
	print var
	print "==========\n"


