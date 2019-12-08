#include <Arduino.h>

int ledPin = 13;
int command = command;

int photocellPin = A0;    	// Ambient light sensor sensor input
int potPin = A1;
int photocellValue = 0;		// Potentiometer sensor input
int potValue = 0;

void setup() {
	pinMode(ledPin, OUTPUT);
	digitalWrite(ledPin, HIGH);
	Serial.begin(9600);	    //Starting serial communication
}

void loop() {
	photocellValue = analogRead(photocellPin);
	Serial.println("Light " + String(photocellValue, DEC));   // send the data
	potValue = analogRead(potPin);
	Serial.println("Poten " + String(potValue, DEC));   // send the data

	while(Serial.available() > 0) {
		command = Serial.read();
		switch (command) {
			case 1:
				digitalWrite(ledPin, HIGH);
				break;
			case 2:
				digitalWrite(ledPin, LOW);
				break;
			default:
				break;
		}
	}

	delay(2000);                  // give the loop some break
}
