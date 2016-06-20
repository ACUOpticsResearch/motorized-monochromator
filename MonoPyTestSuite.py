#Test suite designed to test the monochromator.py class
#By Jared Barker


from monochromator import Mono
import time

a = Mono('COM3')

a.setWavelengthInMemory(6700)

wave = a.getWavelengthFromMemory()

if wave != "6700.00":
    print "Failed Test 1"
else:
    print "Passed Test 1"

wave = a.getWavelength()
if wave != "6700.00":
    print "Failed Test 2"
else:
    print "Passed Test 2"

wave = a.goToWavelength(7000)
if wave != "7000.00":
    print "Failed Test 3"
else:
    print "Passed Test 3"

time.sleep(1)

wave = a.getWavelength()
if wave != "7000.00":
    print "Failed Test 4"
else:
    print "Passed Test 4"

wave = a.stepUp()
if wave != "7000.31":
    print "Failed Test 5"
else:
    print "Passed Test 5"

a.stepDown()
wave = a.stepDown()
if wave != "6999.69":
    print "Failed Test 6"
else:
    print "Passed Test 6"

failed = True

try:
    a.goToWavelength(2000)
except ValueError:
     failed = False
if failed:
    print "Failed Test 7"
else:
    print "Passed Test 7"

a.goToWavelength(6700)
print "Reset to inital conditions"
