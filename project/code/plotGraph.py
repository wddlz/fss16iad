import uuid,numpy
import json
import ast
import sys

import matplotlib.pyplot as plt
def plotGraph(pop,algorithm):

    global save_figure
    #plotGraph

    plt.figure()
    #front = numpy.array([ind.fitness.values for ind in pop if ind.fitness.values[0]== 1 ])
    #optimal_front = numpy.array(pop)
    #plt.scatter(optimal_front[:,0], optimal_front[:,1], c="r")
    #plt.scatter(front[:,0], front[:,1], c="b")
    #print front
    front = numpy.array(pop)
    if len(front) == 0:
        print "Nothing to plot"
        return
    #print "Front ",front
    plt.scatter(front[:,2] , front[:,1],c=front[:,0],label=str(algorithm))
    plt.axis("tight")

    plt.xlabel('time', fontsize=18)
    plt.ylabel('utility', fontsize=16)

    plt.legend(loc='lower right')
    #plt.show()

    fname = str(uuid.uuid4())
    plt.savefig(fname)
    print "Saved Plot at ", fname ,".PNG for ", algorithm
    plt.clf()

if __name__ == "__main__":

	#paretos = input("Paste Paretos from running run.py")
	fname = "pareto_"+sys.argv[1]
	print "Opening ",fname

	with open(fname) as f:
    		content = f.readlines()

	

	p= ast.literal_eval(content[-1])

	for i in p:
		plotGraph(p[i],i)
