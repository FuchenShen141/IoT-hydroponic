import time
import Utility
from threading import Thread, Event
from time import sleep
from flask import Flask, redirect, render_template,request
import RPi.GPIO as GPIO
import random
import sys
from datetime import datetime


Power=0
app = Flask(__name__, static_folder='assets')
Utility.setup()
IsOn=" "
IsOff="active"
IsMode0="active"
IsMode1=" "
WaterLevel=0
WaterLevel2=0
IsValve1=""
IsValve0="active"
IsLights1=""
IsLights0="active"
Dt="08:00"
Nt="14:00"
Irri="06:30"
PiTime=""

def backtoDefault():
    global IsValve1
    global IsValve0
    global IsLights1
    global IsLights0
    IsValve1=""
    IsValve0="active"
    IsLights1=""
    IsLights0="active"
    Utility.pump_off()
    Utility.lightsOff()
def ClockT():
    global PiTime
    while True and IsMode0=="active" and Power==1:
        time_now = datetime.now()
        PiTime = time_now.strftime("%H:%M")
        print(PiTime)
        sleep(15)
def AutoModeT():
    global Power
    global IsMode0
    global PiTime
    global Dt
    global Nt
    global Irri
    status=False
    while IsMode0=="active" and Power==1:
        if PiTime==Dt:
            Utility.lightsOn()
        if PiTime==Nt:
            Utility.lightsOff()
        if PiTime==Irri:
            if Utility.WaterLevel()<100 :
                Utility.pump_on()
            while Utility.WaterLevel()<100 and IsMode0=="active" and Power==1: 
                pass
            if Utility.WaterLevel()>=100:
                Utility.pump_off()

@app.route("/")
def Home():
    global WaterLevel
    WaterLevel=Utility.WaterLevel()
    t1=Thread(target=ClockT)
    t1.start()
    backtoDefault()
    return render_template('index.html',IsOff=IsOff,IsOn=IsOn, IsMode0=IsMode0, IsMode1=IsMode1,WaterLevel=WaterLevel, WaterTemp=Utility.read_temp())

@app.route('/power/<int:action>')
def SwitchPower(action):
    global IsOff
    global IsOn
    global Power
    
    if action==0:
        Power=0
        IsOn=" "
        IsOff="active"
        backtoDefault()
    elif action==1:
        Power=1
        IsOn="active"
        IsOff=" "
    return redirect("/")

@app.route('/mode/<int:action>')
def SwitchMode(action):
    global Mode
    global IsMode0
    global IsMode1
    #Mode=0 Auto; Mode=1 Manual
    if action==0:
        Mode=0
        IsMode0="active"
        IsMode1=" "
        t2= Thread(target=AutoModeT)
        t2.start()
        return redirect("/")
    elif action==1:
        Mode=1
        IsMode1="active"
        IsMode0=" "
        #return render_template('Manual.html',IsOff=IsOff,IsOn=IsOn, IsMode0=IsMode0, IsMode1=IsMode1)
        return redirect("/Manual")

@app.route('/Manual')
def loadManual():
    global WaterLevel2
    WaterLevel2=Utility.WaterLevel()
    return render_template('Manual.html',IsOff=IsOff,IsOn=IsOn, IsValve1=IsValve1, IsValve0=IsValve0,IsLights1=IsLights1, IsLights0=IsLights0,WaterLevel=WaterLevel2, WaterTemp=Utility.read_temp())




@app.route('/Manual.html')
def loadManualhtml():
    return redirect("/Manual")



@app.route('/index.html')
def returnhome():
    return redirect("/")

@app.route('/manual/power/<int:action>')
def ManualPower(action):
    global IsOff
    global IsOn
    global Power
    if action==0:
        Power=0
        IsOff="active"
        IsOn=" "
        backtoDefault()
        Utility.pump_off()
        Utility.lightsOff()
    elif action==1:
        Power=1
        IsOn="active"
        IsOff=" "
    return redirect("/Manual")

@app.route('/manual/valve/<int:action>')
def ManualValve(action):
    global Power
    global IsValve0
    global IsValve1
    if action==0 and Mode==1:
        IsValve0="active"
        IsValve1=" "
        Utility.pump_off()
    elif action==1 and Power==1 and Mode==1:
        IsValve1="active"
        IsValve0=" "
        Utility.pump_on()
    return redirect("/Manual")

@app.route('/manual/lights/<int:action>')
def ManualLights(action):
    global Power
    global IsLights0
    global IsLights1
    if action==0 and Power==1 and Mode==1:
        IsLights0="active"
        IsLights1=" "
        Utility.lightsOff()
    elif action==1 and Power==1 and Mode==1:
        IsLights1="active"
        IsLights0=" "
        Utility.lightsOn()
    return redirect("/Manual")

# @app.route('/Auto.html')
# def Auto():
#     return render_template('Auto.html')

@app.route('/Auto.html', methods=["POST","GET"])
def AutoSetting():
    if request.method =="POST":
        global Dt
        global Nt
        global Irri
        Dt=request.form.get('Daytime')
        Nt=request.form.get('Nighttime')
        Irri=request.form.get('Irrigation')
        print("Day is ", Dt)
        print("Night is ", Nt)
        return render_template('Auto.html',Daytime=Dt, Nighttime=Nt,Irrigation=Irri)
    else:
        return render_template('Auto.html',Daytime=Dt, Nighttime=Nt,Irrigation=Irri)
    
if __name__ == "__main__":
    try:
        #t1=Thread(target=Automode)
        #t1.start()
        app.run(host='0.0.0.0', port=9876, debug=True, threaded=True)
        #t1.join()
    except KeyboardInterrupt:
        GPIO.cleanup()