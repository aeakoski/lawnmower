const int analogInPin = A0;  // Analog input pin that the potentiometer is attached to
const int motorLeftPin = 9; // Analog output Left motor PWM
const int motorRightPin = 10; // Analog output Right motor PWM
const int directionPin = 7;
// const int breakPin = 6;

int sensorValue = 0;        // value read from the pot
int outputValue = 0;        // value output to the PWM (analog out)

String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete

int currentState[3][2] = {
  {directionPin, LOW},
  {motorLeftPin, 0},
  {motorRightPin, 0}
  };


void changeState(int newDirection, int newLeft, int newRight){
  // To avoid discrepencis in the PWM signal, only write state change
  // to pins if there actually is a state change.
  if(currentState[0][1] != newDirection){
    digitalWrite(currentState[0][0], newDirection);
    currentState[0][1] = newDirection;
  }
  if(currentState[1][1] != newLeft){
    analogWrite(currentState[1][0], newLeft);
    currentState[1][1] = newLeft;
  }
  if(currentState[2][1] != newRight){
    analogWrite(currentState[2][0], newRight);
    currentState[2][1] = newRight;
  }
}

void setup() {
  Serial.begin(9600);
  // reserve 200 bytes for the inputString:
  inputString.reserve(200);

  pinMode(directionPin, OUTPUT);
//  pinMode(breakPin, OUTPUT);
  delay(2);
  digitalWrite(directionPin, LOW);
  analogWrite(motorRightPin, 0);
  analogWrite(motorLeftPin, 0);
//  digitalWrite(breakPin, LOW);
}

void serialDrive_v2(){
  // If we dont get any input on serial, stop the mower
  if (Serial.available() <= 0) {
    changeState(LOW, 0, 0);
    return;
  }

  char msg_len = Serial.read(); // read the incoming byte 'udlrb'
  Serial.println(msg_len); // print as an ASCII-encoded decimal

  char buffer[msg_len];
  for (int i = 0; i < msg_len; i++) {
    buffer[i] = Serial.read();
  }
  short left_motor = (buffer[0] << 8) + buffer[1];
  short right_motor = (buffer[2] << 8) + buffer[3];
  int direction = LOW;
  if (buffer[4] && 0x2){
    direction = LOW;
  } else {
    direction = HIGH;
  }
  Serial.println(left_motor);
  Serial.println(right_motor);
  Serial.println(direction);
  Serial.println("\n");
  changeState(direction, left_motor, right_motor);
}

void serialStop(){
  // If we dont get any input on serial, stop the mower
    changeState(LOW, 0, 0);
    return;
  }

void serialDrive() {
  // If we dont get any input on serial, stop the mower
  // if (Serial.available() <= 0) {
  //   changeState(LOW, 0, 0);
  //   return;
  // }
  //
  // char driveByte = Serial.read(); // read the incoming byte 'udlrb'

  //switch (driveByte) {
  Serial.println(inputString); // print as an ASCII-encoded decimal
  switch (inputString[0]) {
    case 'u':
      changeState(LOW, 1023, 1023);
      break;
    case 'd':
      changeState(HIGH, 1023, 1023);
      //digitalWrite(breakPin, LOW);
      break;
    case 'l':
      changeState(LOW, 1023, 0);
      //digitalWrite(breakPin, LOW);
      break;
    case 'x':
      changeState(HIGH, 1023, 0);
      //digitalWrite(breakPin, LOW);
      break;
    case 'r':
      changeState(LOW, 0, 1023);
      //digitalWrite(breakPin, LOW);
      break;
    case 'y':
      changeState(HIGH, 0, 1023);
      //digitalWrite(breakPin, LOW);
      break;
    case 'b':
      changeState(LOW, 0, 0);
      //digitalWrite(breakPin, LOW);
      break;
    default:
      changeState(LOW, 0, 0);
      break;
  }

}

void wiggle() {
  digitalWrite(directionPin, LOW);
  analogWrite(motorRightPin, 1023);
  analogWrite(motorLeftPin, 1023);
//  digitalWrite(breakPin, LOW);

  delay(10000);

  digitalWrite(directionPin, HIGH);
  analogWrite(motorRightPin, 1023);
  analogWrite(motorLeftPin, 1023);
//  digitalWrite(breakPin, LOW);

  delay(10000);

}

void loop() {

  //wiggle();
  if (stringComplete) {
    serialDrive();
    //serialDrive_v2();
    // clear the string:
    inputString = "";
    stringComplete = false;
  } else {
    serialStop();
  }

  delay(150);

}

void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    if (inChar == '\n') {
      stringComplete = true;
      return;
    }
    inputString += inChar;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:

  }

}
