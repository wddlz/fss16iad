import sys
from maxwalksat import mws
from model.osyczka2 import Osyczka2
from model.kursawe import Kursawe
from model.schaffer import Schaffer
sys.dont_write_bytecode = True

for model in [Schaffer, Osyczka2, Kursawe]:
    for optimizer in [mws]:
        print "optimizer : %s model : %s" %(str(optimizer), str(model))
        optimizer(model())
        print