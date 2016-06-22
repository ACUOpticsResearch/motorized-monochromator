# Written by Candace Brooks and Darby Hewitt 2015.
#   functions for Agilent 34450A DMM to perform
#     make sure resource ID is correct if you have problems
#edited by Darby Hewitt on 8/17/15
# * removed from a class
# * measureVoltage now returns measurement
# * find the first visa resource with 'USB' in its ID

import visa

class Multimeter(object):
	def __init__(self, rm, visaID = ""):
		self.rm = rm
		lr = self.rm.list_resources()

		if visaID == "":
			for r in lr:
				if r.find('USB') >= 0:
					self.my_instrument = self.rm.open_resource(str(r))
					self.my_instrument.timeout = 10000
					temp_name = self.my_instrument.query('*IDN?')
					if temp_name.find('34450A') >= 0:
						break
					else:
						self.my_instrument.before_close()
						self.my_instrument.close()
		else:
			self.my_instrument = self.rm.open_resource(visaID)
			self.my_instrument.timeout = 10000

	def measureVoltageDC(self):
		measure = self.my_instrument.query('meas:volt:dc?')
		measure = measure.strip()
		return float (measure)

	def measureVoltageAC(self):
		measure = self.my_instrument.query('meas:volt:ac?')
		measure = measure.strip()
		return float (measure)

	def measureResistance(self):
		measure = self.my_instrument.query('meas:res?')
		measure = measure.strip()
		return float (measure)

	def measureCurrent(self):
		measure = self.my_instrument.query('meas:curr?')
		measure = measure.strip()
		return float (measure)

	def __del__(self):
		self.my_instrument.before_close()
		#self.my_instrument.clear()
		self.my_instrument.close()

if __name__=="__main__":
	rm = visa.ResourceManager()
	a = Multimeter(rm)
	print a.my_instrument.query('*IDN?')
	print a.measureVoltageDC()
