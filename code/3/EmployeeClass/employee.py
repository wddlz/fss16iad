#!/usr/bin/python
from __future__ import division,print_function
import sys,random,os
sys.dont_write_bytecode=True
__author__ = 'ANIKETDHURI'


# usage:
#   python employee

#----------------------------------------------


class Employee:
    'Employee Class'
    eCount = 0

    def __init__(self,name,age):
        """
        :param name:  Name of the Employee
        :param age:  Age of the Employee
        Increments the global Employee eCount variable
        :return: None
        """
        self.name = name
        self.age  = int(age)
        Employee.eCount += 1

    def __repr__(self):
        """
        :return: Representation of the object with Employee Name and Age
        """
        return 'Employee Name : %s , Age : %i' %  (self.name,self.age)

    def __lt__(self, other):
        """
        :param other: Compares self with other Employee object based on age
        :return: True if self < other ; else otherwise
        """
        return self.age < other.age

def employeeCount():
    """
    :return: Returns Employee Count
    """
    print ("Employee Count is %s \n" % Employee.eCount)


if __name__=="__main__":
    e1 = Employee("Rose",24)
    print(e1)
    employeeCount()

    e2 = Employee("Jane",28)
    print(e2)
    employeeCount()


    e3 = Employee("Steve",18)
    print(e3)
    employeeCount()

    print ('Is %s < %s ? : %s ' % ( e1,e2 , e1 < e2))
    print ('Is %s < %s ? : %s ' % ( e2,e1 , e2 < e1))

    list = [e1,e2,e3]
    print ("\nEmployees list sorted on their age \n" )
    for i in sorted(list):
        print (i)
