#! /usr/bin/env python
import wiringpi2 as wiringpi
import time

# Define main trigger and sensor echo pins
CENTER_TRIG = 18 # TRIGGER - GPIO PIN 15
CENTER_ECHO = 22 # ECHO - GPIO PIN 17
RIGHT_SENSE_ECHO = 22
LEFT_SENSE_ECHO = 22

# Define global constants
OUTPUT = 1
INPUT = 0
HIGH = 1
LOW = 0
sensors = []

# Define sensor object with trigger, echo, and relative positions
# Position 0 is center(kinect direction). - numbers are to left and + to the right
class Sensor(object):
    def __init__(self, trigger, echo, position):
	self.trigger = trigger
	self.echo = echo
	self.position = position
	self.baseline = 0


def init():
    #Initialize wiringpi interface
    wiringpi.wiringPiSetupGpio()

    # Enter all known sensors into array
    sensors.append(Sensor(CENTER_TRIG, CENTER_ECHO, 0))
    sensors.append(Sensor(CENTER_TRIG, RIGHT_SENSE_ECHO, 1))
    sensors.append(Sensor(CENTER_TRIG, LEFT_SENSE_ECHO, -1))

    for sensor in sensors: 
        wiringpi.pinMode(sensor.trigger, OUTPUT)
        wiringpi.pinMode(sensor.echo, OUTPUT)


def get_distance(sensor):
    wiringpi.digitalWrite(sensor.echo, LOW)
    wiringpi.digitalWrite(sensor.trigger, HIGH)
    wiringpi.delay(1000)
    wiringpi.digitalWrite(sensor.trigger, LOW)
    start = time.time()
    while wiringpi.digitalRead(sensor.echo) == LOW:
        wait = True
        print( "Pin Echo: " + str(wiringpi.digitalRead(sensor.echo)))

    # Below divide by 340.29 for air distance, or divide by 1484 for water distance
    return (time.time() - start)/340.29

def rotate_robot_to_object(sensor):
    if sensor.position < 0:
	print "logic to turn right"
    elif sensor.position > 0:
	print "logic to turn left"
    elif sensor.position == 0:
	print "kinect should already be facing discrepency"


def set_sensor_baselines():
    for sensor in sensors:
	sensor.baseline = get_distance(sensor)


def watch_for_possible_victim():
    while True:
	for sensor in sensors:
	    temp_dist = get_distance(sensor)
	    # if the sonar reading is more than 5% off the baseline, something could be up
	    if abs(temp_dist-sensor.baseline) > temp_dist*.05:
		rotate_robot_to_object(sensor)
		sensor.baseline = temp_dist
		analyze_with_kinect()
		    

def analyze_with_kinect():
    print ("KINECT ITS YOUR TIME TO SHINE")
    # wait for kinect reading. If there is a problem, send alert. 


def test_getting_all_distances():
    while True:
	for sensor in sensors:
	    print ("Distance for sensor position " + str(sensor.position) + " is:  " + str(get_distance(sensor)))



init()
test_getting_all_distances()  


#Algorithm for rotating is as follows:
# 1. Get to the bottom of the pool
# 2. Set baseline for ditance of each sonar sensor
# 3. Continously check distance the sensor is displaying for any change with respect to baseline.
#    If the reading is different than baseline for 5 seconds, an object has showed up or moved 
#    at that location, and we want more info. Rotate the robot so that the center sonar is now 
#    ligned up with that object.
# 4. Wait for feedback from kinect
