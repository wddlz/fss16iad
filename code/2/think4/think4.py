from swampy.TurtleWorld import *
import sys,math

sys.dont_write_bytecode=True
__author__="Aniket Dhuri"


def square(t,length):
    """Draw square of length length """
    for i in range(4):
        fd(t, length)
        lt(t)

def polygon(t,length,n):
    """Draw polygon with n sides of length length """
    for i in range(n):
        fd(t, length)
        lt(t,(360/n))

def circle(t,r):
    """Draw circle of radius r """
    circum= 2*math.pi*r
    length=30
    l=int( circum/length)
    polygon(t,length,l)

def arc(t,r,angle):
    """Draw arc of angle angle and radius r """
    arc_circum= 2* math.pi *r * angle /360
    length=30
    arc_length=arc_circum/length
    arc_angle=angle/length
    for i in range(length):
        fd(t,arc_length)
        rt(t,arc_angle)


if __name__ == '__main__':
    world = TurtleWorld()
    bob = Turtle()
    print bob

    bob.delay= 0.01

    square(bob,100)         #4.3.1 and 4.3.2

    bob.set_pen_color("#000000")
    polygon(bob,100,5)      #4.3.3

    bob.set_pen_color("#00FF00")
    circle(bob,100)         #4.3.4

    bob.set_pen_color("#FF0000")
    arc(bob,100,90)         #4.3.5
    wait_for_user()