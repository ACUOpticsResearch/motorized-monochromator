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

plt.subplots_adjust(hspace=0)

plt.subplot(2, 1, 1)
plt.plot(measuredWavelength,measuredIntensity, label='Measured')
plt.axvline(x=640, ls='dashed', color='black')
plt.axvline(x=638, ls='dashed', color='black')
plt.axvline(x=650.5, ls='dashed', color='black')
plt.axvline(x=633, ls='dashed', color='black')
plt.axvline(x=660, ls='dashed', color='black')
plt.axvline(x=614.3, ls='dashed', color='black')
plt.axvline(x=693, ls='dashed', color='black')
plt.axvline(x=667.8, ls='dashed', color='black')
plt.axvline(x=585.2, ls='dashed', color='black')
plt.axvline(x=607, ls='dashed', color='black')
plt.axvline(x=603, ls='dashed', color='black')
plt.title('Neon Atomic Spectrum')
plt.ylabel('Relative Intensity', fontsize='large')
plt.annotate('Measured', xy=(640,1), xytext=(587, .9), fontsize='x-large', backgroundcolor='white')
plt.tick_params(axis='x', which='both', labelbottom='off')
plt.yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0], ['0', '0.2', '0.4', '0.6', '0.8', '1.0'])
plt.axis([580,700,0,1.1])

plt.subplot(2, 1, 2)
plt.plot(NISTWavelength,NISTIntensity, label='NIST')
plt.axvline(x=640, ls='dashed', color='black')
plt.axvline(x=638, ls='dashed', color='black')
plt.axvline(x=650.5, ls='dashed', color='black')
plt.axvline(x=633, ls='dashed', color='black')
plt.axvline(x=660, ls='dashed', color='black')
plt.axvline(x=614.3, ls='dashed', color='black')
plt.axvline(x=693, ls='dashed', color='black')
plt.axvline(x=667.8, ls='dashed', color='black')
plt.axvline(x=585.2, ls='dashed', color='black')
plt.axvline(x=607, ls='dashed', color='black')
plt.axvline(x=603, ls='dashed', color='black')
plt.ylabel('Relative Intensity', fontsize='large')
plt.xlabel('Wavelength (nm)', fontsize='large')
plt.axis([580,700,0,1.1])
plt.annotate('Known Lines', xy=(640,1), xytext=(587, .9), fontsize='x-large', backgroundcolor='white')
plt.annotate('(NIST Atomic Spectra Database)', xy=(640,1), xytext=(587, .8), fontsize='small', backgroundcolor='white')
plt.yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0], ['0', '0.2', '0.4', '0.6', '0.8', '1.0'])

plt.show()
