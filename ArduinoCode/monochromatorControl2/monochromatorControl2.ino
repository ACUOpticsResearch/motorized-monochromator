/*Written by Aric Tate 2014. Edited by Darby Hewitt, Candace Brooks and 
Ryan Wilson 2015. 
Modified by Jared Barker 2016

What would you like to do?

1: Set current wavelength in memory
2: Get current wavelength from memory
3: Go to a wavelenth on the MC
4: Make a single step up   (+.3125 Angstroms)
5: Make a single step down (-.3125 Angstroms)
6: Get current wavelength
*/


#include <Adafruit_MotorShield.h>
#include <Wire.h>
#include <EEPROM.h>

Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
// Connect a stepper motor with 200 steps per revolution (1.8 degree)
// to motor port #2 (M3 and M4)
Adafruit_StepperMotor *myMotor = AFMS.getStepper(200, 2);

#define ADDR 0
float currentMemory;
float currentLocal;

float EEPROMReadFloat()
{
  //Read the 4 bytes from the eeprom memory.
  long four = EEPROM.read(ADDR);
  long three = EEPROM.read(ADDR + 1);
  long two = EEPROM.read(ADDR + 2);
  long one = EEPROM.read(ADDR + 3);

  //Return the recomposed long by using bitshift.
  return (float) ((four << 0) & 0xFF) + ((three << 8) & 0xFFFF) + ((two << 16) & 0xFFFFFF) + ((one << 24) & 0xFFFFFFFF);
}

float EEPROMWriteFloat(float value)
{
  //Decomposition from a long to 4 bytes by using bitshift.
  //One = Most significant -> Four = Least significant byte
  byte four = ((long)value & 0xFF);
  byte three = (((long)value >> 8) & 0xFF);
  byte two = (((long)value >> 16) & 0xFF);
  byte one = (((long)value >> 24) & 0xFF);

  //Write the 4 bytes into the eeprom memory.
  EEPROM.write(ADDR, four);
  EEPROM.write(ADDR + 1, three);
  EEPROM.write(ADDR + 2, two);
  EEPROM.write(ADDR + 3, one);
  
  return value;
}

float setWavelengthToMemory(float wave) {
  //Updates the two global variables, writes it into EEPROM, and returns the given wavelength
  currentLocal = wave;
  currentMemory = wave;
  return EEPROMWriteFloat(wave); // change 0 back to "address"
}   

float getWavelengthFromMemory(){
  //Reads from the EEPROM, updates the global variables, and then returns the wavelength that was read
  currentMemory = EEPROMReadFloat();   // change 0....  read "current" wavelength from eeprom
  currentLocal = currentMemory;
  return currentMemory;
}

float goToWavelength(float wave){
  //Checks if the wavelength is within the possible range
  if(wave > 9990 || wave < 2500)
  {
    //Invalid wavelength. Causes it to do nothing
    Serial.flush();
    wave = currentLocal;
  }

  int steps;

  //Calculates the number of steps the motor will need to turn in order to get to the desired wavelength
  int dif = wave - currentLocal;
  if(dif<0){
    dif = dif*(-1);
  }
  steps = dif/.31215;
 
  //Turns the motor in the needed direction for the calculated number of steps
  if( wave > currentLocal ){
    myMotor->step(steps, FORWARD, DOUBLE);
    myMotor->release();
  }
  if( wave < currentLocal ){
    myMotor->step(steps, BACKWARD, DOUBLE);
    myMotor->release();
  }
  
  //Keeps the variable up to date and then returns it
  currentLocal = wave;
  return currentLocal;
}   

float stepUp(){
  //Moves motor one step up and returns the new wavelength
  myMotor->step(1, FORWARD, DOUBLE);
  currentLocal = currentLocal + .3125;
  myMotor->release();
  return currentLocal;  
}

float stepDown(){
  //Moves motor one step down and returns the new wavelength
  myMotor->step(1, BACKWARD, DOUBLE);
  currentLocal = currentLocal - .3125;
  myMotor->release();
  return currentLocal;
}

void setup() {
  /*
  Sets up the necessary objects. Default frequency is 1.6 kHz. If another frequency is desired,
  it can be specified by using AFMS.begin(1000) for 1 kHz, for example. Also synchronizes the 
  the currentLocal and current Memory variables by calling getWavelengthFromMemory()
  */
  
  Serial.begin(115200);
  AFMS.begin();
  myMotor->setSpeed(50);
  getWavelengthFromMemory();  
}

void loop() {
  //Continually asks the user for a prompt, and then runs the command
  int action = 0;

  while (!Serial.available());
  if(Serial.available()){
    action = Serial.parseInt();
  }
  
  //Sets Wavelength in EEPROM
  if(action == 1){
    Serial.println("Ok");
    Serial.flush();
    while (!Serial.available());
    Serial.println(setWavelengthToMemory(Serial.parseFloat()));
  }
  
  //Prints the Wavelength Saved in EEPROM
  if(action == 2){
    Serial.println(getWavelengthFromMemory());
    Serial.flush();
  }
  
  //Moves the Monochromator to a Specific Wavelength
  if(action == 3){
    Serial.println("Ok");
    while (!Serial.available());
    Serial.println(goToWavelength(Serial.parseFloat()));
  }
  
  //Steps Up the Wavelength
  if(action == 4){
    Serial.println(stepUp());
  }
  
  //Steps Down the Wavelength
  if(action == 5){
    Serial.println(stepDown());
  }
  
  //Prints the Local Wavelength
  if(action == 6){
    Serial.println(currentLocal);
  }
}

//The End

