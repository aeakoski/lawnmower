const int analogInPin = A0;  // Analog input pin that the potentiometer is attached to
const int motorLeftPin = 9; // Analog output Left motor PWM
const int motorRightPin = 10; // Analog output Right motor PWM
const int leftDirectionPin = 7;
const int rightDirectionPin = 8;
// const int breakPin = 6;

const int NUMBER_OF_LOOPS_BEFORE_APPLYING_EMERGENCY_BREAKS = 4;

int numberOfLoopsWithoutCommands = 0;

int sensorValue = 0;        // value read from the pot
int outputValue = 0;        // value output to the PWM (analog out)

unsigned char inputBytes[5];         // array to hold incoming 5 steering bytes
boolean stringComplete = false;  // whether the string is complete

int currentState[4][2] = {
  {leftDirectionPin, LOW},
  {rightDirectionPin, HIGH}, // Since motor is mirored, direction needs to be mirrored
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
    digitalWrite(currentState[1][0], !newDirectionRight); // Since motor is mirored, direction needs to be mirrored
    currentState[1][1] = newDirectionRight;
  }
  if(currentState[2][1] != newLeft){
    analogWrite(currentState[2][0], newLeft);
    currentState[2][1] = newLeft;
  }
  if(currentState[3][1] != newRight){
    analogWrite(currentState[3][0], newRight);
    currentState[3][1] = newRight;
  }
}

void setup() {
  Serial.begin(9600);
  // reserve 200 bytes for the inputBytes:
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  delay(1000);
  digitalWrite(LED_BUILTIN, HIGH);
  delay(500);
  digitalWrite(LED_BUILTIN, LOW);
  delay(500);
  digitalWrite(LED_BUILTIN, HIGH);
  delay(500);
  digitalWrite(LED_BUILTIN, LOW);
  delay(500);
  digitalWrite(LED_BUILTIN, HIGH);
  delay(500);
  digitalWrite(LED_BUILTIN, LOW);

  pinMode(leftDirectionPin, OUTPUT);
  pinMode(rightDirectionPin, OUTPUT);
  pinMode(motorLeftPin, OUTPUT);
  pinMode(motorRightPin, OUTPUT);
  
  delay(2);
  digitalWrite(leftDirectionPin, LOW);
  digitalWrite(rightDirectionPin, LOW);
  analogWrite(motorRightPin, 0);
  analogWrite(motorLeftPin, 0);
  //  digitalWrite(breakPin, LOW);
}

void serialDrive_v2(){
  //Comple first two bytes with value to the left motor
  unsigned short leftMotorSpeed = (inputBytes[0] << 8) | inputBytes[1];
  //Comple second two bytes with value to the right motor
  unsigned short rightMotorSpeed = (inputBytes[2] << 8) | inputBytes[3];
  int rightMotorDirection = LOW;
  int leftMotorDirection = LOW;
  if ((inputBytes[4] == 1) | (inputBytes[4] == 3)){
    rightMotorDirection = HIGH;
  } else {
    rightMotorDirection = LOW;
  }
  if ((inputBytes[4] == 3) | (inputBytes[4] == 2)){
    leftMotorDirection = HIGH;
  } else {
    leftMotorDirection = LOW;
  }
  Serial.println((unsigned int)inputBytes[0]);
  Serial.println((unsigned int)inputBytes[1]);
  Serial.println((unsigned int)inputBytes[2]);
  Serial.println((unsigned int)inputBytes[3]);
  Serial.println((unsigned int)inputBytes[4]);
  // Serial.println(left_motor);
  // Serial.println(right_motor);
  // Serial.println(direction);
  Serial.println("\n");
  changeState(leftMotorDirection, rightMotorDirection, leftMotorSpeed, rightMotorSpeed);
}


void wiggle() {
  int speed = 100;
  digitalWrite(leftDirectionPin, LOW);
  digitalWrite(rightDirectionPin, LOW);
  analogWrite(motorRightPin, speed);
  analogWrite(motorLeftPin, speed);
  digitalWrite(LED_BUILTIN, LOW);
  delay(10000);

  digitalWrite(leftDirectionPin, HIGH);
  digitalWrite(rightDirectionPin, HIGH);
  analogWrite(motorRightPin, speed);
  analogWrite(motorLeftPin, speed);
  digitalWrite(LED_BUILTIN, HIGH);
  delay(10000);

}

void loop() {

  //wiggle();

  if (stringComplete) {
    serialDrive_v2();
    // clear the string:
    stringComplete = false;
    numberOfLoopsWithoutCommands = 0;
    digitalWrite(LED_BUILTIN, LOW);
  } else {
    numberOfLoopsWithoutCommands++;
    delay(150);
    if (numberOfLoopsWithoutCommands > NUMBER_OF_LOOPS_BEFORE_APPLYING_EMERGENCY_BREAKS){
      digitalWrite(LED_BUILTIN, HIGH);
      changeState(LOW, LOW, 0, 0);
    }
  }
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
      Serial.write("E\n");
      return;
    }
    inputBytes[bytesRead] = inChar;
    bytesRead++;
    delay(5);
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:

  }

}
