# Written by Jared Barker

import serial
import time

def wrt(a, input):
    a.write(input)
    while(not a.in_waiting):
        pass
    time.sleep(.01)

def rd(a):
    return str(a.read(a.in_waiting)).strip()

a=serial.Serial('COM3', baudrate=115200)

time.sleep(2)

a.reset_input_buffer()
a.reset_output_buffer()

wrt(a, '1')
rd(a)
wrt(a, '6700')
rd(a)
wrt(a, '2')
wave = rd(a)
if wave != "6700.00":
    print "Failed Test 1"
else:
    print "Passed Test 1"

wrt(a, '6')
wave = rd(a)
if wave != "6700.00":
    print "Failed Test 2"
else:
    print "Passed Test 2"

wrt(a, '3')
rd(a)
wrt(a, '7000')
wave = rd(a)
if wave != "7000.00":
    print "Failed Test 3"
else:
    print "Passed Test 3"

time.sleep(1)

wrt(a, '6')
wave = rd(a)
if wave != "7000.00":
    print "Failed Test 4"
else:
    print "Passed Test 4"

wrt(a, '4')
wave = rd(a)
if wave != "7000.31":
    print "Failed Test 5"
else:
    print "Passed Test 5"

wrt(a, '5')
rd(a)
wrt(a, '5')
wave = rd(a)
if wave != "6999.69":
    print "Failed Test 6"
else:
    print "Passed Test 6"

wrt(a, '3')
rd(a)
wrt(a, '6700')
wave = rd(a)
print "Reset to initial conditions"
