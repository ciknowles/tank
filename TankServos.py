#!/usr/bin/python
# servoTest.py

import robohat
import time


# Define pins for Pan/Tilt

from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

class TankServos(object):
    sstate = {}
    pan = 1   
    tilt = 0
    
    
    pool = ThreadPool(2)
    
    def __init__(self):
        robohat.init()
        print ("Robohat version: ", robohat.version())
        self.sstate[self.tilt]=0
        self.sstate[self.pan]=0
        robohat.setServo(self.pan, self.sstate[self.pan])
        robohat.setServo(self.tilt, self.sstate[self.tilt])

    def doServos(self, panVal, tiltVal):
       self.pool.map(self.doServo, [{'servo':self.pan,'val':panVal},{'servo':self.tilt,'val':tiltVal}])
       #self.pool.close()

    def doServo(self, item):
        sid = item['servo']
        val = item['val']

        step = 5
        if (val<self.sstate[sid]):
            step = -step
        #current - target
        for s in range(self.sstate[sid], val,step):
            robohat.setServo(sid, s)
            time.sleep(0.0001)

        robohat.setServo(sid, val)
        self.sstate[sid]=val

       #robohat.cleanup()
