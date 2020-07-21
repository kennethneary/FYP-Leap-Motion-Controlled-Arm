# !/usr/bin/python
import RPi.GPIO as GPIO

# set up connection with button on GPIO pin 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

class Joint:
  def __init__(self, minPosition, maxPosition):
    self.minPosition = minPosition
    self.maxPosition = maxPosition

  def getCommand(self, handPosition, currentPosition):
    # declare upper and lower tolerances
    treshold_u = currentPosition+15
    treshold_l = currentPosition-15
    # check if claw should move open, close, or stop
    if handPosition > treshold_u and (currentPosition) <= self.maxPosition:
      # if button pressed then stop closing claw
      if GPIO.input(23):
        return 0
      else:
        return 1
    elif handPosition < treshold_l and (currentPosition-10) >= self.minPosition:
      return 2
    else:
      return 0