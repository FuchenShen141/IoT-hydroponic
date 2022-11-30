"""Run the hydroponics system."""

import time

from apscheduler.schedulers.background import BackgroundScheduler

from config import (PUMP_PIN, LIGHTS_PIN, PUMP_DEFAULT_ON, LIGHTS_DEFAULT_ON,
                    PUMP_TIME, LIGHTS_TIME_ON, LIGHTS_TIME_OFF)
from hydroponics import HydroponicsController


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    kwargs = {"pump_pin": PUMP_PIN,
              "lights_pin": LIGHTS_PIN,
              "pump_default_on": PUMP_DEFAULT_ON,
              "lights_default_on": LIGHTS_DEFAULT_ON}
    
    with HydroponicsController(**kwargs) as h:
        scheduler.add_job(h.run_pump, 'interval', hours=1, args=(PUMP_TIME,))
        scheduler.add_job(h.lights_on,  'cron', hour=LIGHTS_TIME_ON)
        scheduler.add_job(h.lights_off, 'cron', hour=LIGHTS_TIME_OFF)
        scheduler.start()

        try:
            while True:
                time.sleep(10)
        finally:
            scheduler.shutdown()
