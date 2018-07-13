import threading
from socket import *
import RPi.GPIO as GPIO                    #Import GPIO library
import time
import urllib2
from wireless import Wireless
import RPi.GPIO as GPIO                    #Import GPIO library
import requests
import sys
import os

cmd = 'ifconfig wlan0 down'
cmd1 = 'ifconfig wlan0 up'
iter = 0
#Import time library
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)                    # programming the GPIO by BCM pin numbers

TRIG = 17
ECHO = 27

TRIG1 = 14
ECHO1 = 15

TRIG2 = 2
ECHO2 = 3

m11=21
m12=20
m21=16
m22=12

GPIO.setup(TRIG,GPIO.OUT)                  # initialize GPIO Pin as outputs
GPIO.setup(ECHO,GPIO.IN)                   # initialize GPIO Pin as input                 

GPIO.setup(TRIG1,GPIO.OUT)                  # initialize GPIO Pin as outputs
GPIO.setup(ECHO1,GPIO.IN) 

GPIO.setup(TRIG2,GPIO.OUT)                  # initialize GPIO Pin as outputs
GPIO.setup(ECHO2,GPIO.IN) 
GPIO.setup(m11,GPIO.OUT)
GPIO.setup(m12,GPIO.OUT)
GPIO.setup(m21,GPIO.OUT)
GPIO.setup(m22,GPIO.OUT)

time.sleep(5)

def stop():
    print "stop"
    GPIO.output(m11, 0)
    GPIO.output(m12, 0)
    GPIO.output(m21, 0)
    GPIO.output(m22, 0)

def forward():
    GPIO.output(m11, 1)
    GPIO.output(m12, 0)
    GPIO.output(m21, 1)
    GPIO.output(m22, 0)
    time.sleep(0.2)
    print "Forward"

def back():
    GPIO.output(m11, 0)
    GPIO.output(m12, 1)
    GPIO.output(m21, 0)
    GPIO.output(m22, 1)
    print "back"

def left():
    GPIO.output(m11, 1)
    GPIO.output(m12, 0)
    GPIO.output(m21, 0)
    GPIO.output(m22, 0)
    print "left"
    time.sleep(0.6)

def right():
    GPIO.output(m11, 0)
    GPIO.output(m12, 0)
    GPIO.output(m21, 1)
    GPIO.output(m22, 0)
    print "right"
    time.sleep(0.6)

'''class DataSend(object):
    def __init__(self, interval=1):
        self.interval = interval
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution
        
    def run(self):
        self.s = socket(AF_INET, SOCK_DGRAM)
        self.server_address = ('192.168.43.186', 4210)
        self.message = 'This is the message.  It will be repeated.
        
        while True:
            wireless = Wireless()
            print wireless.current()
            if iter==0:
                if wireless.current()== "I-Bot":
                    response = urllib2.urlopen('http://11.11.11.11/')
                    html = response.read()
                    humidity,temperature = html.split("....")
                    print humidity,temperature
            elif iter%2 ==1:
            else:
                print "Cant retieve data"
            self.sent = self.s.sendto(self.message, self.server_address)
            self.data, self.server = self.s.recvfrom(4096)
            print('Doing something imporant in the background',self.data)
            time.sleep(self.interval)

example = DataSend()
time.sleep(3)
print('Checkpoint')
time.sleep(2)
print('Bye')'''

tem=0
hum=0

def iBot(i):
    wireless = Wireless(['wlan0'])
    link="https://rajayalla98.pythonanywhere.com/get"
    if i == 9:
        if wireless.connect(ssid='I-Bot', password='12345678'):
            time.sleep(100)
            print wireless.current()
            response = urllib2.urlopen('http://11.11.11.11/')
            
            html = response.read()
            humidity,temperature = html.split("....")
            print humidity,temperature
            return temperature,humidity
            
        else:
            print "Did not connect"
            return [tem,hum]
    elif i == 19:
        if wireless.connect(ssid='Dont ask me', password='Kalyan@1'):
            data = {'temperature':tem,'humidity':hum}
            time.sleep(10)
            print wireless.current()
            requests.get(link,params=data)
            return [tem,hum]
        else:
            print "Did not connect"
            return [tem,hum]
    else:
        print "in loop"
        return [tem,hum]
            
def calcavg():
    i=0
    avgDistance=0
    for i in range(5):
        GPIO.output(TRIG, False)                 #Set TRIG as LOW
        time.sleep(0.1)                                   #Delay
        
        GPIO.output(TRIG, True)                  #Set TRIG as HIGH
        time.sleep(0.00001)                           #Delay of 0.00001 seconds
        GPIO.output(TRIG, False)                 #Set TRIG as LOW

        while GPIO.input(ECHO)==0:              #Check whether the ECHO is LOW
           # wait for the signal to come back
            a=1
        pulse_start = time.time()

        while GPIO.input(ECHO)==1:              #Check whether the ECHO is HIGH
           #claculate time
            a=2
        pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start #time to get back the pulse to sensor

        distance = pulse_duration * 17150        #Multiply pulse duration by 17150 (34300/2) to get distance
        distance = round(distance,2)                 #Round to two decimal points
        avgDistance=avgDistance+distance

    avgDistance=avgDistance/5
    print avgDistance
    return avgDistance




