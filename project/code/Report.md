# Alternating Offers Protocol (Rubenstein)
##### Team Members
* Aniket Dhuri (adhuri@ncsu.edu)
* Ian Drosos (izdrosos@ncsu.edu)
* Karan Jadhav (kjadhav@ncsu.edu)

##### Date : December 07 , 2016  

### Abstract  

Bargaining between buyers and sellers is an activity that has been around since the dawn of civilization. Both parties ideally want low and high prices and try to agree on a price somewhere in between. The large number of decisions that affect the bargaining and the non-deterministic nature of this process’s model, make finding the best solutions difficult and model simulation a slow process. This project made use of prism model simulator to simulate the model and used three different genetic algorithms namely GA,NSGA2 and SPEA2  to find the best decision sets for the buyer-seller model. It also used parallelism and early termination to improve the overall run time of running optimizers on the model.

### Keywords
1. **Prism** : PRISM is a probabilistic model checker, a tool for formal modelling and analysis of systems that exhibit random or probabilistic behaviour.
2. **GA** : Genetic Algorithm is a method for solving both constrained and unconstrained optimization problems based on a natural selection process that mimics biological evolution.
3. **NSGA2** : Non-dominated sorting genetic algorithm for multi objective optimization that makes use of multiple frontiers and primary/secondary sorting.
4. **SPEA2** : Strength pareto evolutionary algorithm for multi objective optimization that uses dominance count and an archive,which is a set of good solutions.
5. **Spread** : How distant each point of a population is from its neighbours
6. **IGD** : Distance between the ideal and obtained pareto front.
7. **Hypervolume** : The volume inside the pareto frontiers.
8. **DEAP** : Distributed Evolutionary Algorithms in Python (DEAP) is a novel evolutionary computation framework for rapid prototyping and testing of ideas.
9. **SCOOP** : Scalable COncurrent Operations in Python (SCOOP) is a distributed task module allowing concurrent parallel programming on various environments, from heterogeneous grids to supercomputers. 

### Introduction
The buyer-seller model depends on many decisions such as buyer/seller initial price, reserved price, strategy, time deadline, etc. The utility value depends on the value at which the buyer and seller agreed for purchase as well as on the time when the agreement was made.The utility value would be higher for purchase value made earlier. The prism model we used had 15 decisions and generated 3 objectives. The large number of decisions in this model was a major challenge undertaken in this project as it becomes increasingly difficult to explore the large solution space. In addition to this, the model simulation took several hours to complete due to the simulation overhead caused by prism simulation. This led us to pursue a new objective to improve the run time by using parallelism, load balancing and early termination.

### Background
#### Rubinstein’s Bargaining Model
The bargaining model features alternating offers through an infinite time horizon where two individuals have several possible contractual agreements before them. The standard model has following elements-

1. Two players - Buyer and Seller.
2. Unlimited offers to reach consensus until one player accepts an offer
3. Alternating offers - first player makes an offer and if second player rejects, the game moves to the next period where second player makes an offer, and so on.
4. Delays are costly since utility value decreases as time progresses.

#### Prism Model
The model used in this project is based on the Rubinstein’s Alternating Offers protocol negotiation framework. The model used was already implemented as a Discrete Time Markov Chain model in the PRISM language, a simple state based language to be run on prism model checker tool.

1. In this, both buyer and seller bargain over an item, proposing offers or counter offers until number of steps configured.
2. Disagreement is the worst outcome and players prefer any agreement at least as much as disagreement.
3. Players seek to maximize utility. For two outcomes of the same value, the one with lesser time has higher utility.

#### Model states

![state](./screenshots/model_state.png )

The model can have the following states as seen in the figure above:

1. Wait Bid : Seller awaiting a bid
2. Bid : Buyer proposing a bid
3. Purchase : Either seller or buyer agreeing to the proposed value
4. Bid Result : Seller’s response on buyer’s bid
5. Wait CBid : Buyer awaiting seller’s counter offer after bid rejection
6. CBid : Counter bid thrown by seller after rejection of buyer’s bid
7. CBid Result : Buyer’s response on seller’s counter bid


