// Sweep
// by BARRAGAN <http://barraganstudio.com> 
// This example code is in the public domain.


#include <Servo.h> 

#define SERVO_PIN 9
#define RUMBLE_PIN 10

#define CLOSED 30
#define OPEN 100
#define DELAY 100

#define RUMBLE_TIME 250

Servo myservo;  // create servo object to control a servo 
                // a maximum of eight servo objects can be created 
 
int pos = 0;    // variable to store the servo position 
 
void setup() 
{ 
  myservo.attach(SERVO_PIN);  // attaches the servo on pin 9 to the servo object 
  Serial.begin(9600);

  Serial.println("Posn 0 to 180");
  myservo.write(CLOSED);

  pinMode(RUMBLE_PIN, OUTPUT);   
} 
 
 
void loop() 
{ 
  /*for(pos = 0; pos < 180; pos += 1)  // goes from 0 degrees to 180 degrees 
  {                                  // in steps of 1 degree 
    myservo.write(pos);              // tell servo to go to position in variable 'pos' 
    delay(15);                       // waits 15ms for the servo to reach the position 
  } 
  delay(1000);
  for(pos = 180; pos>=1; pos-=1)     // goes from 180 degrees to 0 degrees 
  {                                
    myservo.write(pos);              // tell servo to go to position in variable 'pos' 
    delay(15);                       // waits 15ms for the servo to reach the position 
  }
  delay(1000); 
  */
  if (Serial.available())
  {
     int pos = Serial.parseInt();
     Serial.print("read ");
     Serial.println(pos);
     if ( 1 == pos )
     {
           motorOn( RUMBLE_TIME );
           myservo.write(OPEN);
           delay(DELAY); 
           myservo.write(CLOSED);               
               
     }
     
     if (pos > 1 && pos <= 180)
     {
        myservo.write(pos);
        Serial.print("Setting to ");
        Serial.println(pos);

     }
     
  }   
  
} 

void motorOn(int onTime){
  //int onTime = 2000;  //the number of milliseconds for the motor to turn on for
  //int offTime = 2000; //the number of milliseconds for the motor to turn off for
  
  digitalWrite(RUMBLE_PIN, HIGH); // turns the motor On
  delay(onTime);                // waits for onTime milliseconds
  digitalWrite(RUMBLE_PIN, LOW);  // turns the motor Off
  //delay(offTime);               // waits for offTime milliseconds
}

void motorOnThenOff(){
  int onTime = 2000;  //the number of milliseconds for the motor to turn on for
  int offTime = 2000; //the number of milliseconds for the motor to turn off for
  
  digitalWrite(RUMBLE_PIN, HIGH); // turns the motor On
  delay(onTime);                // waits for onTime milliseconds
  digitalWrite(RUMBLE_PIN, LOW);  // turns the motor Off
  delay(offTime);               // waits for offTime milliseconds
}

/*
 * motorOnThenOffWithSpeed() - turns motor on then off but uses speed values as well 
 * (notice this code is identical to the code we used for
 * the blinking LED)
 */
void motorOnThenOffWithSpeed(){
  
  int onSpeed = 200;  // a number between 0 (stopped) and 255 (full speed) 
  int onTime = 2500;  //the number of milliseconds for the motor to turn on for
  
  int offSpeed = 50;  // a number between 0 (stopped) and 255 (full speed) 
  int offTime = 1000; //the number of milliseconds for the motor to turn off for
  
  analogWrite(RUMBLE_PIN, onSpeed);   // turns the motor On
  delay(onTime);                    // waits for onTime milliseconds
  analogWrite(RUMBLE_PIN, offSpeed);  // turns the motor Off
  delay(offTime);                   // waits for offTime milliseconds
}

/*
 * motorAcceleration() - accelerates the motor to full speed then
 * back down to zero
*/
void motorAcceleration(){
  int delayTime = 50; //milliseconds between each speed step
  
  //Accelerates the motor
  for(int i = 0; i < 256; i++){ //goes through each speed from 0 to 255
    analogWrite(RUMBLE_PIN, i);   //sets the new speed
    delay(delayTime);           // waits for delayTime milliseconds
  }
  
  //Decelerates the motor
  for(int i = 255; i >= 0; i--){ //goes through each speed from 255 to 0
    analogWrite(RUMBLE_PIN, i);   //sets the new speed
    delay(delayTime);           // waits for delayTime milliseconds
  }
}

