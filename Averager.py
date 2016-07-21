#CSV Averager
#By Jared Barker

import csv
with open('LaserNoSlit.csv', 'rb') as f:
    reader = csv.reader(f)
    your_list = list(reader)

my_file = open('LaserNoSlitAverage.csv', "w")
currentWavelength = 5000
average = 0

for point in your_list:
    if point[0] == currentWavelength:
        average = average + float(point[1])
    else:
        my_file.write(str(currentWavelength) + ',' + str(average) + '\n')
        currentWavelength = point[0]
        average = float(point[1])

my_file.close()
