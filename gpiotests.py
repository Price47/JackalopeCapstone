#! /usr/bin/env python
import wiringpi2 as wiringpi
import time
import readchar
from sonar import Sonar_Array, Sensor

# Define global constants
OUTPUT = 1
INPUT = 0
HIGH = 1
LOW = 0

def test_getting_all_distances(array):
    while True:
        for sensor in array.sensors:
            print ("Distance for sensor position " + str(sensor.position) + " is:  " + str(array.get_distance(sensor)))

def test_driving_functions(dt):
    print("w: Move Forward")
    print("a: Move Backward")
    print("s: Turn Left")
    print("d: Turn Right")
    print("k: Stop All Movement")
    print("o: Move piston out")
    print("l: Move piston in")
    input = ''
    while input != "\'x\'":
        input = repr(readchar.readchar())
        if input == "\'w\'":
            dt.drive_forward()
        elif input == "\'a\'":
            dt.turn_left()
        elif input == "\'s\'":
            dt.drive_backward()
        elif input == "\'d\'":
            dt.turn_right()
        elif input == "\'k\'":
            dt.stop_all()
        elif input == "\'o\'":
	    dt.piston_out()
        elif input == "\'l\'":
            print ("")
            dt.piston_in()
    dt.stop_all()

def test_gpio(pinNum):
    input = ''
    pin = pinNum
    #wiringpi.pinMode(pin, OUTPUT)

    while input != "\'x\'":
        input = repr(readchar.readchar())
        if input == "\'w\'":
            print("Bring UP")
            wiringpi.digitalWrite(pin,HIGH)
        elif input == "\'s\'":
            print("Bring down")
            wiringpi.digitalWrite(pin,LOW)

def gpio_up(pinNum):
    input = ''
    pin = pinNum
    wiringpi.pinMode(pin, OUTPUT)
    wiringpi.digitalWrite(pin, HIGH)

def gpio_down(pinNum):
    input = ''
    pin = pinNum
    wiringpi.pinMode(pin, OUTPUT)
    wiringpi.digitalWrite(pin, LOW)


