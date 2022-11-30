import time
from threading import Thread
from time import sleep
#'from waiting import wait
import RPi.GPIO as GPIO
import random

Mode=-1
Stuck=0
Edge=0
IsOn=" "
IsOff="active"
IsMode0=" "
IsMode1=" "
from flask import Flask, redirect, render_template

app = Flask(__name__, static_folder='assets')

@app.route("/")

def Home():
    return render_template('index.html',IsOff=IsOff,IsOn=IsOn, IsMode0=IsMode0, IsMode1=IsMode1)

@app.route('/power/<int:action>')
def SwitchPower(action):
    global IsOff
    global IsOn
    IsOff="active"
    IsOn=" "
    if action==0:
        IsOff="active"
        IsOn=" "
        sleep(1)

    elif action==1:
        IsOff=" "
        IsOn="active"
    return redirect("/")

@app.route('/mode/<int:action>')
def SwitchMode(action):
    global Mode
    global IsMode0
    global IsMode1
    IsMode0=" "
    ISMode1=" "
    if action==0:
        IsMode0="active"
        IsMode1=" "
        Mode=0
    elif action==1:
        IsMode0=" "
        IsMode1="active"
        Mode=1
    return redirect("/")

@app.route('/AdditionalInformation')
def loadInfo():
    return render_template('AdditionalInformation.html')

if __name__ == "__main__":
    try:
        #t1=Thread(target=GetStuck)
        #t1.start()
        app.run(host='0.0.0.0', port=9876, debug=True, threaded=True)
        #t1.join()
    except KeyboardInterrupt:
        GPIO.cleanup()