# Written by Candace Brooks 2015.
#edited by Darby Hewitt 8/20/2015
# TODO: remove sleep commands, and wait instead on arduino to return 
#          a "done" message of some sort; this will require arduino 
#          tweaks. One simple way is to use "\n" as the end char for 
#          the "done" message over serial, and use readline() to wait  
#          for the returned val
#
#       then, this class could use an overhaul to reflect the changes in the firmware
#
# changed shutDown to __del__(), because it does everything a destructor should
import serial
import time
# This section of code connects to the correct port

#This section of the code is to communicate with the arudino


class Mono(object):
    def __init__(self, Port):
        self.serPort = serial.Serial(Port)
        #time.sleep(1.67)
        #numberOfCharacters = self.serPort.inWaiting()
        #below is a better way to wait than just sleeping; 
        #  also it clears the buffer. assignment to initialReadout 
        #  automatically waits for readline to return something
        initialReadout = self.serPort.readline()
        initialReadout = self.serPort.readline()
        initialReadout = self.serPort.readline()
        
        print "Monochromator wavelength is"
        self.getWavelengthFromMemory()
        
    def setWavelengthInMemory(self, inputWavelength):
        self.inputWavelength = inputWavelength
        address = 0
        self.serPort.write('1')
        time.sleep(1.67)
        self.serPort.write(str(address))
        time.sleep(1.67)
        self.serPort.write(str(inputWavelength))
        time.sleep(1.67)
        print self.serPort.read(self.serPort.inWaiting())
  
    def getWavelengthFromMemory(self):
        self.serPort.write('2')
#        time.sleep(1.67)
#        storedWavelength = self.serPort.read(self.serPort.inWaiting())
        storedWavelength = self.serPort.read(4)
        self.storedWavelength = storedWavelength
        print storedWavelength
    
    def goToWavelength(self, chooseWavelengthInAngstroms):
        self.chooseWavelengthInAngstroms = chooseWavelengthInAngstroms
        if chooseWavelengthInAngstroms > 9950 or chooseWavelengthInAngstroms < 2500:
            print "Invaild monochromator wavelength"
        else:
            self.serPort.write('3')
            time.sleep(1.67)
            self.serPort.write(str(chooseWavelengthInAngstroms))
            time.sleep(1.67)
            out = self.serPort.read(self.serPort.inWaiting())
            #print out

    def stepUp(self):
        self.serPort.write('4')
        time.sleep(1)

    def stepDown(self):
        self.serPort.write('5')
        time.sleep(1)

    def getWavelength(self):
        self.serPort.write('6')
        time.sleep(1.67)
        currentWavelength = self.serPort.read(self.serPort.inWaiting())
        self.currentWavelength = currentWavelength
        print currentWavelength

    def closePort(self):
        self.serPort.close()

    def openPort(self, Port):
        self.serPort = serial.Serial(Port)
        time.sleep(1.67)
        print self.serPort.inWaiting()
        print self.serPort.read(self.serPort.inWaiting())

    def manualIncrementUp(self, low, high, inc):
        low = low
        high = high
        self.low = low
        self.high = high
        self.inc = inc
        difference = high - low
        if difference % inc == 0:
            while (low) <= high:
                self.goToWavelength(low)
                low = low + inc
        else:
            print "Cannot increment by that amount"

    def manualIncrementDown(self, High, Low, Inc):
        High = High
        Low = Low
        self.High = High
        self.Low = Low
        self.Inc = Inc
        Difference = High - Low
        if Difference % Inc == 0:
            while (Low) <= High:
                self.goToWavelength(High)
                High = High - Inc
                time.sleep(2)
        else:
            print "Cannot increment by that amount"

    def __del__(self):
        print "Final monochromator wavelength is"
        self.getWavelength()
        print "Saved value is"  
        self.getWavelengthFromMemory()
        finalWavelength = int(self.currentWavelength)
        if int(self.storedWavelength) != finalWavelength:
            print "Updating saved value."
            self.setWavelengthInMemory(finalWavelength)
        self.closePort()

    def shutDown(self):
        self.__del__()
    

if __name__ == "__main__":
    b = Mono('COM3')
    #b.setWavelengthInMemory(6990)
    