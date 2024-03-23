#include "Arduino.h"
#include "FastLED.h"
#define NUM_LEDS 34
#define DATA_PIN 12

CRGB leds[NUM_LEDS];

// Pin definitions for BCD control
const int bcd1Pins[] = {2, 4, 5, 6};
const int bcd2Pins[] = {7, 8, 9, 10};
const int buzzerPin = 11;
const int buttonPin = 13;

// BCD values for numbers 0 to 9
const byte bcdValues[] = {
    B0000, // 0
    B0001, // 1
    B0010, // 2
    B0011, // 3
    B0100, // 4
    B0101, // 5
    B0110, // 6
    B0111, // 7
    B1000, // 8
    B1001  // 9
};

void setup()
{
  // Set BCD control pins as outputs
  for (int i = 0; i < 4; i++)
  {
    pinMode(bcd1Pins[i], OUTPUT);
    pinMode(bcd2Pins[i], OUTPUT);
  }
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(buzzerPin, OUTPUT);
  digitalWrite(buzzerPin, LOW);
  FastLED.addLeds<WS2811, DATA_PIN, BRG>(leds, NUM_LEDS);
}

void loop()
{
  for (int dot = 0; dot < NUM_LEDS; dot++)
  {
    leds[dot] = CRGB::Blue;
    leds[dot+1] = CRGB::Green;
    leds[dot+2] = CRGB::Red;
    FastLED.show();
    // clear this led for the next time around the loop
    leds[dot] = CRGB::Black;
    leds[dot+1] = CRGB::Black;
    leds[dot+2] = CRGB::Black;
    delay(70);
  }
  for (int counter = 0; counter <= 9; counter++)
  {
    for (int j = 0; j < 4; j++)
    {
      digitalWrite(bcd1Pins[j], LOW);
      digitalWrite(bcd2Pins[j], bitRead(counter, j));
      
    }
    for (int i = 0; i <= 9; i++)
    {
      // Set BCD control pins based on BCD value
      for (int j = 0; j < 4; j++)
      {
        digitalWrite(bcd1Pins[j], bitRead(i, j));
        if(digitalRead(buttonPin) == LOW){
        break;
      }
      }
      if(digitalRead(buttonPin) == LOW){
        break;
      }
      delay(1000); // Delay for 1 second
    }
  }
  digitalWrite(11, HIGH);
  delay(100);
  digitalWrite(11, LOW);
}