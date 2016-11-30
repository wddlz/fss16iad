import random
import sys

def eucledian(one, two):
  # TODO 4: Code up the eucledian distance. https://en.wikipedia.org/wiki/Euclidean_distance
  dist = 0
  for i in xrange(len(one)):
    dist = dist + (one[i]-two[i])**2
  dist = dist**0.5
  return dist

def sort_solutions(solutions):
  """
  Sort a list of list before computing spread
  """
  def sorter(lst):
    m = len(lst)
    weights = reversed([10 ** i for i in xrange(m)])
    return sum([element * weight for element, weight in zip(lst, weights)])
  return sorted(solutions, key=sorter)


def closest(one, many):
  min_dist = sys.maxint
  closest_point = None
  for this in many:
    dist = eucledian(this, one)
    if dist < min_dist:
      min_dist = dist
      closest_point = this
  return min_dist, closest_point

def spread(obtained, ideals):
  """
  Calculate the spread (a.k.a diversity)
  for a set of solutions
  """
  s_obtained = sort_solutions(obtained)
  s_ideals = sort_solutions(ideals)
  d_f = closest(s_ideals[0], s_obtained)[0]
  d_l = closest(s_ideals[-1], s_obtained)[0]
  n = len(s_ideals)
  distances = []
  for i in range(len(s_obtained)-1):
    distances.append(eucledian(s_obtained[i], s_obtained[i+1]))
  d_bar = sum(distances)/len(distances)
  # TODO 5: Compute the value of spread using the definition defined in the previous cell.
  num = 0;
  for d_i in distances:
    num = num + abs(d_i-d_bar)
  num = num + d_f + d_l
  denom = d_f + d_l + (n-1)*d_bar
  delta = num/denom
  return delta

def paretos_func():
  return {"ga" : [(4,7,3), (1,5,3), (4,5,2)], "nsga2" : [(3,4,7), (7,5,8), (8,3,5)]}

def igd(obtained, ideals):
  igd_val = 0
  for ideal in ideals:
    min_d = 100
    for ob in obtained:
      d = eucledian(ideal, ob)
      if(d < min):
        closest = ob
    igd_val += eucledian(ideal, closest)
    igd_val = igd_val/len(ideals)
  return igd_val

if __name__ == "__main__":
  paretos = paretos_func()  # call actual function to get paretos dict
  agg_pop = []
  for algo, pop in paretos.iteritems():
    print "", algo, " : ", pop
    agg_pop.extend(pop)

  print "agg_pop : ", agg_pop

  random.shuffle(agg_pop) # actually use tools.selBest
  ref_set = agg_pop[0:3]  # use size of each population instead of hardcoded 3

  print "ref_set : ", ref_set;print

  for algo, pop in paretos.iteritems():
    print "spread : ", spread(pop, ref_set)
    print "igd : ", igd(pop, ref_set)