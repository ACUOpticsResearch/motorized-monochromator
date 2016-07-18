#NIST File converter
#By Jared Barker


import csv
with open('file.csv', 'rb') as f:
    reader = csv.reader(f)
    your_list = list(reader)

print your_list
