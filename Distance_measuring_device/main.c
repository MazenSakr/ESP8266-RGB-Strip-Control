#include <LiquidCrystal.h>

LiquidCrystal lcd(12, 11, 5, 4, 3, 2); // Interface pins of the LCD
const int trigPin = 8;
const int echoPin = 9;
long duration;
int distanceCm;

void setup() {
  lcd.begin(16, 2);
  lcd.setCursor(0, 0);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(20);
  digitalWrite(trigPin, LOW);
  delayMicroseconds(20);
  duration = pulseIn(echoPin, HIGH);
  distanceCm = duration * 0.034 / 2;
  lcd.setCursor(0, 1);
  lcd.print(distanceCm);
  lcd.print("cm");
  delay(100);
}