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
bool gameOver = false;
int level[NUM_LEDS] = {0};
int levelIndex = 0;
int playerPosition = 0;
int score = 0;

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

void setBCD(int number)
{
  // Set BCD pins to display the number
  for (int i = 0; i < 4; i++)
  {
    digitalWrite(bcd1Pins[i], bitRead(bcdValues[number % 10], i));
    digitalWrite(bcd2Pins[i], bitRead(bcdValues[int(number / 10)], i));
  }
}

void playTone(int tone)
{
  if (tone == 1)
  {
    digitalWrite(buzzerPin, HIGH);
    delay(50);
    digitalWrite(buzzerPin, LOW);
    delay(50);
    digitalWrite(buzzerPin, HIGH);
    delay(100);
    digitalWrite(buzzerPin, LOW);
  }
  else if (tone == 2)
  {
    digitalWrite(buzzerPin, HIGH);
    for (int j = 0; j < NUM_LEDS; j++)
    {
      leds[j] = CRGB::Red;
    }
    FastLED.show();
    delay(100);
    digitalWrite(buzzerPin, LOW);
    delay(100);
    digitalWrite(buzzerPin, HIGH);
    delay(200);
    digitalWrite(buzzerPin, LOW);
    for (int j = 0; j < NUM_LEDS; j++)
    {
      leds[j] = CRGB::Black;
    }
    FastLED.show();
    delay(200);
    digitalWrite(buzzerPin, HIGH);
    delay(400);
    digitalWrite(buzzerPin, LOW);
    for (int j = 0; j < NUM_LEDS; j++)
    {
      leds[j] = CRGB::Red;
    }
    FastLED.show();
    delay(400);
        for (int j = 0; j < NUM_LEDS; j++)
    {
      leds[j] = CRGB::Black;
    }
    FastLED.show();
  }
}

void generateLevel()
{
  for (int i = 0; i < NUM_LEDS; i++)
  {
    level[i] = random(2);
  }
}

void matchLedsToLevel()
{
  for (int i = 0; i < NUM_LEDS; i++)
  {
    if (level[i] == 1)
    {
      leds[i] = CRGB::Green;
    }
    else
    {
      leds[i] = CRGB::Black;
    }
  }
  FastLED.show();
}

void updatePlayer()
{
  // Move the player LED forward by one
  if (playerPosition < NUM_LEDS - 1)
  {
    leds[playerPosition] = CRGB::Black;
    playerPosition++;
    leds[playerPosition] = CRGB::Red;
  }
  else
  {
    leds[playerPosition] = CRGB::Black;
    playerPosition = 0;
    leds[playerPosition] = CRGB::Red;
  }

  // Set the LED behind the player to the level color
  if (playerPosition > 0)
  {
    if (level[playerPosition - 1] == 1)
    {
      leds[playerPosition - 1] = CRGB::Green;
    }
    else
    {
      leds[playerPosition - 1] = CRGB::Black;
    }
  }
  else
  {
    if (level[NUM_LEDS - 1] == 1)
    {
      leds[NUM_LEDS - 1] = CRGB::Green;
    }
    else
    {
      leds[NUM_LEDS - 1] = CRGB::Black;
    }
  }

  FastLED.show();
}

void didPlayerPressButtonCorrectly()
{
  if (digitalRead(buttonPin) == LOW)
  {
    if (level[playerPosition] == 1)
    {
      score++;
      playTone(1);
    }
    else
    {
      gameOver = true;
      playTone(2);
    }
  }
}

void reset()
{
  levelIndex = 0;
  playerPosition = 0;
  score = 0;
  gameOver = false;
  setBCD(0);
}

void setup()
{
  for (int i = 0; i < 4; i++)
  {
    pinMode(bcd1Pins[i], OUTPUT);
    pinMode(bcd2Pins[i], OUTPUT);
  }
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(buzzerPin, OUTPUT);
  digitalWrite(buzzerPin, LOW);
  FastLED.addLeds<WS2811, DATA_PIN, BRG>(leds, NUM_LEDS);
  randomSeed(analogRead(0));
}

void loop()
{
  if (digitalRead(buttonPin) == HIGH)
  {
    uint8_t thisSpeed = 10;
    uint8_t deltaHue = 10;
    uint8_t thisHue = beat8(thisSpeed, 255);
    fill_rainbow(leds, NUM_LEDS, thisHue, deltaHue);
    FastLED.show();
  }
  else
  {
    delay(300);
    while (!gameOver)
    {
      generateLevel();
      matchLedsToLevel();
      while ((levelIndex == score) && !gameOver)
      {
        didPlayerPressButtonCorrectly();
        updatePlayer();
        delay(map(levelIndex, 0, 30, 700, 10));
      }
      levelIndex++;
      setBCD(score);
    }
    delay(1000);
    reset();
  }
}
