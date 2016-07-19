#NIST File converter
#By Jared Barker


import csv
with open('NISTAdjustedData.csv', 'rb') as f:
    reader = csv.reader(f)
    your_list = list(reader)

my_file = open('NISTDataWithSpikes.csv', "w")

for spike in your_list:
    my_file.write(str(float(spike[0]) - 3) + ",0\n")
    my_file.write(spike[0] + "," + spike[1] + "\n")
    my_file.write(str(float(spike[0]) + 3) + ",0\n")

my_file.close()
