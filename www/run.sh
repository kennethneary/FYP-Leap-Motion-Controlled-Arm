#! /bin/bash

# get IP addrres of server in order to stream video to client
sudo sh /var/www/getIPAddress.sh

# start node server
sudo node /var/www/app.js &

# start video stream
cd /home/pi/mjpg-streamer
mjpg_streamer -i "./input_uvc.so -n -f 20 -r 640x480" -o "./output_http.so -n -w ./www" 
