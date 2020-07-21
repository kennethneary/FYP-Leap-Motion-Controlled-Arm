# !/usr/bin/python
import usb.core
import time

class RobotArm:

  # set up connection with robot arm via usb
  def __init__(self):
    self.device = usb.core.find(idVendor=0x1267, idProduct=0x0000)
    if self.device is None:
       raise ValueError("RobotArm not found")
    self.device.set_configuration()
    self.led = 0
    self.resetAll()

  # send command to robot arm
  def updateArm(self):
    newCmd = self.buildCommand()
    self.device.ctrl_transfer(0x40, 0x06, 0x100, 0, newCmd, 1000)

  # generate usb command 
  def buildCommand(self):
    command_byte1 = (self.shoulder*64) + (self.elbow*16) + (self.wrist*4) + self.grip
    command_byte2 = self.base
    command_byte3 = self.led
    command = (command_byte1, command_byte2, command_byte3)
    return command

  # reset all joints to stop them moving
  def resetAll(self):
    self.base = 0
    self.shoulder = 0
    self.elbow = 0
    self.wrist = 0
    self.grip = 0
    self.led = self.led
    self.updateArm()

  # set all joints for usb command
  def setBase(self, value):
    if(value in range(0,3)):
      self.base = value
    else:
      self.base = 0

  def setShoulder(self, value):
    if(value in range(0,3)):
      self.shoulder = value
    else:
      self.shoulder = 0

  def setElbow(self, value):
    if(value in range(0,3)):
      self.elbow = value
    else:
      self.elbow = 0

  def setWrist(self, value):
    if(value in range(0,3)):
      self.wrist = value
    else:
      self.wrist = 0

  def setGrip(self, value):
    if(value in range(0,3)):
      self.grip = value
    else:
      self.grip = 0

  def setLED(self, value):
    if(value in range(0,2)):
      self.led = value
    else:
      self.led = 0

  # function to set all joint and move arm
  def moveJoints(self, base, shoulder, elbow, wrist, grip, led):
    print "arm::: Base:%d Shoulder:%d Elbow:%d Wrist:%d Grip:%d LED:%d" % (base, shoulder, elbow, wrist, grip, led)
    self.setBase(base)
    self.setShoulder(shoulder)
    self.setElbow(elbow)
    self.setWrist(wrist)
    self.setGrip(grip)
    self.setLED(led)
    self.updateArm()
