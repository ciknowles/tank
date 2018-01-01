import pygame,sys
import math

import RPi.GPIO as GPIO, sys, threading, time, os, subprocess
from pygame.math import Vector2
from pygame.locals import *
#from enum import Enum

speed = 30
print ("Tests the motors by using the arrow keys to control")
print ("Use , or < to slow down")
print ("Use . or > to speed up")
print ("Speed changes take effect when the next arrow key is pressed")
print ("Press Ctrl-C to end")



class MotionAction:
       STOP =0
       FORWARD = 1
       REVERSE = 2
       SPINLEFT = 3
       SPINRIGHT = 4



class Tank():
      
        
        def __init__(self):
                  # Pins 35, 36 Left Motor
                # Pins 32, 33 Right Motor
                self.L1 = 24
                self.L2 = 26
                self.R1 = 19
                self.R2 = 21

                # Define obstacle sensors and line sensors
                # These can be on any input pins, but this library assumes the following layout
                # which matches the build instructions
                self.irFL = 7
                self.irFR = 11
                self.lineLeft = 12
                self.lineRight = 13

                # Define Sonar Pin (Uses same pin for both Ping and Echo)
                self.sonar = 8

                self.ServosActive = False

                self.speed = 40

               
                GPIO.setwarnings(False)

                #use physical pin numbering
                GPIO.setmode(GPIO.BOARD)
                #print GPIO.RPI_REVISION

                #set up digital line detectors as inputs
                GPIO.setup(self.lineRight, GPIO.IN) # Right line sensor
                GPIO.setup(self.lineLeft, GPIO.IN) # Left line sensor

                #Set up IR obstacle sensors as inputs
                GPIO.setup(self.irFL, GPIO.IN) # Left obstacle sensor
                GPIO.setup(self.irFR, GPIO.IN) # Right obstacle sensor

                #use pwm on inputs so motors don't go too fast
                GPIO.setup(self.L1, GPIO.OUT)
                self.p = GPIO.PWM(self.L1, 20)
                self.p.start(0)

                GPIO.setup(self.L2, GPIO.OUT)
                self.q = GPIO.PWM(self.L2, 20)
                self.q.start(0)

                GPIO.setup(self.R1, GPIO.OUT)
                self.a = GPIO.PWM(self.R1, 20)
                self.a.start(0)

                GPIO.setup(self.R2, GPIO.OUT)
                self.b = GPIO.PWM(self.R2, 20)
                self.b.start(0)

                GPIO.setup(self.sonar, GPIO.OUT)

                self.action = MotionAction.STOP

                self.startServos()
                self.setServo(0, 0)
                self.setServo(1,0)

        # cleanup(). Sets all motors off and sets GPIO to standard values
        def cleanup(self):
            self.stop()
            self.stopServos()
            GPIO.cleanup()

        # version(). Returns 2. Invalid until after init() has been called
        def version():
            return 2 #(version 1 is Pirocon, version 2 is RoboHAT)

        # End of General Functions
        #======================================================================


        #======================================================================
        # Motor Functions
        #
        # stop(): Stops both motors
        def stop(self):
            self.p.ChangeDutyCycle(0)
            self.q.ChangeDutyCycle(0)
            self.a.ChangeDutyCycle(0)
            self.b.ChangeDutyCycle(0)
            self.action = MotionAction.STOP

        def incspeed(self, amount):
            print("inc speed ")
            if (amount>0):
                   self.speed = min(self.speed+amount, 100)
            else:
                   self.speed = max(self.speed+amount, 0)

            if (self.action == MotionAction.FORWARD):
                   self.forward()
            elif (self.action == MotionAction.REVERSE):
                   self.reverse()
            elif (self.action == MotionAction.SPINLEFT):
                   self.spinLeft()
            elif (self.action == MotionAction.SPINRIGHT):
                   self.spinRight()
                   
            
        # forward(speed): Sets both motors to move forward at speed. 0 <= speed <= 100
        def forward(self):
            print("forward")
            self.p.ChangeDutyCycle(self.speed)
            self.q.ChangeDutyCycle(0)
            self.a.ChangeDutyCycle(self.speed)
            self.b.ChangeDutyCycle(0)
            self.p.ChangeFrequency(self.speed + 5)
            self.a.ChangeFrequency(self.speed + 5)
            self.action = MotionAction.FORWARD
            
        # reverse(speed): Sets both motors to reverse at speed. 0 <= speed <= 100
        def reverse(self):
            print("reverse")
            self.p.ChangeDutyCycle(0)
            self.q.ChangeDutyCycle(self.speed)
            self.a.ChangeDutyCycle(0)
            self.b.ChangeDutyCycle(self.speed)
            self.q.ChangeFrequency(self.speed + 5)
            self.b.ChangeFrequency(self.speed + 5)
            self.action = MotionAction.REVERSE

        # spinLeft(speed): Sets motors to turn opposite directions at speed. 0 <= speed <= 100
        def spinLeft(self):
            self.p.ChangeDutyCycle(0)
            self.q.ChangeDutyCycle(self.speed)
            self.a.ChangeDutyCycle(self.speed)
            self.b.ChangeDutyCycle(0)
            self.q.ChangeFrequency(self.speed + 5)
            self.a.ChangeFrequency(self.speed + 5)
            self.action = MotionAction.SPINLEFT
            
        # spinRight(speed): Sets motors to turn opposite directions at speed. 0 <= speed <= 100
        def spinRight(self):
            self.p.ChangeDutyCycle(self.speed)
            self.q.ChangeDutyCycle(0)
            self.a.ChangeDutyCycle(0)
            self.b.ChangeDutyCycle(self.speed)
            self.p.ChangeFrequency(self.speed + 5)
            self.b.ChangeFrequency(self.speed + 5)
            self.action = MotionAction.SPINRIGHT
            

