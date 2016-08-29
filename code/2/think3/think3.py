# -*- coding: utf-8 -*-
# !/usr/bin/python
"""
think3.py for Chapter 3 Exercises
"""
import sys

# Exercise 1
# Error message :
# NameError: name 'repeat_lyrics' is not defined
print "EXERCISE 3.1: "
print "Answer: NameError: name 'repeat_lyrics' is not defined"
# repeat_lyrics()


def print_lyrics():
    """ print lyrics of lumberjack poem """
    print "I'm a lumberjack, and I'm okay."
    print "I sleep all night and I work all day."


def repeat_lyrics():
    """ call print_lyrics twice """
    print_lyrics()
    print_lyrics()


# Exercise 2
# Output :
# I'm a lumberjack, and I'm okay.
# I sleep all night and I work all day.
# I'm a lumberjack, and I'm okay.
# I sleep all night and I work all day.
print "\nEXERCISE 3.2: "
repeat_lyrics()


# Exercise 3
def right_justify(s):
    """ :param s: string param whose last character will be the 70th character printed"""
    num_columns = 70
    num_spaces = num_columns - len(s)
    # new_str = ""  # If you want to return an object rather than just print
    while num_spaces > 0:
        sys.stdout.write(" ")
        # new_str += " "  # Use the new_str way
        num_spaces -= 1
    # return new_str + s  # instead of printing
    print s


print "\nEXERCISE 3.3: "
right_justify("allen")

# Exercise 4-part1
# Output screen shot added
print "\nEXERCISE 3.4.1: "


def do_twice(f):
    """ :param f: functions to be ran twice """
    f()
    f()


def print_spam():
    """ prints spam """
    print "spam"


do_twice(print_spam)

print "\nEXERCISE 3.4.2,3,4: "


# Exercise 4-part2,3,4
def do_twice(f, val):
    """
    :param f: function to be ran twice
    :param val: param to be input for function f
    """
    f(val)
    f(val)


def print_twice(s):
    """
    :param s: to be printed twice
    """
    print s
    print s


do_twice(print_twice, "spam")


# Exercise 4-part5
# Output screen shot added
def do_four(f, val):
    """
    :param f: function to be passed to do_twice twice
    :param val: param to be input to do_twice (thus function f)
    :return:
    """
    do_twice(f, val)
    do_twice(f, val)


print "\nEXERCISE 3.4.5: "
do_four(print_twice, "spam")


# Exercise 5
# Method to call : gen_grid()
def generate_line(end_mid, other):
    """
    :param end_mid:
    :param other:
    :return:
    """
    print end_mid,
    gen_mid_line(other)
    print end_mid,
    gen_mid_line(other)
    print end_mid


def gen_mid_line(x):
    """
    :param x:
    :return:
    """
    for i in xrange(4):
        print x,


def spec_line():
    """
    :return:
    """
    generate_line("+", "-")


def normal_lines():
    """
    :return:
    """
    for i in xrange(4):
        generate_line("/", " ")


def gen_grid():
    """
    :return:
    """
    spec_line()
    normal_lines()
    spec_line()
    normal_lines()
    spec_line()


print "\nEXERCISE 5.1: "
gen_grid()

print "\nEXERCISE 5.2: "


def generate_symbol(s):
    """
    :param s: symbol to be printed
    """
    print s,


def print_x(f, s, x):
    """
    :param f: function to be ran
    :param s: param to be passed to function f
    :param x: how many times function f is run
    :return:
    """
    for i in xrange(x):
        f(s)


# a dynamic grid generator
def generate_grid(x):
    """
    :param x: how many rows and columns in the grid
    :return:
    """
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


# generate_grid(2) Programmatic 2 rather than hard code
generate_grid(4)

print "\nand 6x6 for fun"
generate_grid(6)
