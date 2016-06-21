# Written by Candace Brooks and Darby Hewitt 2015.
#   functions for Agilent 34450A DMM to perform
#     make sure resource ID is correct if you have problems
#edited by Darby Hewitt on 8/17/15
# * removed from a class
# * measureVoltage now returns measurement
# * find the first visa resource with 'USB' in its ID

import visa

class Multimeter(object):
	def __init__(self, visaID = ""):
		self.rm = visa.ResourceManager()
		lr = self.rm.list_resources()

		if visaID == "":
			for r in lr:
				if r.find('USB') >= 0:
					self.my_instrument = self.rm.open_resource(str(r))
					self.my_instrument.timeout = 10000
					temp_name = self.my_instrument.query('*IDN?')
					if temp_name.find('33450A') >= 0:
						print "Import of multimeter successful: " + str(r)
						break
		else:
			self.my_instrument = self.rm.open_resource(visaID)
			self.my_instrument.timeout = 10000
			print "Import of multimeter successful: " + visaID

	def measureVoltage(self):
		return self.my_instrument.query('meas:volt:dc?')

	def measureResistance(self):
		return self.my_instrument.query('meas:res?')

	def measureCurrent(self):
		return self.my_instrument.query('meas:curr?')

	def __del__(self):
		self.rm.close()

if __name__=="__main__":
	print "A"
	a = Multimeter()
	print "B"
	print a.my_instrument.query('*IDN?')
	print "C"
	print a.my_instrument.query('meas:volt:dc?')
#	print a.measureVoltage()
