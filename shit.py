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

wiringpi.wiringPiSetupGpio()
pin = 18
wiringpi.pinMode(pin, OUTPUT)

while input != "\'x\'":
    input = repr(readchar.readchar())
    if input == "\'w\'":
        print("Bring UP")
        wiringpi.digitalWrite(pin,HIGH)
    elif input == "\'s\'":
        print("Brind down")
        wiringpi.digitalWrite(pin,LOW)



