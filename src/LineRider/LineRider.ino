 
//Defines pins
#define pinL A2
#define pinM A1
#define pinR A0

#define pinLeftMotor 8
#define pinLeftSpeed 5

#define pinRightMotor 7
#define pinRightSpeed 6

//Set vehicle speed
const int speed = 120;

//Infrared values
int LValue = 0, MValue = 0, RValue = 0;

void FollowLine(){
  //Set the maximum speed
  analogWrite(pinLeftSpeed, speed)
  analogWrite(pinRightSpeed, speed)

  //Drive straight 
  if(LValue >= 455 && RValue >= 455){
    digitalWrite(pinLeftMotor, HIGH)
    digitalWrite(pinRightMotor, HIGH)
  }

  //Turn Left
  else if(Right <= 455 && Left >= 455){
    digitalWrite(pinLeftMotor, LOW)
    digitalWrite(pinRightMotor, HIGH)
  }

  //Turn Right
  else if(Right <= 455 && Left >= 455){
    digitalWrite(pinLeftMotor, HIGH)
    digitalWrite(pinRightMotor, LOW)
  }
}

void setup() {
  //Set pinMode
  pinMode(pinL, INPUT);
  pinMode(pinM, INPUT);
  pinMode(pinR, INPUT);
  pinMode(pinLeftMotor, OUTPUT);
  pinMode(pinLeftSpeed, OUTPUT);
  pinMode(pinRightMotor, OUTPUT);
  pinMode(pinRightSpeed, OUTPUT);

  Serial.begin(9600);
  delay(1000);
  Serial.println("Start following line");
  digitalWrite(3, HIGH)
}

void loop() {
  //Read values from the analog pins
  LValue = analogRead(pinL);
  MValue = analogRead(pinM);
  RValue = analogRead(pinR);

  FollowLine();
}
