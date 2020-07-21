import spidev
import time
 
# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
 
def readADC(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data
  
while True:
    print "Channel", 4,"=", readADC(4)
    time.sleep(0.6)
