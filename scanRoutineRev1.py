# Written by Candace Brooks and Darby Hewitt 2015.
#condensed by Darby Hewitt on 8/16/2015
#Modified by Jared Barker 2016

#TO DO:
# un-class-ify this (DONE?)
# include flag to post data to screen during scan via matplotlib (DONE)
# implement real-time plotting
# put everything in a try:/except: so data taking can be exited gracefully (DONE?)
# export csv file instead of posting data struct to screen (updated, needs testing)

from monochromator import Mono
from multimeter import Multimeter
import visa

#startWvl and endWvl must have values between 2500 and 9950
def scanRoutine(port, startWvl, endWvl, numPtsPerWvl, stepSize, fileName, average = False):
    #Creates necessary objects. Also creates an empty array to store the measurements
    a = Mono(port)
    b = Multimeter(visa.ResourceManager())
    data = {}
    avg = {}

    #If it needs to go backwards, it adjusts the step size
    if startWvl > endWvl:
        stepSize = -stepSize

    my_file = open(fileName, "w")   #creates a file to write the measurements into
    a.goToWavelength(startWvl)      #moves to the starting wavelength
    try:    #put into a try statement in case of error
        #start at start wavelength, and increment by stepSize taking numPtsPerWvl data points at each wavelength
        for wvl in range(startWvl, endWvl, stepSize):
            a.goToWavelength(wvl)
            buf = [] #buffer for storing numPtsPerWvl data points
            for i in range(numPtsPerWvl):
                value = b.measureVoltageDC()                        #measures the Voltage
                buf.append(value)                                   #adds the measurement to the array
                my_file.write(str(wvl) + "," + str(value) + "\n")   #adds the wavelength and measurement to the file
            data[wvl] = buf                                         #adds the small array to the larger array
            if average:
                avg[wvl] = sum(buf)

        #Since the upper limit of ranger() is not inclusive, we must additiionally measure the voltage at the designated upper limit.
        a.goToWavelength(endWvl)
        buf = []
        for i in range(numPtsPerWvl):
            value = b.measureVoltageDC()
            buf.append(value)
            my_file.write(str(endWvl) + "," + str(value) + "\n")
        data[endWvl] = buf
        if average:
            avg[endWvl] = sum(buf)

        if average:
            my_file.write("\n\n")
            for wvl in avg:
                my_file.write(str(wvl) + "," + str(avg[wvl]) + "\n")

    except Expection as e:     #runs if an error occured during the try statement
        print "There was a scan routine error! Check the data file for clues!"
        print e

    finally:
        #closes the file
        my_file.close()

    return data

if __name__=="__main__":
    #scanRoutine(port, startWvl, endWvl, numPtsPerWvl, stepSize, fileName):
    scanRoutine('COM3', 6990, 7010, 2, 5, 'testWithVis.csv')
