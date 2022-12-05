const int analogInPin = A0;  // Analog input pin that the potentiometer is attached to
const int motorLeftPin = 9; // Analog output Left motor PWM
const int motorRightPin = 10; // Analog output Right motor PWM
const int leftDirectionPin = 7;
const int rightDirectionPin = 8;
// const int breakPin = 6;

const int NUMBER_OF_LOOPS_BEFORE_APPLYING_EMERGENCY_BREAKS = 3;

int numberOfLoopsWithoutCommands = 0;

int sensorValue = 0;        // value read from the pot
int outputValue = 0;        // value output to the PWM (analog out)

unsigned char inputBytes[5];         // array to hold incoming 5 steering bytes
boolean stringComplete = false;  // whether the string is complete

int currentState[4][2] = {
  {leftDirectionPin, LOW},
  {rightDirectionPin, LOW},
  {motorLeftPin, 0},
  {motorRightPin, 0}
  };


void changeState(int newDirectionLeft, int newDirectionRight, int newLeft, int newRight){
  // To avoid discrepencis in the PWM signal, only write state change
  // to pins if there actually is a state change.
  if(currentState[0][1] != newDirectionLeft){
    digitalWrite(currentState[0][0], newDirectionLeft);
    currentState[0][1] = newDirectionLeft;
  }
  if(currentState[1][1] != newDirectionRight){
    analogWrite(currentState[1][0], newDirectionRight);
    currentState[1][1] = newDirectionRight;
  }
  if(currentState[2][1] != newLeft){
    analogWrite(currentState[2][0], newLeft);
    currentState[2][1] = newLeft;
  }
  if(currentState[3][1] != newRight){
    analogWrite(currentState[2][0], newRight);
    currentState[3][1] = newRight;
  }
}

void setup() {
  Serial.begin(9600);
  // reserve 200 bytes for the inputBytes:

  pinMode(leftDirectionPin, OUTPUT);
  pinMode(rightDirectionPin, OUTPUT);
  //  pinMode(breakPin, OUTPUT);
  delay(2);
  digitalWrite(leftDirectionPin, LOW);
  digitalWrite(rightDirectionPin, LOW);
  analogWrite(motorRightPin, 0);
  analogWrite(motorLeftPin, 0);
  //  digitalWrite(breakPin, LOW);
}

void serialDrive_v2(){
  //Comple first two bytes with value to the left motor
  unsigned short leftMotorSpeed = (inputBytes[0] << 8) + inputBytes[1];
  //Comple second two bytes with value to the right motor
  unsigned short rightMotorSpeed = (inputBytes[2] << 8) + inputBytes[3];
  int rightMotorDirection = LOW;
  int leftMotorDirection = LOW;
  if (inputBytes[4] && 0x1){
    rightMotorDirection = HIGH;
  } else {
    rightMotorDirection = LOW;
  }
  if (inputBytes[4] && 0x10){
    leftMotorDirection = HIGH;
  } else {
    leftMotorDirection = LOW;
  }
  // Serial.println((unsigned int)inputBytes[0]);
  // Serial.println((unsigned int)inputBytes[1]);
  // Serial.println(left_motor);
  // Serial.println(right_motor);
  // Serial.println(direction);
  // Serial.println("\n");
  changeState(leftMotorDirection, rightMotorDirection, leftMotorSpeed, rightMotorSpeed);
}


void wiggle() {
  digitalWrite(leftDirectionPin, LOW);
  digitalWrite(rightDirectionPin, LOW);
  analogWrite(motorRightPin, 1023);
  analogWrite(motorLeftPin, 1023);
//  digitalWrite(breakPin, LOW);

  delay(10000);

  digitalWrite(leftDirectionPin, HIGH);
  digitalWrite(rightDirectionPin, HIGH);
  analogWrite(motorRightPin, 1023);
  analogWrite(motorLeftPin, 1023);
//  digitalWrite(breakPin, LOW);
  delay(10000);

}

void loop() {

  //wiggle();
  if (stringComplete) {
    serialDrive_v2();
    // clear the string:
    stringComplete = false;
    numberOfLoopsWithoutCommands = 0;
  } else {
    numberOfLoopsWithoutCommands++;
    if (numberOfLoopsWithoutCommands > NUMBER_OF_LOOPS_BEFORE_APPLYING_EMERGENCY_BREAKS){
      changeState(LOW, LOW, 0, 0);
    }
  }
  delay(150);
}

char bytesRead = 0;
void serialEvent() {
  while (Serial.available()) {
    unsigned char inChar = Serial.read();
    if (inChar == '\n' && bytesRead == 5) {
      stringComplete = true;
      bytesRead = 0;
      Serial.write("Y\n");
      return;
    } else if (bytesRead == 5){
      bytesRead = 0;
      Serial.write("N\n");
      return;
    } else if (inChar == '\n'){
      bytesRead = 0;
      Serial.write("N\n");
      return;
    }
    inputBytes[bytesRead] = inChar;
    bytesRead++;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:

  }

}
