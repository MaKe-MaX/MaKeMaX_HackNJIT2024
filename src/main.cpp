#include <Arduino.h>
#include <SPI.h>
#define SW 8
#define joy_x A0
#define joy_y A1
#define ultrasonic 5
#include <Adafruit_CCS811.h>

Adafruit_CCS811 AQsensor;

unsigned long lastAQRead = 0UL;

void setup()
{
  Serial.begin(19200);
  pinMode(joy_x, INPUT);
  pinMode(joy_y, INPUT);
  pinMode(SW, INPUT);
}

void loop()
{
  float joy_rx = analogRead(joy_x);
  float joy_ry = analogRead(joy_y);

  joy_rx = map(joy_rx, 1, 1024, 500, -500);
  joy_ry = map(joy_ry, 1, 1024, -500, 500);

  Serial.print("X: " + String(joy_rx) + ',');
  Serial.print("Y: " + String(joy_ry) + ',');
  Serial.println(!digitalRead(SW));

  //Serial.print("\t CO2: " + String(AQsensor.geteCO2()) + 
  //"ppm, TVOC: "+ String(AQsensor.getTVOC()) + "ppb.\n");
}