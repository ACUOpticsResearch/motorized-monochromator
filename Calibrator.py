#Calibrator
#By Jared Barker 2016

import time
from monochromator import Mono

def calibrate(startWvl):
    a = Mono('COM3')
    backwards = False
    number_of_steps = 0
    a.setWavelengthInMemory(startWvl)
    if startWvl >= 8950:
        backwards = True
    if backwards:
        end_goal = startWvl - 100
    else:
        end_goal = startWvl + 100
    print "Once the monochromator reaches " + str(end_goal) + " Angstroms, hit Ctrl+C to stop the process."
    try:
        while True:
            if backwards:
                a.stepDown()
            else:
                a.stepUp()
            number_of_steps = number_of_steps + 1
    except Exception as e:
        print "Stopped."
    finally:
        print "Number of steps: " + str(number_of_steps)
