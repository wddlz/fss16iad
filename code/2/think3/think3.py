import sys

#Exercise 1
#Error message :
# NameError: name 'repeat_lyrics' is not defined

print "EXCERCISE 3.1: "
print "Answer: NameError: name 'repeat_lyrics' is not defined"
# repeat_lyrics()

def print_lyrics():
    print "I'm a lumberjack, and I'm okay."
    print "I sleep all night and I work all day."


def repeat_lyrics():
    print_lyrics()
    print_lyrics()

#Exercise 2
#Output :
# I'm a lumberjack, and I'm okay.
# I sleep all night and I work all day.
# I'm a lumberjack, and I'm okay.
# I sleep all night and I work all day.
print "\nEXCERCISE 3.2: "
repeat_lyrics()

#Exercise 3
def right_justify(s):
  num_columns = 70
  num_spaces = num_columns - len(s)
  # new_str = ""  # If you want to return an object rather than just print
  while num_spaces > 0:
    sys.stdout.write(" ")
    # new_str += " "  # Use the new_str way
    num_spaces -= 1
  # return new_str + s  # instead of printing
  print s

print "\nEXCERCISE 3.3: "
right_justify("allen")
  
#Exercise 4-part1
#Output screenshot added
print "\nEXCERCISE 3.4.1: "


def do_twice(f):
  f()
  f()


def print_spam():
  print "spam"

do_twice(print_spam)

print "\nEXCERCISE 3.4.2,3,4: "
#Exercise 4-part2,3,4
def do_twice(f, val):
  f(val)
  f(val)


def print_twice(s):
  print s
  print s

do_twice(print_twice, "spam")

#Exercise 4-part5
#Output screenshot added
def do_four(f, val):
  do_twice(f, val)
  do_twice(f, val)

print "\nEXCERCISE 3.4.5: "
do_four(print_twice, "spam") 


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

print "\nEXCERCISE 5.1: "  
gen_grid()

print "\nEXCERCISE 5.2: "  


def generate_symbol(s):
  print s,

  
def print_x (f, s, x):
  for i in xrange(x):
    f(s)


# a dynamic grid generator
def generate_grid(x):
  a_plus = "+"
  a_dash = "-"
  a_slash = "/"
  a_space = " " 

  # where x is the number of cols/rows
  for j in xrange(x):
    for i in xrange(x):
      print_x(generate_symbol, a_plus, 1)
      print_x(generate_symbol, a_dash, 4)
    print_x(generate_symbol, a_plus, 1)
    print ""

    for k in xrange(4):
      for i in xrange(x):
        print_x(generate_symbol, a_slash, 1)
        print_x(generate_symbol, a_space, 4)
      print_x(generate_symbol, a_slash, 1)
      print ""

  # end line
  for i in xrange(x):
    print_x(generate_symbol, a_plus, 1)
    print_x(generate_symbol, a_dash, 4)
  print_x(generate_symbol, a_plus, 1)
  print ""

# generate_grid(2) Programatic 2 rather than hard code
generate_grid(4)

print "\nand 6x6 for fun"
generate_grid(6)
