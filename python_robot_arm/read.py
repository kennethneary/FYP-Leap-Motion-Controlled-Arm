# !/usr/bin/python
import fcntl
import os
import sys
import subprocess
import datetime

# event class used to create event objects
class Event:
  def __init__(self, valid, base, shoulder, elbow, wrist, grip, light):
    self.valid = valid
    self.base = base
    self.shoulder = shoulder
    self.elbow = elbow
    self.wrist = wrist
    self.grip = grip
    self.light = light

  def __str__(self):
    return 'Event(Valid:%s, Base:%d, Shoulder:%d, Elbow:%d, Wrist:%d, Grip:%d, Light:%d)' % (self.valid, self.base, self.shoulder, self.elbow, self.wrist, self.grip, self.light)

# non-blocking read function
def non_block_read(output):
    fd = output.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
    try:
        return output.read()
    except:
        return ""

# set up a pipe connection to the console log of the server
def event_listener():
  # run server and connect to its standard output
  proc = subprocess.Popen("sh /var/www/run.sh", shell=True, stdout=subprocess.PIPE)
  lastValidCommandTime = datetime.datetime.now()
  while True:
    line = non_block_read(proc.stdout)
    data = line.split(" ")
    # check if data is valid
    if len(data)==7 and data[0]=="true":
      # parse data
      valid = data[0]
      base = int(data[1])
      shoulder = int(data[2])
      elbow = int(data[3])
      wrist = int(data[4])
      grip = int(data[5])
      light = int(data[6])
      # create an event object
      event = Event(valid, base, shoulder, elbow, wrist, grip, light)
      lastValidCommandTime = datetime.datetime.now()
      yield event
      # if no commands recieved within 0.5s then tell arm to stop
    if (datetime.datetime.now() - lastValidCommandTime).microseconds > 500000:
      event = Event("false", 0, 0, 0, 0, 0, 0)
      lastValidCommandTime = datetime.datetime.now()
      yield event