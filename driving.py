# Define driving pins
FORWARD_DRIVE = 999
BACKWARD_DRIVE = 998
PISTON_UP = 997
PISTON_DOWN=996

def get_distance(sensor):
    #wiringpi.digitalWrite(30,HIGH)
    wiringpi.digitalWrite(sensor.echo, LOW)
    wiringpi.delay(1000)
    wiringpi.digitalWrite(sensor.trigger, HIGH)
    wiringpi.delay(1)
    wiringpi.digitalWrite(sensor.trigger, LOW)
    start = time.time()
    while wiringpi.digitalRead(sensor.echo) == LOW:
        wait = True
        #print( "Pin Echo: " + str(wiringpi.digitalRead(sensor.echo)))

    # Below divide by 340.29 for air distance, or divide by 1484 for water distance
    return (time.time() - start)*(340.29/2)

