import matplotlib.pyplot as plt
import random
import numpy as np
import ast

lines = [line.rstrip('\n') for line in open('hit_ratio.txt')]

lbl= []
x_axis = []
y_axis = []

for i in lines :

	lbl.append(i.split(":")[0])
	x_axis.append(ast.literal_eval(i.split(":")[1]))
	y_axis.append(ast.literal_eval(i.split(":")[2]))


	



for x,y,l in zip(x_axis,y_axis,lbl):
    print "Plotting for",l
    plt.plot(x,y,'o-',label = l,c=np.random.rand(3,1))
    plt.axis("tight")
    plt.xlabel('Generations', fontsize=18)
    plt.ylabel('Hashmap Hit Ratio', fontsize=16)
    plt.legend(loc='lower right')
 #   plt.show()



#fig,ax = plt.subplots()
#data_line = ax.plot(x,y, label='Data', marker='o')
#plt.scatter(np.array(x_axis),np.array( y_axis))
# Plot the average line
#mean_line = ax.plot(x,y_mean, label='Mean', linestyle='--')
# Make a legend
#legend = ax.legend(loc='upper right')

#plt.show()	

"""
# Create some random data
x = np.arange(0,10,1)
y = np.zeros_like(x)    
y = [random.random()*5 for i in x]

# Calculate the simple average of the data
y_mean = [np.mean(y) for i in x]


fig,ax = plt.subplots()
# Plot the data
data_line = ax.plot(x,y, label='Data', marker='o')
# Plot the average line
mean_line = ax.plot(x,y_mean, label='Mean', linestyle='--')
# Make a legend
legend = ax.legend(loc='upper right')
"""



plt.show()

