# Written by Candace Brooks and Darby Hewitt 2015.

import monochromator
import multimeter
import serial
import time

class Wvl(object):
    def __init__(self, port):
        a = monochromator.Mono(port)
        b = multimeter.volt()
        self.a = a
        self.b = b
    
    def scanWvl(self, startWvl, endWvl, numPtsPerWvl, stepSize, fileName):
        self.startWvl = startWvl
        self.endWvl = endWvl
        self.numPtsPerWvl = numPtsPerWvl
        self.stepSize = stepSize
        self.fileName = fileName
        backup = numPtsPerWvl
        data = {}
        if startWvl < endWvl:
            differ = endWvl - startWvl
            if differ % stepSize == 0:
                while startWvl <= endWvl:
                    numPtsPerWvl = backup
                    hold = []
                    while numPtsPerWvl > 0:
                        self.a.goToWavelength(startWvl)
                        self.b.take()
                        hold.append(self.b.measurment)
                        data[startWvl] = hold
                        numPtsPerWvl = numPtsPerWvl - 1
                    startWvl = startWvl + stepSize
            else:
                print "Cannot increment by that amount"

        else:
            Differ = startWvl - endWvl
            if Differ % stepSize == 0:
                while startWvl >= endWvl:
                    numPtsPerWvl = backup
                    hold = []
                    while numPtsPerWvl > 0:
                        self.a.goToWavelength(startWvl)
                        self.b.take()
                        hold.append(self.b.measurment)
                        data[startWvl] = hold
                        numPtsPerWvl = numPtsPerWvl - 1
                    startWvl = startWvl - stepSize
            else:
                print "Cannot increment by that amount"
        my_file = open(fileName, "w")
        for item in data:
            my_file.write(str(item)+","+str(data[item])[4:18]+"\n")
        my_file.close()
        
        #print data
        return data

    def end(self):
        self.a.shutDown()

    
