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
        #Opens up communication with the Arduino and empties the buffer
        #so that it is ready to receive input.
        self.serPort = serial.Serial(port, baudrate=115200)
        time.sleep(2)
        self.serPort.reset_input_buffer()
        self.serPort.reset_output_buffer()

        #Ensures that the local wavelength variable and the wavelength
        #variable stored in memory are synced on startup.
        self.getWavelengthFromMemory()

    def _wrt(self, input):
        #Sends the imput command over serial to the Arduino. Then, it waits
        #the Arduino sends a response back to say that it has received the
        #command.
        self.serPort.write(input)
        while(not self.serPort.in_waiting):
            pass
        time.sleep(.01)

    def _rd(self):
        #Reads everything waiting in the buffer, then strips it of
        #unnecessary white space, casts it as a string, and then returns it.
        return str(self.serPort.read(self.serPort.in_waiting)).strip()

        #After _wrt() is called, this function should be called before
        #calling _wrt() again. This allows Python and the Arduino to
        #properly wait for eachother to finish.

    def _roundToStepSize(self, value):
        diff = (value-4000) % .3125
        if diff <= .3125/2:
            return (value - diff)
        else:
            return (value - diff + .3125)
        return value

    def setWavelengthInMemory(self, inputWavelength):
        #Sends the command that corresponds to this method to the Arduino,
        #specifies the wavelength, and then returns the same wavelength.
        self._wrt(str(1))
        self.serPort.reset_input_buffer()
        self._wrt(str(inputWavelength))
        wvl = self._rd()                     #This read is necessary because the Arduino sends a response back to Python once it is done
        self.serPort.reset_input_buffer()
        return wvl

    def getWavelengthFromMemory(self):
        #Sends the command that corresponds to this method to the Arduino,
        #and then reads the Serial buffer, and returns the wavelength that
        #is stored in memory
        self._wrt('2')
        self.storedWavelength = self._rd()
        return self.storedWavelength

    def goToWavelength(self, chooseWavelengthInAngstroms):
        #First checks if the given wavelength is within the possible range
        roundedWavelength = self._roundToStepSize(chooseWavelengthInAngstroms)
        if roundedWavelength != chooseWavelengthInAngstroms:
            chooseWavelengthInAngstroms = roundedWavelength
            print "Rounded to "  + str(roundedWavelength)

        if chooseWavelengthInAngstroms > 9950 or chooseWavelengthInAngstroms < 2500:
            raise ValueError('Invalid monochromator wavelength')  #raises an error if it is out of range
        else:
            #Sends the command to the Arduino, reads its affirmative response,
            #then sends the wavelength, reads its response again, and then
            #returns it.
            self._wrt('3')
            self._rd()
            self._wrt(str(chooseWavelengthInAngstroms))
            out = self._rd()
            return out

    def stepUp(self):
        #Sends the corresponding command and then returns it.
        self._wrt('4')
        return self._rd()

    def stepDown(self):
        #Same as stepUp(), except for it sends the command corresponding to
        #the stepDown function in the Arduino.
        self._wrt('5')
        return self._rd()

    def getWavelength(self):
        #Sends the request to the Arduino, reads its response, updates the
        #current variable on the Python side, and then returns it.
        self._wrt('6')
        currentWavelength = self._rd()
        self.currentWavelength = currentWavelength
        return currentWavelength

    def release(self):
        self._wrt('7')
        return self._rd()

    def closePort(self):
        #Tells the Serial port to close
        self.serPort.close()

    def openPort(self, Port):
        #Opens the Serial port for communication
        self.serPort = serial.Serial(Port)
        time.sleep(1.67)
        print self.serPort.in_waiting
        print self.serPort.read(self.serPort.in_waiting)

    def __del__(self):
        #Checks to see if the local and memory variables are synced. If not,
        #calls getWavelengthFromMemory() in order to sync them. Then, it
        #closes the port.
        print "Final monochromator wavelength is"
        print self.getWavelength()
        print "Saved value is"
        print self.getWavelengthFromMemory()
        finalWavelength = float(self.currentWavelength)
        if float(self.storedWavelength) != finalWavelength:
            print "Updating saved value."
            self.setWavelengthInMemory(finalWavelength)
        print self.release()
        self.closePort()

    def shutDown(self):
        #Simply calls the destructor
        self.__del__()


if __name__ == "__main__":
    b = Mono('COM3')