The buyer makes a bid and if the seller agrees, purchase is completed. Otherwise, he waits for a counter bid (cbid). If counter bid is rejected , the buyer bids again.
The seller waits for a bid and if accepted, the purchase is done. Otherwise he makes a counter bid and the process continues till either the seller or buyer agrees to a bid or cbid. 

#### Strategy
The buyer and seller follow two strategies - Conceder (if the player is willing to yield a lot in the early phase of negotiation) and Boulder (if a player is willing to concede considerably only when it's time deadline is approaching). The strategy can be linear or nonlinear.

#### Decisions
| No 	| Decision                          	| Description                                                                                                 	| Range we used      	|
|----	|-----------------------------------	|-------------------------------------------------------------------------------------------------------------	|--------------------	|
| 1  	| Buyer Initial price B_IP          	| Ideal high and low price at which,buyer begin                                                               	| Buyer(1,100)       	|
| 2  	| Seller Initial price S_IP         	| Ideal high and low price at which seller begin                                                              	| Seller (1000,2000) 	|
| 3  	| Buyer reserved PriceB_RP          	| Threshold where a player rejects offer 100% of the time                                                     	| Buyer(1000,2000)   	|
| 4  	| Seller reserved PriceS_RP         	| Threshold where a player rejects offer 100% of the time                                                     	| Seller(1,100)      	|
| 5  	| Buyer Time-deadlineTb             	| Time that player will quit negotiation if no agreement                                                      	| Buyer(50,100)      	|
| 6  	| Seller Time-deadlineTs            	| Time that player will quit negotiation if no agreement                                                      	| Seller(50,100)     	|
| 7  	| Boulware Strategy Switch Time TbB 	| When a player begins to start conceding from a boulware strategy                                            	| (20,40)            	|
| 8  	| Conceder Strategy Switch Time TsB 	| When a player stops conceding based on the offered value based on reserved price.                           	| (48, 49)           	|
| 9  	| Buyer conceder incrementbCinc     	| Increment in buyer’s bid for Conceder strategy                                                              	| (100,200)          	|
| 10 	| Buyer Boulware incrementbBinc     	| Increment in buyer’s bid for Boulware strategy                                                              	| (1,3)              	|
| 11 	| Seller conceder decrementsCdec    	| Decrement in seller’s bid for conceder strategy                                                             	| (100,200)          	|
| 12 	| Seller Boulware decrementsBdec    	| Decrement in seller’s bid for Boulware strategy                                                             	| (1,3)              	|
| 13 	| Buyer’s switching factor Kb       	| Buyer stops conceding when it’s next bid is lesser thanBuyer switching factor * Buyer conceder increment    	| (1,2)              	|
| 14 	| Seller’s switching factor Ks      	| Seller stops conceding when it’s next bid is lesser thanseller switching factor * seller conceder increment 	| (8,9)              	|
| 15 	| Offset                            	| Allows for considering a shifted accepting interval while minimizing model complexity                       	| (10000, 15000)     	|

#### Decision constraints
The following were the constraints for the decisions that we checked using the ok() function in our code:

1. Buyer Initial Price < Buyer Reserved Price
2. Seller Reserved Price < Seller Initial Price
3. Buyer/Seller Time deadline > 0
4. Buyer’s start conceding time deadline < Buyer time deadline
5. Seller’s stop conceding time deadline < Seller time deadline

#### Objectives 

| No 	| Objective 	| Description                                                                                                                                                                    	| Min/Max  	|
|----	|-----------	|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------	|----------	|
| 1  	| Utility   	| The purchase value agreed upon, dependent on time. Among two purchase outcomes having the same value, the one with lesser time has higher utilityUtility = Purchase value/time 	| Maximize 	|
| 2  	| Time      	| Time taken to come to a purchase agreement                                                                                                                                     	| Minimize 	|
| 3  	| Purchase  	| If purchase was successful Purchase =1 else Purchase =0.                                                                                                                       	| Maximize 	|

### Related Work
1. what paper did?
2. What claims they made?
3. What scope they had?

### Implementation 
#### Prism parser 
Prism model checker has a CLI program which takes the model file as an input along with max steps ( simpath) and the 15 decisions we discussed in the previous sections.  The CLI simulates each step and displays if a purchase was made. We use the following algorithm to parse the simulation and extract the objectives.
```
if ( last step contains “[PURCHASE]” ) :
	“””Purchase was successful “””
	purchase = 1  # 1 is successful purchase
	time = step
	if ( previous == “[BID]” ) : 
		value = BID
	else ( previous == “[CBID]” ) :
		value = CBID
	utility = value / time .
else : 
	“”” Purchase was unsuccessful”””
	purchase = 0 # 0 is unsuccessful purchase
	time = MAXINT
utility = -1 
```
Following figure shows the example simulation.

![cli](./screenshots/prism_cli.png )

In the above example , time = 6 and purchase = 1 . Since last bidding was [BID] , value = 1700 ( bid value ) . utility = 1700/6 = 283.3.

#### DEAP


Distributed Evolutionary Algorithms in Python (DEAP) is a evolutionary computation framework for rapid prototyping and testing of ideas and seeks to make algorithms explicit and data structures transparent. It was this transparency and generalized framework that attracted us to use DEAP for development. DEAP has selection,mutation and crossover operators [3] already developed that helped faster development .DEAP has a learning curve which made us read the documentation and test some simulations without prism parser before we proceeded with integration.

#### Optimizers

OPTIMIZERS
We declare the common functions for population generation, mate and mutate first.
The population was generated as follows:
```creator.create("Fitness", base.Fitness, weights=(4.0, 1.0, -1.0),crowding_dist=None) ```

Here the weights for ( purchase, utility , time ) are (4.0 , 1.0 and -1.0 ) . Here, negative values show minimizing objective. Positive values show maximizing objective. A 4.0 shows that weightage of purchase is higher than the other objectives , so that we get more purchases in the final population.

We define the mate and mutate functions for NSGA2 and SPEA2 for each decision for range ( BOUND_LOW, BOUND_UP ) as:
```
toolbox.register("mate", tools.cxSimulatedBinaryBounded, low=BOUND_LOW, up=BOUND_UP, eta=1.0)
toolbox.register("mutate", tools.mutPolynomialBounded, low=BOUND_LOW, up=BOUND_UP, eta=1.0, indpb=1.0/NDIM)
```
##### NSGA2

1. We first defined the select function :
```toolbox.register("select", tools.selNSGA2)```
2. Generate a population using DEAP
```pop = toolbox.population(n=MU)```
3. Evaluate individuals with invalid fitnesses and evaluate fitnesses again for them
```invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
       ind.fitness.values = fit```
4. Assign crowding distance to the population
```pop = toolbox.select(pop, len(pop))```
5. For every generation run
	* Create new population “offspring” by cloning the population
```offspring = tools.selTournamentDCD(pop, len(pop))
offspring = [toolbox.clone(ind) for ind in offspring]```
	* Using alternate pairs of the new population, with crossover probability mate the two selected individuals and then mutate them
```for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
            if random.random() <= CXPB:
                toolbox.mate(ind1, ind2)
toolbox.mutate(ind1)
toolbox.mutate(ind2)```
	* Evaluate fitness for all invalid individuals again
	* Select the best individuals from the old and new population
```pop = toolbox.select(pop + offspring, MU)```
	* Run steps A-D for the next generation

*Params for NSGA2*
CXPB : Crossover probability : 0.9
MUT  : Mutation probability : 0.03
NDIM :  30


##### SPEA2
We define the select function as:
```toolbox.register("select", tools.selSPEA2)```
The steps, code and params are the same as NSGA2


*Params for SPEA2*

CXPB : Crossover probability : 0.9
MUT  : Mutation probability : 0.03

##### Genetic Algorithm

The mate and mutate and select functions are defined:
```toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutUniformInt, low = BOUND_LOW, up = BOUND_UP, indpb=MUTPB)
toolbox.register("select", tools.selTournament, tournsize=3)```


GA follows the same steps as NSGA 2 except for the following differences:
	* The crossover individuals are mutated based on a mutation probability
```if random.random() < MUTPB:
   toolbox.mutate(mutant)
	* The next generation population is not composed of the best individuals from the old and new population but rather entirely of the new population
pop[:] = offspring```


*Params in GA*
CXPB : Crossover probability : 1.0
MUT  : Mutation probability : 0.01
