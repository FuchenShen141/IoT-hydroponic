import RPi.GPIO as GPIO
import time
import random

Relay=9
GPIO.setmode(GPIO.BCM)
GPIO.setup(Relay, GPIO.OUT)
while True:

    GPIO.output(Relay, GPIO.HIGH)