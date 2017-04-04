#! /usr/bin/env python
import wiringpi2 as wiringpi
import time
import readchar


# Define driving pins
FORWARD_DRIVE = 19 # GPIO PIN 18
BACKWARD_DRIVE = 28 # GPIO PIN 20
PISTON_UP = 31 # GPIO PIN 22
PISTON_DOWN = 25 # GPIO PIN 24

# Define global constants
OUTPUT = 1
INPUT = 0
HIGH = 1
LOW = 0


class Drivetrain(object):
    def __init__(self):
        wiringpi.wiringPiSetupGpio()

        # Set the pin mode for all pins to OUTPUT
        wiringpi.pinMode(FORWARD_DRIVE, OUTPUT)
        wiringpi.pinMode(BACKWARD_DRIVE, OUTPUT)
        wiringpi.pinMode(PISTON_UP, OUTPUT)
        wiringpi.pinMode(PISTON_DOWN, OUTPUT)

	# For safety, make sure all pins are set to 0
	self.stop_all()


    def stop_all(self):
        wiringpi.digitalWrite(FORWARD_DRIVE, LOW)
        wiringpi.digitalWrite(BACKWARD_DRIVE, LOW)
        wiringpi.digitalWrite(PISTON_UP, LOW)
        wiringpi.digitalWrite(PISTON_DOWN, LOW)

    def drive_forward(self):
        self.stop_all()
        wiringpi.digitalWrite(FORWARD_DRIVE, HIGH)

    def drive_backward(self):
        self.stop_all()
        wiringpi.digitalWrite(BACKWARD_DRIVE, HIGH)

    def turn_left(self):
        self.stop_all()
        wiringpi.digitalWrite(PISTON_UP, HIGH)
        wiringpi.delay(2000)
        wiringpi.digitalWrite(PISTON_UP, LOW)
        wiringpi.digitalWrite(FORWARD_DRIVE, HIGH)

    def turn_right(self):
        self.stop_all()
        wiringpi.digitalWrite(PISTON_UP, HIGH)
        wiringpi.delay(2000)
        wiringpi.digitalWrite(PISTON_UP, LOW)
        wiringpi.digitalWrite(BACKWARD_DRIVE, HIGH)

    def reset_piston(self):
        self.stop_all()
        wiringpi.digitalWrite(PISTON_DOWN, HIGH)
        wiringpi.delay(2000)
        wiringpi.digitalWrite(PISTON_DOWN, LOW)

