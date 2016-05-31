This code is written as a class with seperate functions
so that it works better with the scanRoutine code. You 
could try playing around with where the code is in the 
two functions. I just made the __init__ code empty so
I would not have to bother with it. 

In order to make this code work, you have to connect a
multimeter into a USB port. Also, you have to download
PyVISA onto your computer. It can be hard to download 
but this website should help you at least get started.
http://pyvisa.readthedocs.org/en/latest/getting.html 

The code is currently written in a way that you have to 
manually add the resource you want to open. The resource
depends on the multimeter you use. The print command 
that is currently commented out will help you. Just
un-comment it, and comment out everything out after it.
It will print out a list of resources for you to chose 
from. The multimeter should have a name simular to 
'USB0::0x0957::0xB318::MY54420048::INSTR'. When you find
it, use that number to replace the resource that is in
rm.open_resource(). Then comment out the print command 
and un-comment the last three lines.

If the code is working, run the function take() and the 
multimeter should flash and then the display should not 
change numbers.

You could try to make the code work in a way that allows 
you to choose your resource without you having to rewrite 
the code. 

 