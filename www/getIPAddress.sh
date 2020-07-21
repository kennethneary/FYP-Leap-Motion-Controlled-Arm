#! /bin/bash

# update the IP addres in index.jade in order to stream video

# get the IP address in file index.jade
x=$(grep -Eo '([0-9]*\.){3}[0-9]*' /var/www/views/index.jade) 

# get the new IP address of the Raspberry Pi and remove all unwanted text
y=$(hostname -I | sed 's/ *$//g')

# replace IP address in file with new IP address of Raspberry Pi
sudo sed -i -e "s/$x/$y/g" /var/www/views/index.jade
