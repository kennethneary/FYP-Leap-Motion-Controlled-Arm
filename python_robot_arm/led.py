# !/usr/bin/python

class LED:
  def getCommand(self, numberOfHands):
    # if more than one hand detected then tuen on LED
    if numberOfHands > 1:
      return 1
    else:
      return 0