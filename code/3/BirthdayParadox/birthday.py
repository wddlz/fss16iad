from __future__ import division
import random
import sys

__author__="Karan Jadhav"

"""
Checks if given list has duplicate elements
:lst : list to be checked
:return : boolean
"""
def has_duplicates(lst):
  for i in range(len(lst)):
    if lst[i] in lst[i+1:]:
      return True
  return False
  
"""
Calculates probability of 2 people having the same birthday in a group
:num_people : number of people
:sample_size : number of times birthdays are sampled
"""
def birthday_paradox(num_people, sample_size):
  same_birthdays = 0
  for i in range(sample_size):
    birthdays = []
    for i in range(num_people):
      birthdays.append(random.randint(1,366))
    if has_duplicates(birthdays):
      same_birthdays += 1
  print "probability : %s" % (same_birthdays/sample_size)
    
if __name__=="__main__":
  lst1 = [1,2,3,]
  lst2 = [3,1,2,2]
  lst3 = ["abc", "xyz", "abc"]
  print "Exercise 8.1"
  print("{} : {} {} : {} {} : {}\n".format(lst1, has_duplicates(lst1), lst2, has_duplicates(lst2), lst3, has_duplicates(lst3)))
  print "Exercise 8.2"
  birthday_paradox(23, 100)