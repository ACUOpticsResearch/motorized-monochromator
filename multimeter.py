# Written by Candace Brooks and Darby Hewitt 2015.
#   functions for Agilent 34450A DMM to perform
#     make sure resource ID is correct if you have problems
#edited by Darby Hewitt on 8/17/15
# * removed from a class
# * measureVoltage now returns measurement
# * find the first visa resource with 'USB' in its ID

import visa

rm = visa.ResourceManager()
lr = rm.list_resources()
my_instrument = 0


def measureVoltage():
	measurment = my_instrument.query('meas:volt:dc?')
	return measurment

for r in lr:
    if r.find('USB') >= 0:
        my_instrument = rm.open_resource(str(r))
        print "import of multimeter successful: "+str(r)
        print measureVoltage()
        break
        
	

  
if __name__=="__main__":
    print measureVoltage()
