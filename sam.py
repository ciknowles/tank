#!/usr/bin/python
# servoTest.py

import robohat
from TankServos import TankServos
import time

# Define pins for Pan/Tilt
pan = 0
tilt = 1

servo = TankServos()

servo.doServos(0,0)
time.sleep(5)

#servo.doServos(0,80)
#time.sleep(5)

#servo.doServos(0,-80)
#time.sleep(5)

for x in range(1,2):
    servo.doServos(50,0)
    time.sleep(2)
    servo.doServos(10,80)
    time.sleep(2)
    servo.doServos(10,-80)

    time.sleep(2)
    servo.doServos(-10,0)
