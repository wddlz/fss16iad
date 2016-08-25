from swampy.TurtleWorld import *
import sys,math

sys.dont_write_bytecode=True
__author__="Aniket Dhuri"


def polyline(t, n, length, angle):
    """Draws n line segments.

    t: Turtle object
    n: number of line segments
    length: length of each segment
    angle: degrees between segments
    """
    for i in range(n):
        fd(t, length)
        lt(t, angle)


def polygon(t, n, length):
    """Draws a polygon with n sides.

    t: Turtle
    n: number of sides
    length: length of each side.
    Using from : http://www.greenteapress.com/thinkpython/code/polygon.py
    """
    angle = 360.0/n
    polyline(t, n, length, angle)


def arc(t, r, angle):
    """Draws an arc with the given radius and angle.

    t: Turtle
    r: radius
    angle: angle subtended by the arc, in degrees
    Using from http://www.greenteapress.com/thinkpython/code/polygon.py
    """
    arc_length = 2 * math.pi * r * abs(angle) / 360
    n = int(arc_length / 4) + 1
    step_length = arc_length / n
    step_angle = float(angle) / n

    # making a slight left turn before starting reduces
    # the error caused by the linear approximation of the arc
    lt(t, step_angle/2)
    polyline(t, n, step_length, step_angle)
    rt(t, step_angle/2)


def polypie(t, n, r):
    """Draws a pie divided into radial segments.

    t: Turtle
    n: number of segments
    r: length of the radial spokes
    Using : http://www.greenteapress.com/thinkpython/code/pie.py
    """
    angle = 360.0 / n
    for i in range(n):
        isosceles(t, r, angle/2)
        lt(t, angle)


def isosceles(t, r, angle):
    """Draws an icosceles triangle.

    The turtle starts and ends at the peak, facing the middle of the base.

    t: Turtle
    r: length of the equal legs
    angle: peak angle in degrees
    Using http://www.greenteapress.com/thinkpython/code/pie.py
    """
    y = r * math.sin(angle * math.pi / 180)

    rt(t, angle)
    fd(t, r)
    lt(t, 90+angle)
    fd(t, 2*y)
    lt(t, 90+angle)
    fd(t, r)
    lt(t, 180-angle)



def walk(t,length):
    """Walk without dropping ink
    t: Turtle
    length : length to walk
    """
    pu(t)
    fd(t,length)
    pd(t)

def petal(t,r,angle):
    """Draw petal using two arcs
    t:Turtle
    r:radius
    angle:angle subtending arc
    """
    for i in range(2):
        arc(t,r,angle)
        lt(t,180-angle)

def flower(t,p,r,angle):
    """Draw flower with p petals
    t:Turtle
    p:Petals
    r:radius
    angle: angle subtending arc
    """

    for i in range(p):
        petal(t,r,angle)
        lt(t,360.0/p)


def exercise2(t):
    """
    Exercise 4.2
    :t : Turtle

    """
    t.set_pen_color("#FF0000")
    #arc(bob,100,90)         #4.3.5

    walk(t,-100)
    flower(t,7,60,60)

    t.set_pen_color("#0000FF")
    walk(t,150)
    flower(t,10,40,80)

    t.set_pen_color("#00FF00")
    walk(t,150)
    flower(t,20,140,20)

    walk(t,-150)

def exercise3(t):
    """
    Exercise 3
    :t : Turtle
    """

    t.set_pen_color("#FF0000")
    walk(bob,-100)
    polypie(t,5,60)

    t.set_pen_color("#0000FF")
    walk(bob,150)
    polypie(t,6,60)

    t.set_pen_color("#00FF00")
    walk(bob,150)
    polypie(t,7,60)

    walk(bob,-150)

def align(t,length):
    """
    For two sections , align the turtle
    down to print the second sequence.
    :param t: Turtle
    :param length: Length to move down

    """
    pu(t)
    rt(t,90)
    fd(t,length)
    lt(t,90)
    pd(t)


if __name__ == '__main__':
    world = TurtleWorld()
    bob = Turtle()
    print bob
    bob.delay= 0.001


    exercise2(bob)
    align(bob,180)
    exercise3(bob)

    wait_for_user()