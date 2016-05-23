# monochromator-modernizing
Arduino and Python code associated with the motorization and automation of a monochromator.

The stepper motor on the monochromator is controlled by the Arduino sketch in this repository. This receives serial commands and sends messages over serial in reply. 

The file 'monochromator.py' defines the Monochromator class, which wraps the serial interface for the arduino-controlled stepper motor attached to the monochromator.
