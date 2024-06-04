
//Defines pins
#define pinL A2
#define pinM A1
#define pinR A0

#define pinLeftMotor 8
#define pinLeftSpeed 5

#define pinRightMotor 7
#define pinRightSpeed 6

//Set vehicle speed
const int speed = 65;

const int lcv = 61; //Left infrared correction value
const int mcv = 150; //Middel infrared correction value
const int rcv = 46; //right infrared correction value

int thrs = 330; //Threshold infrared value for line detection

//Infrared values
int LValue = 0, MValue = 0, RValue = 0;

void FollowLine(){
  //Set the maximum speed
  analogWrite(pinLeftSpeed, speed);
  analogWrite(pinRightSpeed, speed);

  //Drive straight 
  if(LValue <= thrs && RValue >= thrs){
    digitalWrite(pinLeftMotor, HIGH);
    digitalWrite(pinRightMotor, HIGH);
  }

  //Turn Left
  else if(LValue >= thrs){
    digitalWrite(pinLeftMotor, LOW);
    digitalWrite(pinRightMotor, HIGH);
  }

  //Turn Right
  else if(RValue <= thrs){
    digitalWrite(pinLeftMotor, HIGH);
    digitalWrite(pinRightMotor, LOW);
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
  digitalWrite(3, HIGH);
}

void loop() {
  //Read values from the analog pins
  LValue = analogRead(pinL);
  LValue = LValue - lcv;
  MValue = analogRead(pinM);
  MValue = MValue - mcv;
  RValue = analogRead(pinR);
  RValue = RValue - rcv;

  //FollowLine();
}





































































