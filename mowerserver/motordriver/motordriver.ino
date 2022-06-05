const int analogInPin = A0;  // Analog input pin that the potentiometer is attached to
const int motorLeftPin = 9; // Analog output Left motor PWM
const int motorRightPin = 10; // Analog output Right motor PWM
const int directionPin = 7;
// const int breakPin = 6;

const int NUMBER_OF_LOOPS_BEFORE_APPLYING_EMERGENCY_BREAKS = 3;

int numberOfLoopsWithoutCommands = 0;

int sensorValue = 0;        // value read from the pot
int outputValue = 0;        // value output to the PWM (analog out)

unsigned char inputBytes[5];         // array to hold incoming 5 steering bytes
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
  // reserve 200 bytes for the inputBytes:

  pinMode(directionPin, OUTPUT);
  //  pinMode(breakPin, OUTPUT);
  delay(2);
  digitalWrite(directionPin, LOW);
  analogWrite(motorRightPin, 0);
  analogWrite(motorLeftPin, 0);
  //  digitalWrite(breakPin, LOW);
}

void serialDrive_v2(){
  //Comple first two bytes with value to the left motor
  unsigned short left_motor = (inputBytes[0] << 8) + inputBytes[1];
  //Comple second two bytes with value to the right motor
  unsigned short right_motor = (inputBytes[2] << 8) + inputBytes[3];
  int direction = LOW;
  if (inputBytes[4] && 0x1){
    direction = HIGH;
  } else {
    direction = LOW;
  }
  Serial.println((unsigned int)inputBytes[0]);
  Serial.println((unsigned int)inputBytes[1]);
  Serial.println(left_motor);
  Serial.println(right_motor);
  Serial.println(direction);
  Serial.println("\n");
  changeState(direction, left_motor, right_motor);
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
    serialDrive_v2();
    // clear the string:
    stringComplete = false;
    numberOfLoopsWithoutCommands = 0;
  } else {
    numberOfLoopsWithoutCommands++;
    if (numberOfLoopsWithoutCommands > NUMBER_OF_LOOPS_BEFORE_APPLYING_EMERGENCY_BREAKS){
      changeState(LOW, 0, 0);
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
      Serial.write("ok\n");
      return;
    } else if (bytesRead == 5){
      bytesRead = 0;
      Serial.write("no\n");
      return;
    } else if (inChar == '\n'){
      bytesRead = 0;
      Serial.write("no\n");
      return;
    }
    inputBytes[bytesRead] = inChar;
    bytesRead++;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:

  }

}
