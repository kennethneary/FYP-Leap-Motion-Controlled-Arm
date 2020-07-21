# !/usr/bin/python

class Joint:
  def __init__(self, minPosition, maxPosition):
    self.minPosition = minPosition
    self.maxPosition = maxPosition

  def getCommand(self, handPosition, currentPosition):
    # declare upper and lower tolerances
    treshold_u = currentPosition+15
    treshold_l = currentPosition-15
    # check if shoulder should move forward, backwards, or stop
    if handPosition > treshold_u and currentPosition <= self.maxPosition:
      return 2
    elif handPosition < treshold_l and currentPosition >= self.minPosition:
      return 1
    else:
      return 0