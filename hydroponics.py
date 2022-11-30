#!/usr/bin/python

import time
try:
    import RPi.GPIO as GPIO
except ImportError:
    pass


class HydroponicsController(object):

    def __init__(self, **kwargs):
        self.pump_pin = kwargs["pump_pin"]
        self.lights_pin = kwargs["lights_pin"]
        self.pump_default_on = kwargs["pump_default_on"]
        self.lights_default_on = kwargs["lights_default_on"]

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pump_pin, GPIO.OUT)
        GPIO.setup(self.lights_pin, GPIO.OUT)

    def pump_on(self):
        if self.pump_default_on:
            GPIO.output(self.pump_pin, GPIO.LOW)
        else:
            GPIO.output(self.pump_pin, GPIO.HIGH)

    def pump_off(self):
        if self.pump_default_on:
            GPIO.output(self.pump_pin, GPIO.HIGH)
        else:
            GPIO.output(self.pump_pin, GPIO.LOW)

    def run_pump(self, pump_time):
        """Run the pump for `pump_time` seconds."""
        self.pump_on()
        time.sleep(pump_time)
        self.pump_off()

    def lights_on(self):
        if self.lights_default_on:
            GPIO.output(self.lights_pin, GPIO.LOW)
        else:
            GPIO.output(self.lights_pin, GPIO.HIGH)

    def lights_off(self):
        if self.lights_default_on:
            GPIO.output(self.lights_pin, GPIO.HIGH)
        else:
            GPIO.output(self.lights_pin, GPIO.LOW)

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        GPIO.cleanup()



if __name__ == '__main__':
    kwargs = {"pump_pin": 13,
              "lights_pin": 11,
              "pump_default_on": False,
              "lights_default_on": True}
    
    with HydroponicsController(**kwargs) as h:
        print "Hit Ctrl + C to interrupt process."
        while True:
            h.lights_on()
            time.sleep(5)
            h.lights_off()
            time.sleep(5)