# getDistance(). Returns the distance in cm to the nearest reflecting object. 0 == no object
        def getDistance(self, sample_wait, sample_size):
           #GPIO.setup(self.sonar, GPIO.OUT)
           sample = []
           for distance_reading in range(sample_size):
                  GPIO.setup(self.sonar, GPIO.OUT)
                  GPIO.output(self.sonar, False)
                  time.sleep(sample_wait)
                  
                  # Send 10us pulse to trigger
                  GPIO.output(self.sonar, True)
                  #time.sleep(0.00001)
                  time.sleep(0.001)
                  GPIO.output(self.sonar, False)
                  echo_status_counter = 1

                  GPIO.setup(self.sonar,GPIO.IN)
                  while GPIO.input(self.sonar) ==0:
                         if echo_status_counter<1000:
                                sonar_signal_off=time.time()
                                echo_status_counter +=1
                         else:
                                raise SystemError('Echo not received')

                  while GPIO.input(self.sonar) ==1:
                         sonar_signal_on = time.time()

                  time_passed = sonar_signal_on - sonar_signal_off
                  sample.append(time_passed*34000/2)
           sorted_sample = sorted(sample)
           GPIO.cleanup((self.sonar))
           return sorted_sample[sample_size//2]
           

        def setServo(self, Servo, Degrees):
           if self.ServosActive == False:
               self.startServos()
           self.pinServod (Servo, Degrees) # for now, simply pass on the input values

        def stopServos(self):
           #print "Stopping servo"
           self.stopServod()
           
        def startServos(self):
           #print "Starting servod as CPU =", CPU
           self.startServod()
           
        def startServod(self):
           
           #print "Starting servod. ServosActive:", ServosActive
           SCRIPTPATH = os.path.split(os.path.realpath(__file__))[0]
           #os.system("sudo pkill -f servod")
           initString = SCRIPTPATH +'/servod --daemonise=1 --pcm --idle-timeout=20000 --p1pins="18,22" > /dev/null'
           os.system(initString)
           #print initString
           self.ServosActive = True

        def pinServod(self, pin, degrees):
           #print pin, degrees
           pinString = "echo " + str(pin) + "=" + str(50+ ((90 - degrees) * 200 / 180)) + " > /dev/servoblaster"
           #print pinString
           os.system(pinString)
           
        def stopServod():
           os.system("sudo pkill -f servod")
           self.ServosActive = False




pygame.init()
WIDTH = 300
HEIGHT = 300
DISPLAYSURF=pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('My Brain')

tank = Tank()
lastreading = 0
while 1:
        dis = tank.getDistance(0.05,3)
        print(dis)
               
        for event in pygame.event.get():
                if event.type==QUIT:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                                tank.spinLeft()
                        if event.key == pygame.K_RIGHT:
                                tank.spinRight()
                        if event.key == pygame.K_UP:
                                tank.forward()
                        if event.key == pygame.K_DOWN:
                                tank.reverse()
                        if ((event.key == pygame.K_GREATER) or (event.key==pygame.K_PERIOD)):
                                tank.incspeed(10)
                                
                        if ((event.key == pygame.K_LESS) or (event.key==pygame.K_COMMA)):
       
                                tank.incspeed(-10)
                                
                        if event.key == pygame.K_SPACE:
                                tank.stop()
                        if event.key == pygame.K_d:
                                dis = tank.getDistance(0.1,4)
                                print(dis)
                                         
         #               if event.key == pygame.K_RIGHT:
         #                        
         #               if event.key == pygame.K_UP:
         #                   
         #               if event.key == pygame.K_DOWN:
                            
        #pygame.display.update()




#        def forward():
#                robohat.forward
