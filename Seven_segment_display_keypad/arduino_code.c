/***************************************************************
Author :Mazen Sakr
Descritpion :This project contains the code to output 
the recieved input from a keypad to one of two seven segment displays
***************************************************************/
//----------------------definitions section-----------------------------
//First 7-Segment offset
#define SSegment1Offset 6

//Second 7-Segment offset
#define SSegment2Offset 2

//Keypad offset
#define KeypadOffset 10

//Debug mode Defintion
#define DEBUGMODE

//----------------------------------------------------------------------------

//-------------------globals section---------------------------------
bool SSegment1[4] = {0,0,0,0};
bool SSegment2[4] = {0,0,0,0};
bool Keypad[4] = {0,0,0,0};
void readKeypad(bool *keypad);
void decodeInput(bool *keypad, bool *SSegment1, bool *SSegment2);
void printSSegment1(bool *SSegment1);
void printSSegment2(bool *SSegment2);
//----------------------------------------------------------------------------

//-----------------setup section----------------------------------------------
void setup() {
//First 7-Segement setup
for(int counter = 0; counter < 4; counter++){
    pinMode(counter + SSegment1Offset,OUTPUT);
  }

//Second 7-Segement setup
for(int counter = 0; counter < 4; counter++){
    pinMode(counter + SSegment2Offset,OUTPUT);
  }

//Keypad setup
for(int counter = 0; counter < 4; counter++){
    pinMode(counter + KeypadOffset,OUTPUT);
  }
pinMode(A0,INPUT_PULLUP);
pinMode(A1,INPUT_PULLUP);
pinMode(A2,INPUT_PULLUP);
pinMode(A3,INPUT_PULLUP);

//Serial initalization for debugging
#ifdef DEBUGMODE 
  Serial.begin(9600);
#endif

}
//------------------------------------------------------------------------------

//---------------------------loop section---------------------------------------
void loop() {
  readKeypad(Keypad);
  decodeInput(Keypad,SSegment1,SSegment2);
  printSSegment1(SSegment1);
  printSSegment2(SSegment2);
  #ifdef DEBUGMODE 
    for(int counter = 0; counter < 4; counter++){
      Serial.print(Keypad[counter]);
    }
    Serial.println("");

  #endif
}

//-------------------------------------------------------------------------------

//----------------------------sub-program section---------------------------------
void readKeypad(bool *keypad){
  for(int counter = 0; counter < 4; counter++){
      Keypad[counter] = digitalRead(counter + KeypadOffset);
    }
}

void decodeInput(bool *keypad, bool *SSegment1, bool *SSegment2){
  static char activeSSegment = 0;
  if (keypad[0] == 1 && keypad[1] == 0 && keypad[2] == 1 && keypad[3] == 0){
    activeSSegment  = !activeSSegment;
    } else if (0 == activeSSegment){
        for(int counter = 0; counter < 4; counter++){
          SSegment1[counter] = keypad[counter];
        }
    } else if (1 == activeSSegment){
        for(int counter = 0; counter < 4; counter++){
          SSegment2[counter] = keypad[counter];
        }
    }
}
void printSSegment1(bool *SSegment1){
    for(int counter = 0; counter < 4; counter++){
      digitalWrite(counter + SSegment1Offset,SSegment1[counter]);
  }
}
void printSSegment2(bool *SSegment2){
    for(int counter = 0; counter < 4; counter++){
      digitalWrite(counter + SSegment2Offset,SSegment2[counter]);
  }
}
