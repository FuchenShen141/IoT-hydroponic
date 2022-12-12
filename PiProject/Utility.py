import RPi.GPIO as GPIO
import time
import random
import os
import glob


def setup():
    #GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    global Relay
    global GPIO_TRIGGER
    global GPIO_ECHO
    global GPIO_PUMP
    global base_dir
    global device_folder
    global device_file

    Relay=9
    GPIO_TRIGGER = 18
    GPIO_ECHO = 24
    GPIO_PUMP = 23
    #set GPIO direction (IN / OUT)
    GPIO.setup(Relay, GPIO.OUT)
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    GPIO.setup(GPIO_PUMP, GPIO.OUT)
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
 
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'


def lightsOn():
    GPIO.output(Relay, True)
    print("Growing lights on")

def lightsOff():
    GPIO.output(Relay, False)
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
    low=7.3
    high=2.6
    perfect= 3.7
    dist=distance()
    p=int(((low-dist)/(low-high))*100)
    if p<0:
        return 0
    elif p>100:
        return 100
    else:
        return p

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while not lines or lines[0].strip()[-3:] != 'YES' or "00 00 00 00 00 00 00 00 00" in lines[0]:
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        #return temp_c, temp_f
        return temp_c # celsius