import sys
import uuid

def genFileName(algorithm,plot,ngen,mu,temp):
	return "stats/stat_"+algorithm+"_"+plot+"_"+"gen"+str(ngen)+"pop"+str(mu)+"_"+temp+".txt"	

def insert(filename,string):
	with open(filename, "a") as myfile:
		myfile.write(string+" ")


def insertnl(filename):
	with open(filename, "a") as myfile:
		myfile.write("\n")



if __name__=="__main__":
	print genFileName("NSGA2","purchase",100,20)
