#! /usr/bin/env python
import wiringpi2 as wiringpi
import time
import readchar


# Define driving pins
FORWARD_DRIVE = 209 # GPIO PIN 16
BACKWARD_DRIVE = 19 # GPIO PIN 18
PISTON_UP = 31 # GPIO PIN 22
PISTON_DOWN = 25 # GPIO PIN 24

#FORWARD_DRIVE = 18 # GPIO PIN 16
#BACKWARD_DRIVE = 18 # GPIO PIN 18
#PISTON_UP = 18 # GPIO PIN 22
#PISTON_DOWN = 18 # GPIO PIN 24


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
	print "Stopping everything..."
        wiringpi.digitalWrite(FORWARD_DRIVE, LOW)
        wiringpi.digitalWrite(BACKWARD_DRIVE, LOW)
        wiringpi.digitalWrite(PISTON_UP, LOW)
        wiringpi.digitalWrite(PISTON_DOWN, LOW)
	wiringpi.delay(100)
	print "Done stopping"

    def drive_forward(self):
        self.stop_all()
        wiringpi.digitalWrite(FORWARD_DRIVE, HIGH)
	print "Driving Forward..."

    def drive_backward(self):
        self.stop_all()
        wiringpi.digitalWrite(BACKWARD_DRIVE, HIGH)
	print "Driving Backward..."

    def turn_left(self):
	print "Raising piston then turning left..."
        self.stop_all()
        wiringpi.digitalWrite(PISTON_UP, HIGH)
        wiringpi.delay(4000)
        wiringpi.digitalWrite(PISTON_UP, LOW)
        wiringpi.digitalWrite(FORWARD_DRIVE, HIGH)
	print "Done"

    def turn_right(self):
	print "Raising piston then turning right..."
        self.stop_all()
        wiringpi.digitalWrite(PISTON_UP, HIGH)
        wiringpi.delay(4000)
        wiringpi.digitalWrite(PISTON_UP, LOW)
        wiringpi.digitalWrite(BACKWARD_DRIVE, HIGH)
	print "Done"

    def piston_out(self):
	self.stop_all()
	print "Piston going up for 2 sec..."	
	wiringpi.digitalWrite(PISTON_UP, HIGH)
	wiringpi.delay(4000)
	wiringpi.digitalWrite(PISTON_UP, LOW)
	print "Done"

    def piston_in(self):
        self.stop_all()
	print "Piston coming down for 2 sec..."
        wiringpi.digitalWrite(PISTON_DOWN, HIGH)
        wiringpi.delay(4000)
        wiringpi.digitalWrite(PISTON_DOWN, LOW)
	print "Done"

