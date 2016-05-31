# Written by Candace Brooks and Darby Hewitt 2015.
#condensed by Darby Hewitt on 8/16/2015

#TO DO: 
# un-class-ify this (DONE?)
# include flag to post data to screen during scan via matplotlib (DONE)
# implement real-time plotting
# put everything in a try:/except: so data taking can be exited gracefully (DONE?)
# export csv file instead of posting data struct to screen (updated, needs testing)
# Jared waz here

import monochromator
import multimeter
#import matplotlib #only needed if realTimeOut flag is set to true
import serial #necessary?
import time #necessary?

def scanRoutine(port, startWvl, endWvl, numPtsPerWvl, stepSize, fileName, realTimeOut=False):
    a = monochromator.Mono(port)
    #time.sleep(4)
    backup = numPtsPerWvl
    data = {}

#step backwards if necessary
    if startWvl > endWvl: 
        stepSize = -stepSize

#do we want to plot data in real time? How much should be done here?
    if realTimeOut:
        import numpy as np
        import matplotlib.pyplot as plt

		#define pltWvl and pltAmp arrays here
		pltWvl = [startWvl-stepSize]+range(startWvl, endWvl, stepSize)
		pltAmp = [multimeter.measureVoltage()]
		#then:
		line, = plt.plot(np.array(pltWvl)[0], np.array(pltAmp)[0], 'b-', linewidth=2)
		dashes = [10, 5, 100, 5] # 10 points on, 5 off, 100 on, 5 off
		line.set_dashes(dashes)
		
		if stepSize > 0:
			plt.axis([startWvl,endWvl,0,.5])
		else:
			plt.axis([endWvl,startWvl,0,.5])
		
		plt.ion()
		plt.show()
		curIndex = 1
		
    #a.goToWavelength(startWvl) #should I go here before the loop?
    print range(startWvl, endWvl, stepSize)
    try:
        #start at start wavelength, and increment by stepSize taking numPtsPerWvl data points at each wvl
        for wvl in range(startWvl, endWvl, stepSize):
            a.goToWavelength(wvl)
            buf = [] #buffer for storing numPtsPerWvl data points
            for i in range(numPtsPerWvl):
                buf.append(multimeter.measureVoltage())

            data[wvl] = buf

            if realTimeOut:
				#get average of buf and store in pltAmp for real-time
				sum = 0
				for n in buf:
					sum += n
				pltAmp.append(sum)
			
				curIndex +=1
				
				line, = plt.plot(np.array(pltWvl)[1:curIndex], np.array(pltAmp)[1:curIndex], 'b-', linewidth=2)
				plt.draw()
			
        #include endWvl values, too
        a.goToWavelength(endWvl)
        buf = [] #buffer for storing numPtsPerWvl data points
        for i in range(numPtsPerWvl):
            buf.append(multimeter.measureVoltage())

        data[endWvl] = buf
    except:
        print "There was a scan routine error! Check the data file for clues!"

    finally:
        # FILE STUFF BELOW.

        my_file = open(fileName, "w")
        for item in data:
            for val in data[item]:
                my_file.write(str(item)+","+str(val)[4:18]+"\n")

        my_file.close()

        #a.shutDown() #close and destroy link to com port; shouldn't need to call this

    return data

if __name__=="__main__":
    scanRoutine('COM3', 6990, 7010, 2, 5, 'testWithVis.csv', True)
    #scanRoutine(port, startWvl, endWvl, numPtsPerWvl, stepSize, fileName, realTimeOut=false):
