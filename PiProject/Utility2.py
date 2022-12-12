import RPi.GPIO as GPIO
import time
import random

def setup():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    global Relay
    global GPIO_TRIGGER
    global GPIO_ECHO
    global GPIO_PUMP

    Relay=9
    GPIO_TRIGGER = 18
    GPIO_ECHO = 24
    GPIO_PUMP = 23
    #set GPIO direction (IN / OUT)
    GPIO.setup(Relay, GPIO.OUT)
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    GPIO.setup(GPIO_PUMP, GPIO.OUT)


def lightsOn():
    GPIO.output(Relay, GPIO.HIGH)
    print("Growing lights on")

def lightsOff():
    GPIO.output(Relay, GPIO.LOW)
    print("Growing lights off")
 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = round((TimeElapsed * 34300) / 2,2)
 
    return distance # unit: cm

def pump_on():
    GPIO.output(GPIO_PUMP, True)
    print('pump on')
    return
 
def pump_off():
    GPIO.output(GPIO_PUMP, False)
    print('pump off')
    return

def WaterLevel():
    return random.randint(0,100)