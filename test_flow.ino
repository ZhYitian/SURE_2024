// install two libraries
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// Initialize the PWM driver. By default, it uses I2C address 0x40.
Adafruit_PWMServoDrwiriver pwm = Adafruit_PWMServoDriver();

// Define the PWM channels for the servo motors
#define SERVO1_PWM 0 // PV
#define SERVO2_PWM 1 // CR1
#define SERVO3_PWM 2 // CR2

// Flow sensor pin
const int flowSensorPin = 2;
volatile int pulseCount = 0;


/*
For the YS-F401 flow sensor 5880 pulses = 1L,
The hall-effect flow sensor has the constant that it has 4.5 pulses/sec.
*/
const float calibrationFactor = 98;

float flowRate;
unsigned int flowMilliLitres;
unsigned long totalMilliLitres;
unsigned long oldTime;

void pulseCounter() {
  pulseCount++;
}

void setup() {
  Serial.begin(9600);
  pwm.begin();
  pwm.setPWMFreq(60);  

  pinMode(flowSensorPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(flowSensorPin), pulseCounter, FALLING);

  pulseCount = 0;
  flowRate = 0.0;
  flowMilliLitres = 0;
  totalMilliLitres = 0;
  oldTime = millis();

  Serial.println("Setup complete");
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    
    if (command.startsWith("SERVO")) {
      int servoIndex = command.substring(6, 7).toInt();
      int percent = command.substring(8).toInt();
      setServoPosition(servoIndex, percent);
      Serial.println("Servo " + String(servoIndex) + " set to " + String(percent) + "%");
    }
    
    if (command.startsWith("FLOW")) {
      measureFlowRate();
    }
  }
}

void setServoPosition(int servoIndex, int percent) {
  int pulseLength = 0;
  switch (servoIndex) {
    case 0:
      pulseLength = map(percent, 0, 100, 370, 520); // for PV: 370 count equals an angle of 0 and a 520 count is an angle of 90
      break;
    case 1:
      pulseLength = map(percent, 0, 100, 150, 290); // for CR1: 150 count equals an angle of 0 and a 290 count is an angle of 90
      break;
    case 2:
      pulseLength = map(percent, 0, 100, 260, 410); // for CR2: 260 count equals an angle of 0 and a 410 count is an angle of 90
      break;
  }
  pwm.setPWM(servoIndex, 0, pulseLength);
}

void measureFlowRate() {
  detachInterrupt(digitalPinToInterrupt(flowSensorPin));
  flowRate = ((1000.0 / (millis() - oldTime)) * pulseCount) / calibrationFactor;
  oldTime = millis();
  
  flowMilliLitres = (flowRate / 60) * 1000;
  totalMilliLitres += flowMilliLitres;

  Serial.println("FLOW " + String(pulseCount));
  pulseCount = 0;
  attachInterrupt(digitalPinToInterrupt(flowSensorPin), pulseCounter, FALLING);
}
