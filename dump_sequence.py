import RPi.GPIO as GPIO
import time
from flask import Flask
from flask import request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(12,GPIO.OUT)

servo1 = GPIO.PWM(11,50)
servo2 = GPIO.PWM(12,50)

servo1.start(0)
servo2.start(0)

def setBaseAngle(angle):
    duty = angle / 18 + 2
    servo1.ChangeDutyCycle(duty)
    time.sleep(0.3)
    servo1.ChangeDutyCycle(0)

def setArmAngle(angle):
    duty = angle / 18 + 2
    servo2.ChangeDutyCycle(duty)
    time.sleep(0.3)
    servo2.ChangeDutyCycle(0)

def left():
    setBaseAngle(0)

def right():
    setBaseAngle(180)

def centre():
    setBaseAngle(90)

def dump():
    setArmAngle(90)
    setArmAngle(0)

@app.route("/hello")
def hello_world():
    return "Hello World!"

@app.route("/setup")
def setup():
    return("Ready")

@app.route("/quit")
def quit():
    servo1.stop()
    servo2.stop()
    GPIO.cleanup()
    return("Quit")

@app.route("/servo", methods=['GET','POST'])
def servo():


    direction = request.json["direction"].lower()
    if (direction in "left"):
        left()
        print("Going left")
    elif (direction in "right"):
        right()
    elif (direction in "centre"):
        centre()
    time.sleep(1)
    dump()
    print(direction)
    return "went"


