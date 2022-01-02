const int analogInPin = A0;  // Analog input pin that the potentiometer is attached to
const int motorLeftPin = 9; // Analog output Left motor PWM
const int motorRightPin = 10; // Analog output Right motor PWM
const int directionPin = 7;
// const int breakPin = 6;

int sensorValue = 0;        // value read from the pot
int outputValue = 0;        // value output to the PWM (analog out)

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
  pinMode(directionPin, OUTPUT);
//  pinMode(breakPin, OUTPUT);
  delay(2);
  digitalWrite(directionPin, LOW);
  analogWrite(motorRightPin, 0);
  analogWrite(motorLeftPin, 0);
//  digitalWrite(breakPin, LOW);
}

void serialDrive() {
  // If we dont get any input on serial, stop the mower
  if (Serial.available() <= 0) {
    changeState(LOW, 0, 0);
    return;
  }

  char driveByte = Serial.read(); // read the incoming byte 'udlrb'
  Serial.println(driveByte); // print as an ASCII-encoded decimal

  switch (driveByte) {
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

  delay(100);
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

  serialDrive();
  //wiggle();
}
