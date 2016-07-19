#Plotter for .csv files created from measurements
#By Jared Barker

import matplotlib.pyplot as plt
import csv

measuredWavelength = []
measuredIntensity = []
NISTWavelength = []
NISTIntensity = []

with open('AdjustedNeonDataNanometers.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        measuredWavelength.append(float(row[0]))
        measuredIntensity.append((float(row[1])-.53)/(0.307346394))

with open('AdjustedNeonNISTDataNanometers.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        NISTWavelength.append(float(row[0]))
        NISTIntensity.append(float(row[1])*2)

plt.subplot(2, 1, 1)
plt.plot(measuredWavelength,measuredIntensity, label='Measured')
plt.title('Ne I Atomic Spectra')
plt.ylabel('Relative Intensity')

plt.axis([580,700,0,1.05])

plt.subplot(2, 1, 2)
plt.plot(NISTWavelength,NISTIntensity, label='NIST')
plt.ylabel('Relative Intensity')
plt.xlabel('Wavelength (nm)')
plt.axis([580,700,0,1.05])

plt.show()
