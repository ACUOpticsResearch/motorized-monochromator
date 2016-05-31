It is important that this code works with the edited Aurduino code written by Aric.

All of the time.sleep commands throughout the program are there to give the 
monochromator a chance to read and preform the other commands. You can add longer
times and play with these if you wish, the current times are the shortest times
that work. These commands also require the import time at the top, so make sure
you have that loaded.

The __init__ function opens automatically whenever you start the class. 
It allows you to chose the port that the Aurduino is connected to.
It also reads off the existing characters so that they do not clutter the
other functions. It fetches the saved wavelength so that you can check if it 
matches the monochromator. These are the last two lines and they are necessary 
somewhat to prevent confusion within the code. You do not need the print line but 
you do need to run the function getWavelengthFromMemory 

The setWavelengthInMemory function is self explanatory. It automatically writes and 
the wavelength in address 0 every time. It then sends '1' to Aric's code, then the 
address 0, then the entered wavelength, in order to run the code that resets the 
memory. The rest of this code is written to use this function as few times as 
possible, because of the limited rewrite space. 

The getWavelengthFromMemory uses Aric's code to read the current saved wavelength 
from the memory. Note that this may not be the same wavelength as the current
wavelength. This is because of the limited number of times this number can be 
rewritten. As long as this value (which is called at the beginning of the class)
is the same as the value on the monochromator at the beginning, the code is working.

The goToWavelength function uses Aric's code to turn the motor and go to the entered 
wavelength. You can only go to wavelengths between 2500 and 9950 Angstroms. The 
monochromator reads in nanometers while the code is written to read Angstroms 
(nanometers*10 = Angstroms). The code has a built in failsafe to prevent the wrong 
wavelength from being entered. If you do not enter a number in the correct range, you
will get the message "Invaild monochromator wavelength" 

The stepUp function goes up a step. This function does not save the current 
wavelength very well, especially when used a lot. The problem might lie within Aric's
code, but I am not sure how to fix it. I find it best to use the goToWavelength 
function whenever you want to move the motor. None of my other codes rely on this
function, it is just here because it was in Aric's code.

The stepDown function is the inverse of the stepUp function. Please read the section
on the stepUp function before using.

The getWavelength function gets the current wavelength. The output of this function
should always match the monochromator's wavelength. 

The closePort function closes the port only. I suggest only using this when the 
current memory and the stored memory are the same, or else the wavelength will be 
wrong next time you use this class. The shutDown program should be used instead.

The openPort function is to be used if you close the port and wish to reopen it 
without restarting the class. It can only be used after closePort or shutDown.

The manualIncrementUp function allows you to automatically cycle through desired
wavelengths. You put in the wavelength you want to start with, the greater wavelength
you want to end at (this one is included), and the increment you want use in between 
the two. For example, if you want to cycle through 5000, 5100, 5200, 5300, 5400, 5500
enter, (5000, 5500, 100). If the increment does not divide evenly between the two
wavelengths, you will get the message "Cannot increment by that amount" You must 
start at the smaller value and work up, or this function will not work. If you want
to cycle down, use the manualIncrementDown function. It is possible to combine these
two functions, so you don't have to worry about incrementing up or down. I never got
around to it in this class, but if you have access to my scanRoutine class, you could
look at the scanWvl function and base it off that.  

The manualIncrementDown function allows you to automatically cycle through desired
wavelengths. You put in the wavelength you want to start with, the lesser wavelength
you want to end at (this one is included), and the increment you want use in between 
the two. For example, if you want to cycle through 5500, 5400, 5300, 5200, 5100, 5000
enter, (5500, 5000, 100). If the increment does not divide evenly between the two
wavelengths, you will get the message "Cannot increment by that amount" You must 
start at the larger value and work down, or this function will not work. If you want
to cycle up, use the manualIncrementUp function. It is possible to combine these
two functions, so you don't have to worry about incrementing up or down. I never got
around to it in this class, but if you have access to my scanRoutine class, you could
look at the scanWvl function and base it off that.

The shutDown function properly updates the Arduino memory, closes the port, and ends 
the program. PLEASE use this function before you exit the Python shell every time. It 
does not update the memory if the current wavelength and the wavelength in memory are
the same, so it will not waste memory space. It is important to close out of the port
properly or the computer may need to restart.

The __del__ function is what causes the program to close. It is meant to be used in
the shutDown function, not by itself. You need to have a function called __del__
to close the program but it doesn't pop up on the scroll down menu so I wrote a 
separate shutDown function instead of making this function the ending function. It 
can be used on it's own and it will shut the port, but it will not update the memory 
so I don't suggest calling it manually. 

This part at the end:
if __name__ == "__main__":
    b = Mono('COM3')
This was written by Dr. Hewitt so I'm not sure exactly how it works but it is 
basically a failsafe to make sure the port is open properly. It might not be 
needed but ask Dr. Hewitt before you delete it (if you can). It only works if the
Aurdino is plugged into COM3 (it usually is).

Now that I have gone though the code, I will give an example of how to open it, go
to 5000 Angstroms and then close it. [The comments (after #) are just explanations
so you do not need to add them]:
import monochromator  #This works if the code is saved as monochromator
a = monochromator.Mono('COM3') #This opens the class and the port COM3 (a can be anything)
a.goToWavelength(5000)
a.shutDown()

Tips: 
1. Use shutDown() before you exit the program!

2. Make sure you have the two libraries serial and time. You need pyserial to use the
serial libary, which you can download here:https://pypi.python.org/pypi/pyserial
You should be able to use the pyserial-2.7.win32.exe (md5) link for a Windows
After the download, this site http://pyserial.sourceforge.net/pyserial.html#installation
should help you install it. Just click install on the left of the screen.

3. In the above example, after defining a, if you type a. and wait, a pulldown 
menu should pop up to give you your options. This is useful if you forget the 
function names. Use the up/down arrow keys to highlight the one you want and push
enter to chose it. It also works when you type monochromator. to pull up the name of 
the class

4. In the above example, You can put import monochromator as mono (or any name of 
your choice) instead of import monochromator. After that, you can type mono instead 
of monochromator

I believe that's it. Good luck running this code! If you want to ask me something, 
try emailing me at cdb11d@acu.edu I can't promise I'll remember how to work it, but
I'll help if I can. 