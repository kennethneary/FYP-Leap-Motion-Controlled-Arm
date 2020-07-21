# !/usr/bin/python
import arm
import read
import spidev
import time
import base
import elbow
import wrist
import led
import claw
import shoulder

# create a RoboticArm instance
rArm = arm.RobotArm()

# open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)

# create joint and LED instances
base_joint = base.Joint(280, 750)
shoulder_joint = shoulder.Joint(440, 880)
elbow_joint = elbow.Joint(200, 720)
wrist_joint = wrist.Wrist(430, 600)
grip_claw = claw.Joint(450, 550)
light_led = led.LED()
 
# read from SPI function
def readADC(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data
  
try:
  # listen for event objects from read.py
  for event in read.event_listener(): 
    # check if event object is valid
    if event.valid == "true":
      # get command of each joint
      # the command determines how each joint should move
      # this is done by comparing the desired sample potentiometer value with its actual current sample potentiometer value
      base_command = base_joint.getCommand(event.base, readADC(0))
      shoulder_command = shoulder_joint.getCommand(event.shoulder, readADC(1))
      elbow_command = elbow_joint.getCommand(event.elbow, readADC(2))
      wrist_command =  wrist_joint.getCommand(event.wrist, readADC(3))
      grip_command = grip_claw.getCommand(event.grip, readADC(4))
      led_command = light_led.getCommand(event.light)
      # send each joints command to the RoboticArm instance to be converted to a usb command
      rArm.moveJoints(base_command, shoulder_command, elbow_command, wrist_command, grip_command, led_command)
    else:
      rArm.resetAll();
	
except KeyboardInterrupt:
  # if normal ececution interrupted then tell arm to stop moving
  rArm.resetAll();
  print "Exiting arm commands!"


 
