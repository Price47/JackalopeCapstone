#! /usr/bin/env python
import wiringpi2 as wiringpi
import time
import readchar
from sonar  import Sonar_Array, Sensor
from drivetrain import Drivetrain
from gpiotests import *

def rotate_robot_to_object(sensor):
    if sensor.position < 0:
        print "logic to turn right"
    elif sensor.position > 0:
        print "logic to turn left"
    elif sensor.position == 0:
        print "kinect should already be facing discrepency"

def watch_for_possible_victim():
    while True:
        for sensor in sonar.sensors:
            temp_dist = sonar.get_distance(sensor)
            # if the sonars detect an object within a 3 meter radius, take a closer look
            if temp_dist < 3.0:
                rotate_robot_to_object(sensor)
                sensor.baseline = temp_dist
                analyze_with_kinect()

def analyze_with_kinect():
    print ("KINECT ITS YOUR TIME TO SHINE")
    # wait for kinect reading. If there is a problem, send alert. 

# Initialize classes to control sonar array and drivetrain
sonarArray = Sonar_Array()
drivetrain = Drivetrain()

# Assorted Testing Functions
#test_driving_functions(drivetrain)
#test_gpio(18)
test_getting_all_distances(sonarArray)
