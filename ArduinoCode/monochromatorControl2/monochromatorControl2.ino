/*Written by Eric Tate 2014. Edited by Darby Hewitt, Candace Brooks and 
Ryan Wilson 2015. 
*/


#include <Adafruit_MotorShield.h>
#include <Wire.h>
#include <EEPROM.h>

Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
// Connect a stepper motor with 200 steps per revolution (1.8 degree)
// to motor port #2 (M3 and M4)
Adafruit_StepperMotor *myMotor = AFMS.getStepper(200, 2);

long address;
long currenteep; 
long current; 
long currenteep2;
long WVL,WVL2;
long dif;
long goldengoose;

long EEPROMReadlong(long address)
{
  //Read the 4 bytes from the eeprom memory.
  long four = EEPROM.read(address);
  long three = EEPROM.read(address + 1);
  long two = EEPROM.read(address + 2);
  long one = EEPROM.read(address + 3);

  //Return the recomposed long by using bitshift.
  return ((four << 0) & 0xFF) + ((three << 8) & 0xFFFF) + ((two << 16) & 0xFFFFFF) + ((one << 24) & 0xFFFFFFFF);
}

void EEPROMWritelong(int address, long value)
{
  //Decomposition from a long to 4 bytes by using bitshift.
  //One = Most significant -> Four = Least significant byte
  byte four = (value & 0xFF);
  byte three = ((value >> 8) & 0xFF);
  byte two = ((value >> 16) & 0xFF);
  byte one = ((value >> 24) & 0xFF);

  //Write the 4 bytes into the eeprom memory.
  EEPROM.write(address, four);
  EEPROM.write(address + 1, three);
  EEPROM.write(address + 2, two);
  EEPROM.write(address + 3, one);
}

void AX() {
 // Serial.println();
 // Serial.println("Set current wavelength in memory (EEPROM)");
//  Serial.println("What address would you like to save to: 0,4,8...");
  Serial.flush();
  while (!Serial.available());
  delay(300);
  if(Serial.available()){
    address = Serial.parseInt();
  }
 // Serial.println();
 // Serial.println("What is the current wavelength in Angstroms");
  Serial.flush();
  while (!Serial.available());
  delay(300);
  if(Serial.available()){
    currenteep2 = Serial.parseInt();
  }
  goldengoose = currenteep2;
  current = currenteep2;
  EEPROMWritelong(address ,currenteep2); // change 0 back to "address"
}   
void BX(){
  currenteep = EEPROMReadlong(0);   // change 0....  read "current" wavelength from eeprom

 // Serial.println();
 // Serial.print("The current wavelength saved to EEPROM is ");
  Serial.print(currenteep);
 // Serial.println(" Angstroms");
  Serial.flush();

  goldengoose = currenteep;
  current = currenteep;  
}
void CX(){
  //Serial.println();
  //Serial.println("What wavelength would you like to go to (in Angstroms)?");
  //Serial.println("DO NOT GO OVER 9950 OR BELOW 2500.");
  Serial.flush();
  while (!Serial.available());
  delay(300);
  if(Serial.available()){
    WVL2 = Serial.parseInt();
  }
  //Serial.print("You have entered ");
  //Serial.print(WVL2);
 // Serial.println(" Angstroms.");

  if(WVL2 > 9990 || WVL2 < 2500)
  {
   // Serial.println("You have entered an invalid wavelength.");
    Serial.flush();
    WVL2 = current;
  }

  dif = WVL2 - current;
  if(dif<0){
    dif = dif*(-1);
  }
  // int steps = dif/1.25; // 1/1 ratio
     int steps = dif/.3125; // 1/4   
 
  if( WVL2 > current ){
    myMotor->step(steps, FORWARD, SINGLE);
  }
  if( WVL2 < current ){
    myMotor->step(steps, BACKWARD, SINGLE);
  }
  current = WVL2;                
  goldengoose = WVL2;
}   
void DX(){
  myMotor->step(1, FORWARD, SINGLE);
  goldengoose = goldengoose + .3125;      
}
void EX(){
  myMotor->step(1, BACKWARD, SINGLE);
  goldengoose = goldengoose - .3125;      
}
void FX(){
  //Serial.println();
  //Serial.print("The current wavelength is ");
  Serial.print(goldengoose);
  //Serial.println(" Angstroms.");
}

void setup() {
  Serial.begin(9600);           // set up Serial library at 9600 bps
 // Serial.println("L A S E Rz");

  AFMS.begin();  // create with the default frequency 1.6KHz
  //AFMS.begin(1000);  // OR with a different frequency, say 1KHz
  myMotor->setSpeed(50);  
}

void loop() {
  int leprechaun = 0;

/*
  Serial.println("");
  Serial.println("Would you like to");
  Serial.println("1: Set current wavelength in memory");
  Serial.println("2: Get current wavelength from memory");
  Serial.println("3: Go to a wavelenth on the MC");
  Serial.println("4: Make a single step up   (+.3125 Angstroms)");
  Serial.println("5: Make a single step down (-.3125 Angstroms)");
  Serial.println("6: Get current wavelength");
  Serial.flush();
*/
  while (!Serial.available());
  //delay(300);
  if(Serial.available()){
    leprechaun = Serial.parseInt();
  }
  



////////////////////////////////////////////////////////////////////
  if(leprechaun == 1){
    AX();
  }
  ///////////////////////////////////////////////////////////////////
  if(leprechaun == 2){
    BX();
  }
  /////////////////////////////////////////////////////////////////////////////
  if(leprechaun == 3){
    CX();
  }
  ////////////////////////////////////////////////////////////////////
  if(leprechaun == 4){
    DX();
  }
  //////////////////////////////////////////////////////////////////
  if(leprechaun == 5){
    EX();
  }
  //////////////////////////////////////////////////////////////////
  if(leprechaun == 6){
    FX();
  }
  //////////////////////////////////////////////////////////////////

  delay(300);
}

//the end

