#include <Arduino.h>
#include <SPI.h>
#include <stdio.h>
#define SW 8
#define joy_x A0
#define joy_y A1
#define echo 6
#define trig 5
#include <Adafruit_CCS811.h>

//Adafruit_CCS811 AQsensor;

//unsigned long lastAQRead = 0UL;

void setup()
{
  Serial.begin(19200);
  pinMode(joy_x, INPUT);
  pinMode(joy_y, INPUT);
  pinMode(SW, INPUT);
  pinMode(trig, OUTPUT);
  pinMode(echo, INPUT);

  //AQsensor.begin();

}

void loop()
{
  float joy_rx = analogRead(joy_x);
  float joy_ry = analogRead(joy_y);
  float distance;

  joy_rx = map(joy_rx, 1, 1024, -500, 500);
  joy_ry = map(joy_ry, 1, 1024, -500, 500);
  if(joy_rx < 1 && joy_rx >= -21)
    joy_rx = 0;
  if(joy_ry <= 20.0 && joy_ry > -5)
    joy_ry = 0;

  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);

  long duration = pulseIn(echo, HIGH);

  distance = (duration * 0.0346)/2;

  Serial.println(String(joy_rx) + ' ' + String(joy_ry) + ' ' + String(!digitalRead(SW)) + ' ' + String(distance));

  //Serial.print("\t CO2: " + String(AQsensor.geteCO2()) + 
  //"ppm, TVOC: "+ String(AQsensor.getTVOC()) + "ppb.\n");
}