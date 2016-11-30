import urllib2
import urllib
import ast
import sys


def getObjectives(individual):


   try:
	data = {}
	#data['name'] = 'Somebody Here'
	params= ['brp', 'srp', 'bip','sip', 'tb', 'tbb', 'ts', 'tsb', 'bcinc', 'bbinc', 'scdec', 'sbdec', 'kb', 'ks', 'offset']
	for i,p in enumerate(params):
		data[p]=individual[i]
	
	url_values = urllib.urlencode(data)
	#print url_values  # The order may differ. 
	url = 'http://152.46.19.201/prism'


	full_url = url + '?' + url_values
	#print full_url
	results = urllib2.urlopen(full_url).read()
	return ast.literal_eval(results)
   except:
	print "Error connecting to ",url," for ", full_url
	print "Better exit ,else you will get values like (0,0,0) "
	return (0,0,0)


#data = urllib2.urlopen(full_url)


if __name__ == "__main__":
	
	print getObjectives( [1982,27,27,1982,97,27,74,48,135,3 ,110,3,1 ,9,12004] )
