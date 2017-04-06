#! /usr/bin/env python
import wiringpi2 as wiringpi
import time
import readchar
import subprocess
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
	check_for_victim = True   
	while check_for_victim:
        	for sensor in sonar.sensors:
            		temp_dist = sonar.get_distance(sensor)
            		# if the sonars detect an object within a 3 meter radius, take a closer look
            		if temp_dist < 3.0:
            	    		rotate_robot_to_object(sensor)
            	    		sensor.baseline = temp_dist
            	    		check_for_victim = analyze_with_kinect()

# return bool is in reference not to drowning, but to whether the loop 
# which contains it should continue running. Confusing, maybe, so I'm
# sorry
def analyze_with_kinect():
	response = subprocess.check_output(['bash','run.sh'])
	
	res = str(response[-2:])
	output = res[0]	
	print "python response: " + str(output)

	if int(output) == 1:
		print 'drowning'
		return False
	elif int(output) == 0:
		print 'not drowning'
		return True
	else:
		print 'fuck'
	
# Initialize classes to control sonar array and drivetrain
#sonarArray = Sonar_Array()
#drivetrain = Drivetrain()

# Assorted Testing Functions
#test_driving_functions(drivetrain)
#test_gpio(18)
#test_getting_all_distances(sonarArray)

#main loop. watch_for_possible_victim() will run forever if no victim is found,
# so the alert_pi (which should alert the pi board but isn't implemented yet)
# will only run if that loop ever finishes, which indicates a drowning victim has
# been found

	#watch_for_possible_victim()
	#alert_pi()

analyze_with_kinect()
