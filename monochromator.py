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
# edited by Darby Hewitt 5/31/2016
# * adding return values to all methods in order to minimize timing errors
# * also replacing fixed delays between serial writes to serial reads
#
# edited by Darby 6/2/16
# * ripped Jared's wrt and rd functions from


import serial
import time

class Mono(object):
    def __init__(self, port):
        self.serPort = serial.Serial(port, baudrate=115200)
        time.sleep(2)
        #numberOfCharacters = self.serPort.in_waiting
        #below is a better way to wait than just sleeping;
        #  also it clears the buffer. assignment to initialReadout
        #  automatically waits for readline to return something
        #initialReadout = self.serPort.readline()
        #initialReadout = self.serPort.readline()
        #initialReadout = self.serPort.readline()
        self.serPort.reset_input_buffer()
        self.serPort.reset_output_buffer()
        #print "Monochromator wavelength is"
        self.getWavelengthFromMemory()

    def __wrt__(self, input):
        self.serPort.write(input)
        while(not self.serPort.in_waiting):
            pass
        time.sleep(.01)

    def __rd__(self):
        return str(self.serPort.read(self.serPort.in_waiting)).strip()

    def setWavelengthInMemory(self, inputWavelength):
        self.__wrt__(str(1))
        #time.sleep(1.67)
        #while(self.serPort.in_waiting == 0):
            # this should do nothing until something is in the input buffer
        #    pass
        #flush input buffer
        self.serPort.reset_input_buffer()

        #self.serPort.write(str(address))
        #while(self.serPort.in_waiting == 0):
            # this should do nothing until something is in the input buffer
        #    pass
        #flush input buffer
        #self.serPort.reset_input_buffer()

        self.__wrt__(str(inputWavelength))

        #while(self.serPort.in_waiting == 0):
            # this should do nothing until something is in the input buffer
        #    pass

        #output contents of input buffer
        wvl = self.__rd__()
        #reset input buffer after read
        self.serPort.reset_input_buffer()
        #print wvl
        return wvl

    def getWavelengthFromMemory(self):
        self.__wrt__('2')
#        time.sleep(1.67)
#        storedWavelength = self.serPort.read(self.serPort.in_waiting)

        #wait for available bytes
        #while(self.serPort.in_waiting == 0)
        #    pass

        self.storedWavelength = self.__rd__()
        return self.storedWavelength

    def goToWavelength(self, chooseWavelengthInAngstroms):
        self.chooseWavelengthInAngstroms = chooseWavelengthInAngstroms
        if chooseWavelengthInAngstroms > 9950 or chooseWavelengthInAngstroms < 2500:
            raise ValueError('Invalid monochromator wavelength')
        else:
            self.__wrt__('3')
            #time.sleep(1.67)
            self.__rd__()
            self.__wrt__(str(chooseWavelengthInAngstroms))
            #time.sleep(1.67)
            out = self.__rd__()
            #print out
            return out

    def stepUp(self):
        self.__wrt__('4')
        #time.sleep(1)
        return self.__rd__()

    def stepDown(self):
        self.__wrt__('5')
        #time.sleep(1)
        return self.__rd__()

    def getWavelength(self):
        self.__wrt__('6')
        #time.sleep(1.67)
        currentWavelength = self.__rd__()
        self.currentWavelength = currentWavelength
        return currentWavelength

    def closePort(self):
        self.serPort.close()

    def openPort(self, Port):
        self.serPort = serial.Serial(Port)
        time.sleep(1.67)
        print self.serPort.in_waiting
        print self.serPort.read(self.serPort.in_waiting)

    def __del__(self):
        print "Final monochromator wavelength is"
        print self.getWavelength()
        print "Saved value is"
        print self.getWavelengthFromMemory()
        finalWavelength = float(self.currentWavelength)
        if float(self.storedWavelength) != finalWavelength:
            print "Updating saved value."
            self.setWavelengthInMemory(finalWavelength)
        self.closePort()

    def shutDown(self):
        self.__del__()


if __name__ == "__main__":
    b = Mono('COM3')
    #b.setWavelengthInMemory(6990)
