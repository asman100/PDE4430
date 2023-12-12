#include <Wire.h>
#include <ros.h>
#include <std_msgs/String.h>
#include <std_msgs/Float32.h>
#include <std_msgs/Int16.h>
#include "std_msgs/Float32MultiArray.h"
const int trigPin = 9;
const int echoPin = 10;



int speed = 0;


ros::NodeHandle nh;
std_msgs::Float32 distance;
std_msgs::Float32MultiArray rpm;

ros::Publisher pub_distance("distance", &distance);
ros::Publisher pub_rpm1("rpm1", &rpm);


unsigned long millisBefore;
volatile float holes;
volatile float holes2;
long duration;


void motor1(const std_msgs::Int16& cmd_msg) {
  speed = cmd_msg.data;
  analogWrite(6,speed );
}
ros::Subscriber<std_msgs::Int16> sub("motor", motor1);

void ultrasonic() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance.data = duration * 0.034 / 2;
  pub_distance.publish(&distance);
  delay(500);
}

void count() {
  holes++;
}
void count2() {
  holes2++;
}

void setup() {

  nh.initNode();
  nh.advertise(pub_distance);
  nh.advertise(pub_rpm1);

  nh.subscribe(sub);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  pinMode(6, OUTPUT);


  pinMode(2, INPUT);
  pinMode(3, INPUT);

  attachInterrupt(digitalPinToInterrupt(2), count, FALLING);
  attachInterrupt(digitalPinToInterrupt(3), count2, FALLING);
}

void loop() {
  ultrasonic();
  
  if (millis() - millisBefore > 1000) {
    float data[2];


    data[0] = (holes / 20.0) * 60;
    holes = 0;
    data[1] = (holes2 / 20.0) * 60;
    rpm.data = data;
    rpm.data_length = 2;
    holes2 = 0;
    millisBefore = millis();

    pub_rpm1.publish(&rpm);
  }

  delay(100);
  nh.spinOnce();
}
