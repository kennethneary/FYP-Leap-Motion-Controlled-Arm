# !/usr/bin/python

class Joint:
  def __init__(self, minPosition, maxPosition):
    self.minPosition = minPosition
    self.maxPosition = maxPosition

  def getCommand(self, handPosition, currentPosition):
    # declare upper and lower tolerances
    treshold_u = currentPosition+30
    treshold_l = currentPosition-30
    # check if elbow should move up, down, or stop
    if handPosition > treshold_u and (currentPosition+10) <= self.maxPosition:
      return 1
    elif handPosition < treshold_l and (currentPosition-10) >= self.minPosition:
      return 2
    else:
      return 0