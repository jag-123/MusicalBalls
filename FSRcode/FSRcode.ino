#include <SoftwareSerial.h>
 
int fsrAnalogPin = 0; // FSR is connected to analog 0
int irAnalogPin = 1;
int fsrReading;      // the analog reading from the FSR resistor divider
 
void setup() {
  Serial.begin(9600);
}
 
void loop() {
  float irValue = analogRead(irAnalogPin);
  
  // convert value (0-1024) to voltage,  * (5/1024)
  float voltage = irValue * 0.0048828125;

  // convert voltage to distance in cm
  float distanceObject = int(60*pow(voltage, -1.1));
  
  fsrReading = analogRead(fsrAnalogPin);
  
  Serial.print(distanceObject);
  Serial.print(" ");
  Serial.println(fsrReading);
}
