# Written by Candace Brooks and Darby Hewitt 2015.
#   functions for Agilent 34450A DMM to perform
#     make sure resource ID is correct if you have problems
#edited by Darby Hewitt on 8/17/15
# * removed from a class
# * measureVoltage now returns measurement
# * find the first visa resource with 'USB' in its ID
#Edited by Jared Barker 2016
# * now is in a class
# * added functionality for resistance, current, and AC Voltage

import visa

class Multimeter(object):
	def __init__(self, rm, visaID = ""):
		#Creates a list of all devices interacting with the computer.
		self.rm = rm
		lr = self.rm.list_resources()

		if visaID == "":	#if visaID is not specified
			for r in lr:	#looks through everything in the list
				if r.find('USB') >= 0:	#checks to see if the word 'USB' is in its ID, implying that it is connected via USB
					self.my_instrument = self.rm.open_resource(str(r))	#assigns the instrument to my_instrument
					self.my_instrument.timeout = 10000	#increases the timeout threshold to 10 seconds (prevents some errors that can occur later on)
					temp_name = self.my_instrument.query('*IDN?') #this command tells the instrument to identify itself
					if temp_name.find('34450A') >= 0:	#if its identification includes '34450A' (the model of the multimeter) then it quits the loop and keeps the multimeter assigned to my_instrument
						break
					else:
						self.my_instrument.before_close()	#if it is not the multimeter, it closes the instrument
						self.my_instrument.close()
		else:	#if visaID is specified
			self.my_instrument = self.rm.open_resource(visaID)	#looks the instrument up by its ID
			self.my_instrument.timeout = 10000	#increases timeout, similarly to above

	def measureVoltageDC(self):
		measure = self.my_instrument.query('meas:volt:dc?')	#asks instrument to measure the DC Voltage, returns a string
		measure = measure.strip()							#strips the whitespace off of the string
		return float (measure)								#casts it as a float, and returns it

	def measureVoltageAC(self):
		measure = self.my_instrument.query('meas:volt:ac?')	#asks instrument to measure the AC Voltage, returns a string
		measure = measure.strip()							#strips the whitespace off of the string
		return float (measure)								#casts it as a float, and returns it

	def measureResistance(self):
		measure = self.my_instrument.query('meas:res?')		#asks instrument to measure the resistance, returns a string
		measure = measure.strip()							#strips the whitespace off of the string
		return float (measure)								#casts it as a float, and returns it

	def measureCurrent(self):
		measure = self.my_instrument.query('meas:curr?')	#asks instrument to measure the current, returns a string
		measure = measure.strip()							#strips the whitespace off of the string
		return float (measure)								#casts it as a float, and returns it

	def __del__(self):
		self.my_instrument.before_close()					#these two methods are required in order to properly close the instrument
		self.my_instrument.close()

if __name__=="__main__":
	rm = visa.ResourceManager()
	a = Multimeter(rm)
	print a.my_instrument.query('*IDN?')
	print a.measureVoltageDC()
