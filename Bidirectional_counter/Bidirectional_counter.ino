#include <Wire.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27, 16, 2);
int irPin1 = 3;
int irPin2 = 4;

boolean state1 = true;
boolean state2 = true;
boolean insideState = false;
boolean outsideIr = false;
boolean isPeopleExiting = false;
int ans = 1;
int i = 1;
int j = 1;
int count = 0;
boolean enter = false;
void setup() {
  lcd.begin();
  lcd.print("Visitor Counter");
  lcd.setCursor(0, 1);
  lcd.print("  ELECTROSTARS");
  lcd.backlight();
  Serial.begin(9600);
  pinMode(irPin1, INPUT);
  pinMode(irPin2, INPUT);
}
void loop() {

  while (Serial.available() > 0) {
    ans = Serial.read();
    i = 1;
    j = 1;
    state1 = true;
    state2 = true;
    if (!digitalRead(irPin1) && digitalRead(irPin2) && i == 1 && state1) {
      outsideIr = true;
      i = 2;
      enter = true;
      state1 = false;
      while (true) {
        if (!digitalRead(irPin1) && !digitalRead(irPin2) && enter) {
          while (true) {
            if (digitalRead(irPin1) && !digitalRead(irPin2) && enter) {

              Serial.println("Entering into room");
              outsideIr = true;
              i = 1;
              state2 = false;
              count += int(ans) - int('0');

              Serial.print("No of persons inside the room: ");
              Serial.println(count);
              lcd.clear();

              lcd.print("ENTERING");
              lcd.setCursor(0, 1);
              lcd.print("Total :   ");
              lcd.print(count);
              if (digitalRead(irPin1)) {
                state1 = true;
              }

              if (digitalRead(irPin2)) {
                state2 = true;
              }
              break;
            }
            if (!digitalRead(irPin2) && digitalRead(irPin1) && i == 2 && state2 && enter) {
              if (digitalRead(irPin1) && digitalRead(irPin2)) {
                Serial.println("Entering into room");
                outsideIr = true;
                i = 1;
                state2 = false;
                count += int(ans) - int('0');

                Serial.print("No of persons inside the room: ");
                Serial.println(count);
                lcd.clear();

                lcd.print("ENTERING");
                lcd.setCursor(0, 1);
                lcd.print("Total :   ");
                lcd.print(count);
                if (digitalRead(irPin1)) {
                  state1 = true;
                }

                if (digitalRead(irPin2)) {
                  state2 = true;
                }
                break;
              }
            } else if (!digitalRead(irPin1) && digitalRead(irPin2) && enter) {
              break;
            }
          }
        } else if (digitalRead(irPin1) && digitalRead(irPin2)) {
          break;
        } else if (digitalRead(irPin1)) {
          break;
        }
      }
    }

    if (digitalRead(irPin1)) {
      state1 = true;
    }
    if (digitalRead(irPin2)) {
      state2 = true;
    }

    i = 1;
    j = 1;
    state1 = true;
    state2 = true;
    if (!digitalRead(irPin2) && digitalRead(irPin1) && j == 1 && state2) {
      outsideIr = true;
      enter = false;
      j = 2;
      state2 = false;
      while (true) {
        if (!digitalRead(irPin1) && !digitalRead(irPin2) && !enter) {
          while (true) {
            if (digitalRead(irPin2) && !digitalRead(irPin1) && !enter) {
              Serial.println("Exiting from room");
              outsideIr = true;
              j = 1;
              state1 = false;

              count -= abs(int(ans)) - int('0');
              Serial.print("No of persons inside the room: ");
              Serial.println(count);
              lcd.clear();
              lcd.print("EXITING");
              lcd.setCursor(0, 1);
              lcd.print("Total :   ");
              lcd.print(count);
              if (digitalRead(irPin1)) {
                state1 = true;
              }

              if (digitalRead(irPin2)) {
                state2 = true;
              }
              break;
            }
            if (!digitalRead(irPin1) && digitalRead(irPin2) && j == 2 && state1 && !enter) {

              if (digitalRead(irPin2) && digitalRead(irPin1) && !enter) {
                Serial.println("Exiting from room");
                outsideIr = true;
                j = 1;
                state1 = false;

                count -= abs(int(ans)) - int('0');
                Serial.print("No of persons inside the room: ");
                Serial.println(count);
                lcd.clear();
                lcd.print("EXITING");
                lcd.setCursor(0, 1);
                lcd.print("Total :   ");
                lcd.print(count);
                if (digitalRead(irPin1)) {
                  state1 = true;
                }

                if (digitalRead(irPin2)) {
                  state2 = true;
                }
                break;
              }
            }
            else if(!digitalRead(irPin2) && digitalRead(irPin1) && !enter) {
              break;
            }
          }
        } else if (digitalRead(irPin1) && digitalRead(irPin2)) {
          break;
        } else if (digitalRead(irPin2)) {
          break;
        }
      }
    }


    i = 1;
    j = 1;
    if (digitalRead(irPin1)) {
      state1 = true;
    }

    if (digitalRead(irPin2)) {
      state2 = true;
    }
  }
}
