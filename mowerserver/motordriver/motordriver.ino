const int analogInPin = A0;  // Analog input pin that the potentiometer is attached to
const int motorLeftPin = 9; // Analog output Left motor PWM
const int motorRightPin = 10; // Analog output Right motor PWM
const int directionPin = 7;
//const int breakPin = 6;

int sensorValue = 0;        // value read from the pot
int outputValue = 0;        // value output to the PWM (analog out)

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
void oldDriver(){
  sensorValue = analogRead(analogInPin);
  // map it to the range of the analog out:
  if(sensorValue < 700){
      sensorValue = 0;
  }
  outputValue = map(sensorValue, 0, 1023, 0, 255);
  // change the analog out value:
  analogWrite(motorRightPin, outputValue);
  analogWrite(motorLeftPin, outputValue);

  // print the results to the Serial Monitor:
  Serial.print("sensor = ");
  Serial.print(sensorValue);
  Serial.print("\t output = ");
  Serial.println(outputValue);

  // wait 2 milliseconds before the next loop for the analog-to-digital
  // converter to settle after the last reading:
  delay(2);
}

void serialDrive() {
  if (Serial.available() <= 0) {
    analogWrite(motorRightPin, 0);
    analogWrite(motorLeftPin, 0);
//    digitalWrite(breakPin, LOW);
    return;
  }

  // udlrb

  char driveByte = Serial.read(); // read the incoming byte 'udlrb'
  Serial.println(driveByte); // print as an ASCII-encoded decimal

  switch (driveByte) {
    case 'u':
      digitalWrite(directionPin, LOW);
      analogWrite(motorRightPin, 1023);
      analogWrite(motorLeftPin, 1023);
//      digitalWrite(breakPin, LOW);
      break;
    case 'd':
      digitalWrite(directionPin, HIGH);
      analogWrite(motorRightPin, 1023);
      analogWrite(motorLeftPin, 1023);
//      digitalWrite(breakPin, LOW);
      break;
    case 'l':
      digitalWrite(directionPin, LOW);
      analogWrite(motorRightPin, 0);
      analogWrite(motorLeftPin, 1023);
//      digitalWrite(breakPin, LOW);
      break;
    case 'x':
      digitalWrite(directionPin, HIGH);
      analogWrite(motorRightPin, 0);
      analogWrite(motorLeftPin, 1023);
//      digitalWrite(breakPin, LOW);
      break;
    case 'r':
      digitalWrite(directionPin, LOW);
      analogWrite(motorRightPin, 1023);
      analogWrite(motorLeftPin, 0);
//      digitalWrite(breakPin, LOW);
      break;
    case 'y':
      digitalWrite(directionPin, HIGH);
      analogWrite(motorRightPin, 1023);
      analogWrite(motorLeftPin, 0);
//      digitalWrite(breakPin, LOW);
      break;
    case 'b':
      digitalWrite(directionPin, LOW);
      analogWrite(motorRightPin, 0);
      analogWrite(motorLeftPin, 0);
//      digitalWrite(breakPin, LOW);
      break;
    default:
      analogWrite(motorRightPin, 0);
      analogWrite(motorLeftPin, 0);
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
