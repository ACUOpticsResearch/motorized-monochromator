Before trying to get this code to work, make sure you
have my other two codes (monochromator and multimeter)
working.

The function __init__ has one input, port. Whatever port
you use for monochromator, you should use for this code 
too. This function runs automatically when you call the 
class and it connects the Arduino to the computer and 
connects this code to my other two codes.

The function scanWvl has five inputs. startWvl is the
wavelength you want to start the scan with (in Angstroms).
endWvl is the wavelength you want to end the scan with 
(in Angstroms). numPtsPerWvl is how many times you want 
to measure the voltage per step. stepSize is how big you 
want the steps to be between the the startWvl and the 
endWvl. fileName is the file you want to save the results
to. If you want to save the results to a text file, make 
sure to use .txt to end your file name with. This function
has multiple if and while loops to take the data and save
it into empty variables. After the data is taken, it is
rewritten into a file and saved.   

An example of using this function would be the input
scanWvl(5000, 5100, 1, 50, "example.txt") would give
you a text file with the contents simular to:
5000,5.84793E-02 
5050,5.87563E-02
5100,5.90264E-02

I have not tested saving a file with more than one 
voltage measurement. You may have to fix the code to make 
that work. Also, you may want to make it so that if you 
have more than one voltage, that the average of those
voltages are taken and saved. Another thing you may need 
to fix is to add an interupt in case you have to stop
the code in the middle of the data collection or if an 
error occurs in the middle of the data collection. 

The end function shuts off the connection to the port 
properly and should be used before exiting out of the 
code, or you may need to restart the computer.

Good luck and happy data collecting!


