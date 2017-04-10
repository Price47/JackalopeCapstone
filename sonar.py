#! /usr/bin/env python
import wiringpi2 as wiringpi
import time
import readchar

# Define main trigger and sensor echo pins
CENTER_TRIG = 18 # TRIGGER - GPIO PIN 15
CENTER_ECHO = 22 # ECHO - GPIO PIN 17
OUTPUT_ENABLED = 30 # ENABLING OF OUTPUT - GPIO PIN 19

# Define global constants
OUTPUT = 1
INPUT = 0
HIGH = 1
LOW = 0


# Define sensor object with trigger, echo, and relative positions
# Position 0 is center(kinect direction). - numbers are to left and + to the right
class Sensor(object):
    def __init__(self, trigger, echo, position):
        self.trigger = trigger
        self.echo = echo
        self.position = position
        self.baseline = 0

class Sonar_Array(object):
    sensors = []
    
    def __init__(self):
        #Initialize wiringpi interface
        wiringpi.wiringPiSetupGpio()

        # Enter all known sensors into array
        self.sensors.append(Sensor(CENTER_TRIG, CENTER_ECHO, 0))
        #sensors.append(Sensor(CENTER_TRIG, RIGHT_SENSE_ECHO, 1))
        #sensors.append(Sensor(CENTER_TRIG, LEFT_SENSE_ECHO, -1))
        wiringpi.digitalWrite(OUTPUT_ENABLED, HIGH)
        for sensor in self.sensors:
            wiringpi.pinMode(sensor.trigger, OUTPUT)
	    print 'for'

            wiringpi.pinMode(sensor.echo, INPUT)
        #wiringpi.digitalWrite(CENTER_TRIG, HIGH)
        #wiringpi.digitalWrite(CENTER_ECHO, HIGH)

    def get_distance(self, sensor):
        #wiringpi.digitalWrite(30,HIGH)
        wiringpi.digitalWrite(sensor.echo, LOW)
        wiringpi.delay(1000)
        wiringpi.digitalWrite(sensor.trigger, HIGH)
        wiringpi.delay(1)
        wiringpi.digitalWrite(sensor.trigger, LOW)
        #start = time.time()
	print "Trying to get distance of sensor " , sensor.position, "Trig: ", sensor.trigger, " Echo:", sensor.echo
	status = LOW
	while(wiringpi.digitalRead(sensor.echo) == LOW):
		status = LOW
	start = time.time()
	while(wiringpi.digitalRead(sensor.echo) == HIGH):
		status = LOW
	end = time.time()	

#	while status == LOW:
#	    feedback = wiringpi.digitalRead(sensor.echo)
#	    if(feedback == HIGH):
#		while(feedback == HIGH):
#		    status = LOW
#		end = time.time()
#		print("Time Elapsed: ", end-start)
#		status = HIGH
#	    if((time.time() - start) > 1):
#		end = time.time()
#		status = HIGH

        # Below divide by 340.29 for air distance, or divide by 1484 for water distance
        return (end - start)*(340.29/2)
#	status = HIGH
#	while(status == HIGH):
#	    if(wiringpi.digitalRead(sensor.echo) == HIGH):
#		start = time.time()
#		while(wiringpi.digitalRead(sensor.echo) == HIGH):
#		    status == HIGH
#		end = time.time()
#		print("Was high for: ", end-start)
#	    elif(wiringpi.digitalRead(sensor.echo) == LOW):
#		start = time.time()
#		while(wiringpi.digitalRead(sensor.echo) == LOW):
#		    status == HIGH
#		end = time.time()
#		print("Was low for: ", end-start)

