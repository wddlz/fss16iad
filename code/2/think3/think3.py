import sys

#Exercise 1
#Error message :
# NameError: name 'repeat_lyrics' is not defined

#Exercise 2
#Output :
# I'm a lumberjack, and I'm okay.
# I sleep all night and I work all day.
# I'm a lumberjack, and I'm okay.
# I sleep all night and I work all day.

#Exercise 3
def right_justify(s):
  num_columns = 70
  num_spaces = num_columns - len(s)
  while num_spaces > 0:
    sys.stdout.write(" ")
    num_spaces -= 1
  print s
  
#Exercise 4-part1
#Output screenshot added

#Exercise 4-part2,3,4
def do_twice(f, val):
  f(val)
  f(val)
def print_twice(s):
  print s
  print s
def do_four(f, val):
  do_twice(f, val)
  do_twice(f, val)
  
#Exercise 5-part5
#Output screenshot added

#Exercise 5
#Method to call : gen_grid()
def generate_line(end_mid, other):
  print end_mid,
  gen_mid_line(other)
  print end_mid,
  gen_mid_line(other)
  print end_mid

def gen_mid_line(x):
  for i in xrange(4):
    print x,

def spec_line():
  generate_line("+", "-")
  
def normal_lines():
  for i in xrange(4):
    generate_line("/", " ")
  
def gen_grid():
  spec_line()
  normal_lines()
  spec_line()
  normal_lines()
  spec_line()
  
gen_grid()