// Sweep
// by BARRAGAN <http://barraganstudio.com> 
// This example code is in the public domain.


#include <Servo.h> 
#define CLOSED 30
#define OPEN 100

Servo myservo;  // create servo object to control a servo 
                // a maximum of eight servo objects can be created 
 
int pos = 0;    // variable to store the servo position 
 
void setup() 
{ 
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object 
  Serial.begin(9600);

  Serial.println("Posn 0 to 180");
  myservo.write(CLOSED);               
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
           myservo.write(OPEN);
           delay(500); 
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