def calcleft():
    i=0
    avgDistance=0
    for i in range(5):
        GPIO.output(TRIG2, False)                 #Set TRIG as LOW
        time.sleep(0.1)                                   #Delay

        GPIO.output(TRIG2, True)                  #Set TRIG as HIGH
        time.sleep(0.00001)                           #Delay of 0.00001 seconds
        GPIO.output(TRIG2, False)                 #Set TRIG as LOW

        while GPIO.input(ECHO2)==0:              #Check whether the ECHO is LOW
           # wait for the signal to come back
            a=1
        pulse_start = time.time()

        while GPIO.input(ECHO2)==1:              #Check whether the ECHO is HIGH
           #claculate time
            a=2
        pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start #time to get back the pulse to sensor

        distance = pulse_duration * 17150        #Multiply pulse duration by 17150 (34300/2) to get distance
        distance = round(distance,2)                 #Round to two decimal points
        avgDistance=avgDistance+distance

    avgDistance=avgDistance/5
    print avgDistance
    if avgDistance < 15:
        return False
    else:
        return True

def calcright():
    i=0
    avgDistance=0
    print("obstacle detected")
    for i in range(5):
        GPIO.output(TRIG1, False)                 #Set TRIG as LOW
        time.sleep(0.1)                                   #Delay

        GPIO.output(TRIG1, True)                  #Set TRIG as HIGH
        time.sleep(0.00001)                           #Delay of 0.00001 seconds
        GPIO.output(TRIG1, False)                 #Set TRIG as LOW

        while GPIO.input(ECHO1)==0:              #Check whether the ECHO is LOW
           # wait for the signal to come back
            a=1
        pulse_start = time.time()

        while GPIO.input(ECHO1)==1:              #Check whether the ECHO is HIGH
           #claculate time
            a=2
        pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start #time to get back the pulse to sensor

        distance = pulse_duration * 17150        #Multiply pulse duration by 17150 (34300/2) to get distance
        distance = round(distance,2)                 #Round to two decimal points
        avgDistance=avgDistance+distance

    avgDistance=avgDistance/5
    print avgDistance
    if avgDistance < 15:
        return False
        print("returned false")
    else:
        print("returned true")
        return True
        

def turnrightfun():
    flag = 1
    inc = 0
    forward()
    #time.sleep(0.3)
    stop()
    while True:
        if calcleft():
            left()
            #time.sleep(0.4)
            stop()
            forward()
            #time.sleep(0.3)
            stop()
            inc += 1
            break
        else:
            forward()
            #time.sleep(0.3)
            stop()
            flag += 1
    while True:
        if calcleft() == True:
            forward()
            stop()
            forward()
            stop()
            left()
            #time.sleep(0.4)
            stop()
            while flag!=0:
                forward()
                #time.sleep(0.3)
                stop()
                flag -= 1
            break
        else:
            forward()
            inc += 1
            #time.sleep(0.3)
            stop()
    forward()
    stop()
    right()
    #time.sleep(0.4)
    stop()
    return inc


def turnleftfun():
    flag = 1
    inc = 0
    forward()
    #time.sleep(0.3)
    stop()
    while True:
        if calcright() == True:
            right()
            #time.sleep(0.4)
            stop()
            forward()
            #time.sleep(0.3)
            stop()
            inc += 1
            break
        else:
            forward()
            #time.sleep(0.3)
            stop()
            flag += 1
    while True:
        if calcright() == True: 
            right()
            #time.sleep(0.4)
            stop()
            while flag!=0:
                forward()
                #time.sleep(0.3)
                stop()
                flag -= 1
            break
        else:
            forward()
            #time.sleep(0.3)
            stop()
    forward()
    stop()
    left()
    #time.sleep(0.4)
    stop()
    return inc


stop()
inc=0
path = []
for i in range(0,9):
    path.append(0)
path.append(1)
for i in range(0,9):
    path.append(0)
path.append(1)
for i in range(0,9):
    path.append(0)
path.append(1)
for i in range(0,9):
    path.append(0)

while True:
 for i in range(0,len(path)):
     tem,hum = iBot(i)
     print i
     avgDistance=calcavg()
     if avgDistance>15:
         if path[i] == 0:
             forward()
             #time.sleep(0.3)
         elif path[i] == 1:
             time.sleep(1)
             right()
             #time.sleep(0.4)
         elif path[i] == 2:
             time.sleep(1)
             left()
             #time.sleep(0.4)
         stop()
     elif avgDistance<15:
         if calcright() == True:
             #time.sleep(0.5)
             right()
             #time.sleep(0.4)
             stop()
             inc = turnrightfun()
             i+=inc
         elif calcleft() == True:
             print("entered left")
             #time.sleep(0.5)
             left()
             #time.sleep(0.4)
             stop()
             inc = turnleftfun()
             i+=inc
         else:
             stop()
             break