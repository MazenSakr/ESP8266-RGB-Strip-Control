//joystick input variables
int x;
int y;
 
//servo control variables
const int servoPin1 = 2 ;
const int servoPin2 = 8 ;
int actualPos ;
const int actualPosPin = A0 ;
int deltaPos ;
 
//motor control variables
const int motor1pin1 = 9;
const int motor1pin2 = 5;
const int motor2pin1 = 10;
const int motor2pin2 = 11;
int vangle ;
 
//Variables for UDP
const byte numChars = 32;
char receivedChars[numChars];
char tempChars[numChars];
boolean newData = false;
 
void setup() {
  Serial.begin(9600);
 
  //initializing servo
  pinMode(servoPin1, OUTPUT);
  pinMode(servoPin2, OUTPUT);
  pinMode(actualPosPin, INPUT);
  
  //initializing motor control
  pinMode(motor1pin1, OUTPUT);
  pinMode(motor1pin2, OUTPUT);
  pinMode(motor2pin1, OUTPUT);
  pinMode(motor2pin2, OUTPUT);
}
 
void loop() {
  //recieving joystick input from controller
  static boolean recvInProgress = false;
  static byte ndx = 0;
  char startMarker = '<';
  char endMarker = '>';
  char rc;
  
  while (Serial.available() > 0 && newData == false) {
    rc = Serial.read();
 
    if (recvInProgress == true) {
      if (rc != endMarker) {
        receivedChars[ndx] = rc;
        ndx++;
        if (ndx >= 9) {
          ndx = 8;
        }
      }
      else {
        receivedChars[ndx] = '\0'; // terminate the string
        recvInProgress = false;
        ndx = 0;
        newData = true;
      }
    }
 
    else if (rc == startMarker) {
      recvInProgress = true;
    }
  }
  
  strcpy(tempChars, receivedChars);
  char * strtokIndx;
  strtokIndx = strtok(tempChars, ",");
  y = atoi(strtokIndx);
  strtokIndx = strtok(NULL, ",");
  x = atoi(strtokIndx);
  newData = false;
  
  //servo control code (manual control using its potentiometer)
  int vPos = map(x, -255, 255, 0, 400);
  actualPos = analogRead(actualPosPin);
  deltaPos = vPos - actualPos ;
 
  if (abs (deltaPos) < 30) {
    digitalWrite(servoPin1, LOW);
    digitalWrite(servoPin2, LOW);
  }
  else if (deltaPos > 30) {
    digitalWrite(servoPin1, HIGH);
    digitalWrite(servoPin2, LOW);
  }
  else if (deltaPos < -30) {
    digitalWrite(servoPin1, LOW);
    digitalWrite(servoPin2, HIGH);
  }
  
  //motor control code
  if (x == 0) {
    if (y >= 0) {
      analogWrite(motor1pin1, 0);
      analogWrite(motor1pin2, y);
 
      analogWrite(motor2pin1, 0);
      analogWrite(motor2pin2, y);
    }
    else {
      int s = abs (y);
      analogWrite(motor1pin1, s);
      analogWrite(motor1pin2, 0);
 
      analogWrite(motor2pin1, s);
      analogWrite(motor2pin2, 0);
    }
  }
  else if (x > 0) {
    
    //code for calculating the difference in speed between the two wheels due to turning
    vangle = map (x, 0, 255, 0, 40);
    int r = 19 * tan((90 - vangle) * 0.0175) ;
    int v2 = abs (y) ;
    int v1 = v2 * abs(r - 15) / r ;
 
    if (y >= 0) {
      analogWrite(motor1pin1, 0);
      analogWrite(motor1pin2, v2);
 
      analogWrite(motor2pin1, 0);
      analogWrite(motor2pin2, v1);
    }
    else {
      analogWrite(motor1pin1, v2);
      analogWrite(motor1pin2, 0);
 
      analogWrite(motor2pin1, v1);
      analogWrite(motor2pin2, 0);
    }
  }
  else if (x < 0) {
 
    //code for calculating the difference in speed between the two wheels due to turning
    int a = abs(x);
    vangle = map (a, 0, 255, 0, 40);
    int r = 19 * tan((90 - vangle) * 0.0175) ;
    int v2 = abs (y) ;
    int v1 = v2 * abs(r - 15) / r ;
 
    if (y >= 0) {
      analogWrite(motor1pin1, 0);
      analogWrite(motor1pin2, v1);
 
      analogWrite(motor2pin1, 0);
      analogWrite(motor2pin2, v2);
    }
    else {
      analogWrite(motor1pin1, v1);
      analogWrite(motor1pin2, 0);
 
      analogWrite(motor2pin1, v2);
      analogWrite(motor2pin2, 0);
    }
  }
}