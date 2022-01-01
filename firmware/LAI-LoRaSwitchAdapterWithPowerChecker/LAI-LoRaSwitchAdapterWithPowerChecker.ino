/*
 * < LAYGOND-AI >
 * Device Title: LAI-LoRaSwitchAdapterWithPowerChecker
 * Device Description: A servo that acts as an elevator's power switch through LoRa messages
 * Device Explanation: The device(at Lobby) receives a LoRa message from the 
 *                     server(in elevator) to rotate a servo motor that will 
 *                     turn on/off the elevator main power switch. Verification 
 *                     of elevator's mains power is done locally with a CT clamp. 
 *                     
 * Author: Bryan Laygond
 * Github: @laygond
 * 
 * Inspired by: 
 * - Bill        https://dronebotworkshop.com/
 * - Anthonywebb https://github.com/anthonywebb/
 * - OpenEnergyMonitor  https://learn.openenergymonitor.org/
 * 
 * Code may only be distributed through https://github.com/laygond/Elevator-AI any 
 * other methods of obtaining or distributing are prohibited.
 * < LAYGOND-AI > Copyright (c) 2020
 * 
 * 
 * PREREQUISITES:
 *  Libraries
 * - EmonLib.h by https://learn.openenergymonitor.org/electricity-monitoring/ct-sensors/interface-with-arduino 
 * - rfm92w.h  is included and was adapted from https://github.com/anthonywebb/RFM92 
 * 
 * Board (ESP8266)
 * - Append http://arduino.esp8266.com/stable/package_esp8266com_index.json at 'File/Preferences/Additional Board Manage URL'
 * - install esp8266 by ESP8266 Community Version 2.5.0 from 'Tools/Boards/Board Manager'
 * 
 * HARDWARE & SCHEMATICS:
 * - Current Transformer Sensor Clamp 100amp/50mA resolution SCT013-000 https://learn.openenergymonitor.org/electricity-monitoring/ct-sensors/measurement-implications-of-adc-resolution-at-low-current-values
 * - Servo Motor DS3225MG
 * - RobotDyn's Mosfet with optocoupler IRF540N and EL817 (s->3.3,GND->D0 so that it acts as active low; since D0 high at boot)
 * - LoRa HopeRF rfm92w   (PIN CONNECTIONS at rfm92w.h)
 * 
 * FIND IDEAL BURDEN RESISTOR ACCROSS CLAMP SCT013-000:
 * https://learn.openenergymonitor.org/electricity-monitoring/ct-sensors/interface-with-arduino
      float primary_RMS_current = 140.0;         //max current
      float primary_peak_current = primary_RMS_current * 1.414;     // sqrt(2)= 1.414
      float secondary_peak_current = primary_peak_current / 2000.0; // sct013 clamp has 2000 turns
      float AREF = 3.3;   //voltage reference in esp8266
      float ideal_burden_resistance = (AREF/2) / secondary_peak_current; // half only so that it oscillates between +-(AREF/2)
                                                                         // then add an offset of AREF/2 so that [0,AREF] interval
                                                                         // offset is achieved through voltage divider and capacitor
 */
#include "EmonLib.h"
#include <Servo.h> 
#include "rfm92w.h"    // antenna pins are defined at "rfm92w.h"
                   
EnergyMonitor emon1;   // monitors current with CT clamp                
Servo myservo1;        // acts as a switch
int servoPin = D2;     // Servo's control signal pin
int servoPowerPin = D0;// Mosfet&Optocoupler's pin to control power to Servo
char msg[11];          // Variable to receive Lora Message

void setup() 
{
  pinMode(servoPowerPin, OUTPUT);    //Start Servo deactivated
  digitalWrite(servoPowerPin, HIGH); //Since Active Low
  beginLoraRX();              
  emon1.current(A0, 115.81);  //calibration factor of 115.81 for max current
                              //of 140 Amps with 16.66 ohm burden resistor
}

void loop() 
{
  //Await LoRa Message
  if(digitalRead(dio0) == 1)
  {
     receiveMessage(msg);
     //Serial.print(msg);
     //Serial.println("\n");
     if (strcmp(msg, "OFF")==0 || strcmp(msg, "ONN")==0)//yes two N's since 2 character noise 'NO' is possible 
     {
        //Serial.println("HELLO ACTION BABY\n");
        actionSwitch(msg);      
     }
  }
 }

 
/**
 * Moves servo based on receiving message. Since elevator switch is a  
 * 2-way switch (like a staircase wiring method), both directions are tried
 * until power reading matches receiving msg command.
 */
void actionSwitch( char *msgString)
{
  if (strcmp(msgString, "ONN")==0){
      if (isPowerON()==false){//power is OFF
          moveSwitch(10);     //degree difference from a 90 degree position
          if (isPowerON()==false){//power still OFF try other way
              moveSwitch(-10);}}}   
  else if (strcmp(msgString, "OFF")==0){
      if (isPowerON()==true){
          moveSwitch(10);   
          if (isPowerON()==true){//power still ON try other way
              moveSwitch(-10);}}}
 }
 

/**
// * Returns true if power in elevator is ON, false otherwise.
// * Five readings are taken with the Emon Library before returning
// */
boolean isPowerON()
{
  double val;             //Amperage reading value in RMS 
  int decision_total = 0; //decision tracker
  double threshold = 0.6;  //Amps 
  //Take five readings
  for (int i = 0; i < 5; i++){
      val = emon1.calcIrms(1480);  // Calculate Irms by taking 1480 measurements
      //Serial.println(val);  
      while (val == threshold){// Keep taking measurements 
          val = emon1.calcIrms(1480);}
      if (val > threshold){    
          decision_total += 1;}       
      else if (val < threshold){
          decision_total -= 1;}}
  //Final Criteria
  if (decision_total > 0){
      return true;}
  else{
      return false;}
}


/**
 * Moves servo to center, then to specified delta position, and finally back to center 
 */
void moveSwitch(double delta) //degree difference from a 90 degree position   
{  
  myservo1.attach(servoPin);
  digitalWrite(servoPowerPin, LOW); //Since Active Low

  //Initialize Center position
  if(90 < myservo1.read()){
    for (int tempPos = myservo1.read(); 90 <= tempPos; tempPos--){
       myservo1.write(tempPos);
       delay(40);}}   //for,if-initialize
  else{
    for (int tempPos = myservo1.read(); 90 >= tempPos; tempPos++){
       myservo1.write(tempPos);
       delay(40);}}   //for,else-initialize

  //Check within range
  if (delta <= 90 && delta >= -90){
    double pos = 90+delta;

    //Move servos to pos
    if(pos < myservo1.read()){
      for (int tempPos = myservo1.read(); pos <= tempPos; tempPos--){
         myservo1.write(tempPos);
         delay(40);}}   //for,if-servomove
    else{
      for (int tempPos = myservo1.read(); pos >= tempPos; tempPos++){
         myservo1.write(tempPos);     
         delay(40);}}   //for,else-servomove

    //Recenter position
    if(90 < myservo1.read()){
      for (int tempPos = myservo1.read(); 90 <= tempPos; tempPos--){
         myservo1.write(tempPos);         
         delay(40);}}   //for,if-recenter
    else{
      for (int tempPos = myservo1.read(); 90 >= tempPos; tempPos++){
         myservo1.write(tempPos);         
         delay(40);}}}  //for,else-recenter,if-delta-range

  //Detach
  myservo1.detach();
  digitalWrite(servoPowerPin, HIGH); //Since Active Low
}
